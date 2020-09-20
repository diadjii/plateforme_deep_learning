from keras.models import Sequential, load_model
from keras.layers import Dense,Dropout,Flatten
from keras.losses import mean_squared_error as mse
from keras.utils import to_categorical
from keras import models
from keras.datasets import mnist

import os, sys


sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from models.keras_ssd300 import ssd_300
from Callbacks.callbacks import Callbacks
from Optimizers.optimizers import Optimizer
from Losses.losses import Loss
# from keras_loss_function.keras_ssd_loss import SSDLoss
import tensorflow as tf

from keras_layers.keras_layer_AnchorBoxes import AnchorBoxes
from keras_layers.keras_layer_DecodeDetections import DecodeDetections
from keras_layers.keras_layer_DecodeDetectionsFast import DecodeDetectionsFast
from keras_layers.keras_layer_L2Normalization import L2Normalization
from mrcnn.config import Config
from mrcnn import model as modellib, utils

sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'utils'))
from generic_utils import launch_func

class RCNNConfig(Config):
	#Move this in the configuration instance in the future ?
	NAME = "DEFAULT_NAME"


	def __init__(self,conf):
		if conf['TASK']=="INFERENCE":
			self.GPU_COUNT=1
			self.IMAGES_PER_GPU=1
		self.NUM_CLASSES = len(conf['CLASSES'])
		self.STEPS_PER_EPOCH=100
		if "MODEL_NAME" in conf :
			self.NAME = conf['MODEL_NAME']
		super().__init__()

class ModelInstance:
	def __init__(self,conf):
		self.conf=conf
		self.callbacks = None
		self.lr = None
		if conf['TASK'] =="TRAIN" or conf['TASK']=='FIND_LR' or conf['MODEL_TYPE'] == 'SSD300':
			self.compil_options = conf['COMPILATION']
		self.check_conf()
		# self.model=self.load_model()

	def load_model(self):
		model_type = self.conf['MODEL_TYPE']
		if model_type=="DENSE_MNIST":
			self.model = self.load_simple_mnist()
		if model_type=="KERAS":
			self.model = self.load_keras_model()
		if model_type=='SSD300':
			self.model = self.load_ssd300()
		if model_type=="RCNN":
			self.model = self.load_rcnn()
		return self.model

	def load_weights(self,model):
		if self.conf['WEIGHTS_PATH'] == "rcnn_imagenet":
			weights_path = model.get_imagenet_weights()
			model.load_weights(weights_path,by_name=True)
		elif self.conf['WEIGHTS_PATH'] == "rcnn_coco":
			weights_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'weights'),'mask_rcnn_coco.h5')
			model.load_weights(weights_path,
							   by_name=True,
							   exclude=["mrcnn_class_logits",
							   			"mrcnn_bbox_fc",
										"mrcnn_bbox",
										"mrcnn_mask"])
		else:
			model.load_weights(self.conf['WEIGHTS_PATH'],by_name=True)

	def load_model_from_weights(self):
		print('Loading model from weights... ')
		if self.conf['MODEL_TYPE']=="SSD300":
			loss = self.get_loss()
			model = load_model(self.conf['WEIGHTS_PATH'],
								custom_objects ={'AnchorBoxes': AnchorBoxes,
							                     'L2Normalization': L2Normalization,
							                     'DecodeDetections': DecodeDetections,
							                     'compute_loss': loss})
			self.model = model
		if self.conf['MODEL_TYPE']=="RCNN":
			model = self.load_model()

		return model

	def load_simple_mnist(self):
		model = Sequential()
		model.add(Dense(512,input_shape=(28*28,),activation='relu'))
		model.add(Dropout(0.2))
		model.add(Dense(512,activation='relu'))
		model.add(Dropout(0.2))
		model.add(Dense(10,activation='softmax'))
		if self.conf['TASK'] == "FIND_LR":
			model = Sequential()
			model.add(Dense(128,input_shape = (28,28,1),activation='relu'))
			model.add(Dropout(0.2))
			model.add(Flatten())
			model.add(Dense(64,activation='relu'))
			model.add(Dropout(0.2))
			model.add(Dense(10,activation='softmax'))
		return model

	def load_keras_model():
		print('TODO : load all keras integrated models ? ')
		return 0


	def load_rcnn(self):
		RcnnConfig = RCNNConfig(self.conf)
		# RcnnConfig.set(self.conf)
		self.rcnnconf=RcnnConfig
		RcnnConfig.display()
		if self.conf['TASK']=="TRAIN":
			model = modellib.MaskRCNN(mode="training",
									  config=RcnnConfig,
	                                  model_dir=self.conf['LOGS_PATH'])
		else :
			model = modellib.MaskRCNN(mode="inference",
									  config=RcnnConfig,
	                                  model_dir=self.conf['LOGS_PATH'])
		self.load_weights(model)
		return model

	def load_ssd300(self):
		print('loading SSD 300 ... ')
		img_shape = self.conf['IMG_SHAPE']
		classes = self.conf['CLASSES']
		swap_channels = [2, 1, 0] # The color channel order in the original SSD is BGR, so we'll have the model reverse the color channel order of the input images.
		n_classes = len(classes)
		scales_pascal = [0.1, 0.2, 0.37, 0.54, 0.71, 0.88, 1.05] # The anchor box scaling factors used in the original SSD300 for the Pascal VOC datasets
		scales = scales_pascal
		aspect_ratios = [[1.0, 2.0, 0.5],
                     [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                     [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                     [1.0, 2.0, 0.5, 3.0, 1.0/3.0],
                     [1.0, 2.0, 0.5],
                     [1.0, 2.0, 0.5]] # The anchor box aspect ratios used in the original SSD300; the order matters
		steps = [8, 16, 32, 64, 100, 300] # The space between two adjacent anchor box center points for each predictor layer.
		two_boxes_for_ar1 = True
		mean_color=[123,117,104] #TODO : add this as a parameter
		offsets = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
		clip_boxes=False
		variances=[0.1, 0.1, 0.2, 0.2]
		normalize_coords=True
		batch_size = self.conf['BATCH_SIZE']

		model = ssd_300(image_size=tuple(img_shape),
						n_classes=20,
						mode='training',
						l2_regularization=0.0005,
						scales=scales,
						aspect_ratios_per_layer=aspect_ratios,
						two_boxes_for_ar1=two_boxes_for_ar1,
						steps=steps,
						offsets=offsets,
						clip_boxes=clip_boxes,
						variances=variances,
						normalize_coords=normalize_coords,
						subtract_mean=mean_color,
						swap_channels=swap_channels)
		self.load_weights(model)
		return model


	def compile_model(self):
		# Specific workflows :
		if self.conf['MODEL_TYPE']=="RCNN":
			return 0

		loss= self.get_loss()
		opt = self.get_optimizer()

		self.model.compile(loss = loss,
						optimizer = opt,
						# metrics =['accuracy']
						metrics =self.compil_options['METRICS']
						)
		# print(self.model.get_config())


	def get_loss(self):
		loss_conf = self.compil_options['LOSS']
		loss = Loss(loss_conf)
		if self.conf['MODEL_TYPE']=="SSD300":
			return loss.load_loss_function()
		return loss.load_loss_function(self.model)

	def get_optimizer(self):
		opt_conf = self.compil_options['OPT']
		opt = Optimizer(opt_conf)
		return opt.load_optimizer()

	def load_callbacks(self):
		callback_list=[]
		if 'CALLBACKS' in self.conf :
			callbacks = Callbacks(self.conf['CALLBACKS'])
			callbacks.load_callbacks()
			callback_list = callbacks.get_callbacks()
			self.callbacks=callback_list
			self.lr = callbacks.get_lr()

		return callback_list

	def get_callbacks(self):
		return self.callbacks

	def get_lr(self):
		return self.lr

	def check_conf(self):
		print('checking model configuration')
		# Check model type values :
		model_type = self.conf['MODEL_TYPE']
		assert model_type in ['SSD300','DENSE_MNIST','RCNN','CUSTOM'], 'Invalid MODEL_TYPE argument, check your configuration'
		if model_type is "SSD300":
			print('TODO : Check SDD300 model conf ')
		if model_type is "RCNN":
			print(' TODO : check RCNN model conf')
		if self.conf['TASK'] == "TRAIN" :
			for elem in ['LOSS','OPT','METRICS']:
				assert elem in self.compil_options, 'Configuration file do not have a {} argument in the model compilation part. Plase add one '.format(elem)
		# assert self.compil_options['LOSS']  in ['categorical_crossentropy'], 'Unknown loss. Please check your configuration file '
		# assert self.compil_options['OPT'] in ['adam','rmsprop'], 'Unknown optimizer. Please check your configuration file'
		#TODO : add assert for metrics
    	
	def mnist_model(self):
		(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
		network = Sequential()

		network.add(Dense(512, activation='relu', input_shape=(28 * 28,)))
		network.add(Dense(10, activation='softmax'))
		network.compile(optimizer='sgd',loss='categorical_crossentropy', metrics=['accuracy'])

		train_images = train_images.reshape((60000, 28 * 28))
		train_images = train_images.astype('float32') / 255

		test_images = test_images.reshape((10000, 28 * 28))
		test_images = test_images.astype('float32') / 255

		train_labels = to_categorical(train_labels)
		test_labels = to_categorical(test_labels)

		hist = network.fit(train_images, train_labels, epochs=5, batch_size=128, validation_split=.1)
			
		return hist