import json
import os,sys
import skimage.draw
import numpy as np
from keras.datasets import mnist, cifar10, cifar100, imdb, reuters, fashion_mnist, boston_housing
from keras.utils import to_categorical

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from data_generator.object_detection_2d_photometric_ops import ConvertTo3Channels
from data_generator.object_detection_2d_data_generator import DataGenerator
from data_generator.object_detection_2d_geometric_ops import Resize
from ssd_encoder_decoder.ssd_input_encoder import SSDInputEncoder
from mrcnn import model as modellib, utils

sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'utils'))
from generic_utils import launch_func


class GENDataset(utils.Dataset):
	#Class for dataset generated from folders.

	def set(self,conf):
		self.conf=conf

	def load_annotations(self,dataset_dir):
		label_format = self.conf['LABEL_FORMAT']
		if label_format == "VIA_JSON":
			annotations = json.load(open(os.path.join(dataset_dir,self.conf['LABEL_NAME'])))
			annotations = list(annotations.values())
			annotations = [a for a in annotations if a['regions']]

			for a in annotations :
				if type(a['regions']) is dict:
					polygons = [r['shape_attributes'] for r in a['regions'].values()]
				else:
					polygons = [r['shape_attributes'] for r in a['regions']]

				image_path = os.path.join(dataset_dir,a['filename'])
				image = skimage.io.imread(image_path)
				height,width = image.shape[:2]

				self.add_image("class",
							   image_id = a['filename'],
							   path = image_path,
							   width = width,
							   height = height,
							   polygons = polygons
				)
			print('TODO : check we have the right data count : ', len(annotations))
			return len(annotations)


	def load_subset(self,subset):

		for i,elem in enumerate(self.conf['CLASSES']):
			#class numer 0 should be the Background
			if i==0:
				continue

			self.add_class("class",i,elem)


		assert subset in ['train','val','test']
		dataset_dir = os.path.join(self.conf['DATA_PATH'],subset)
		return self.load_annotations(dataset_dir)

	def load_generator(self,subset,conf):
		dataset_size = self.load_subset(subset)
		self.prepare()

		##Using a trick here : loading the class instead of trhe generators to respect matterport worklow

		# generator_options=self.conf['GENERATOR']
		# generator = modellib.data_generator(self,
		# 									conf,
		# 									shuffle=True,
		# 									batch_size=generator_options['BATCH_SIZE'])
		# return (generator,dataset_size)
		return (self,dataset_size)


	def load_mask(self, image_id):
		#TODO : add other ways than via annotation
		image_info = self.image_info[image_id]
		if image_info["source"] != "class":
			return super(self.__class__, self).load_mask(image_id)

		info = self.image_info[image_id]
		mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
						dtype=np.uint8)
		for i, p in enumerate(info["polygons"]):
			rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
			try :
				mask[rr, cc, i] = 1
			except IndexError:
				print('Caught and index error with values : {},{} for a width of {} and a height of {}'.format(rr,cc,info["width"],info["height"]))
				continue
		return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)


	def check_conf(self):
		print ('TODO : check GEN Dataset config ')


keras_datasets = ['MNIST',
				  'CIFAR10',
				  'CIFAR100',
				  'IMDB',
				  'REUTERS',
				  'BOSTON_HOUSING']

class DataInstance:

	def __init__(self,data):
		self.datas=data
		self.train_generator=None
		self.val_generator = None
		self.test_generator = None
		self.check_conf()

	def load_keras_dataset(self,model_instance):
		data_info = self.datas
		dataset_name = data_info['DATA_PATH']
		load_data_func = globals()[dataset_name.lower()].load_data
		(x_train,y_train),(x_test,y_test)=launch_func(load_data_func,data_info)
		if data_info['RESHAPE']=="True":
			x_train = x_train.astype('float32')/255
			x_test = x_test.astype('float32')/255
			y_train = to_categorical(y_train)
			y_test = to_categorical(y_test)
			if dataset_name=="MNIST":
				x_train= x_train.reshape((60000,28*28))
				x_test = x_test.reshape((10000,28*28))
		return[x_train,y_train,x_test,y_test]

	def load_generators(self, model_instance):
		if self.datas['DATA_FORMAT'] == "GEN":
			self.check_GEN_format(self.datas['DATA_PATH'])
			if self.datas['DATA_TYPE'] == "IMG":
				return self.load_GEN_IMG_generators(model_instance)

		if self.datas['DATA_FORMAT'] == "VOC":
			self.check_VOC_format(self.datas['DATA_PATH'])
			if self.datas['DATA_TYPE'] == "IMG":
				return self.load_VOC_IMG_generators(model_instance.model)

		return 0

	def load_GEN_IMG_generators(self,model_instance):
		train_dataset = GENDataset()
		train_dataset.set(self.datas)
		train_generator, train_size = train_dataset.load_generator('train',model_instance.rcnnconf)

		val_dataset = GENDataset()
		val_dataset.set(self.datas)
		val_generator, val_size = val_dataset.load_generator('val',model_instance.rcnnconf)

		return [train_generator,train_size],[val_generator,val_size]

	def load_VOC_IMG_generators(self,model):
		print('Making VOC image generators')
		datadir = self.datas['DATA_PATH']
		train_dataset = DataGenerator(load_images_into_memory=False, hdf5_dataset_path=None)
		val_dataset = DataGenerator(load_images_into_memory=False, hdf5_dataset_path=None)
		test_dataset = DataGenerator(load_images_into_memory=False, hdf5_dataset_path=None)
		images_dir                   = os.path.join(datadir,'Images')
		annotations_dir              = os.path.join(datadir,'Annotations')
		train_image_set_filename  = os.path.join(datadir,'ImageSets','train.txt')
		val_image_set_filename      = os.path.join(datadir,'ImageSets','val.txt')
		test_image_set_filename      = os.path.join(datadir,'ImageSets','test.txt')
		generator_options = self.datas['GENERATOR']

		train_dataset.parse_xml(images_dirs=[images_dir],
		                        image_set_filenames=[train_image_set_filename],
		                        annotations_dirs=[annotations_dir],
		                        classes=self.datas['CLASSES'],
		                        include_classes='all',
		                        exclude_truncated=False,
		                        exclude_difficult=False,
		                        ret=False)
		val_dataset.parse_xml(images_dirs=[images_dir],
		                        image_set_filenames=[val_image_set_filename],
		                        annotations_dirs=[annotations_dir],
		                        classes=self.datas['CLASSES'],
		                        include_classes='all',
		                        exclude_truncated=False,
		                        exclude_difficult=False,
		                        ret=False)
		test_dataset.parse_xml(images_dirs=[images_dir],
		                        image_set_filenames=[test_image_set_filename],
		                        annotations_dirs=[annotations_dir],
		                        classes=self.datas['CLASSES'],
		                        include_classes='all',
		                        exclude_truncated=False,
		                        exclude_difficult=False,
		                        ret=False)

		convert_to_3_channels = ConvertTo3Channels()
		target_size = generator_options['TARGET_SIZE']
		resize = Resize(height=target_size[0], width=target_size[1])

		predictor_sizes = [model.get_layer('conv4_3_norm_mbox_conf').output_shape[1:3],
	                       model.get_layer('fc7_mbox_conf').output_shape[1:3],
	                       model.get_layer('conv6_2_mbox_conf').output_shape[1:3],
	                       model.get_layer('conv7_2_mbox_conf').output_shape[1:3],
	                       model.get_layer('conv8_2_mbox_conf').output_shape[1:3],
	                       model.get_layer('conv9_2_mbox_conf').output_shape[1:3]]
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

		ssd_input_encoder = SSDInputEncoder(img_height = target_size[0],
											img_width = target_size[1],
											n_classes = 20, #TODO : handle subsampling
											predictor_sizes=predictor_sizes,
											scales=scales,
											aspect_ratios_per_layer=aspect_ratios,
											two_boxes_for_ar1=two_boxes_for_ar1,
											steps=steps,
											offsets=offsets,
											clip_boxes=clip_boxes,
											variances=variances,
											matching_type='multi',
											pos_iou_threshold=0.5,
											neg_iou_limit=0.5,
											normalize_coords=normalize_coords
											)
		train_generator = train_dataset.generate(batch_size=generator_options['BATCH_SIZE'],
												shuffle=True,
												transformations=[convert_to_3_channels,
																resize],
												label_encoder=ssd_input_encoder,
												returns={'processed_images',
														 'encoded_labels'},
												keep_images_without_gt=False)

		val_generator = val_dataset.generate(batch_size=generator_options['BATCH_SIZE'],
												shuffle=True,
												transformations=[convert_to_3_channels,
																resize],
												label_encoder=ssd_input_encoder,
												returns={'processed_images',
														 'encoded_labels'},
												keep_images_without_gt=False)

		test_generator = test_dataset.generate(batch_size=generator_options['BATCH_SIZE'],
												shuffle=True,
												transformations=[convert_to_3_channels,
																resize],
												label_encoder=ssd_input_encoder,
												returns={'processed_images',
														 'encoded_labels'},
												keep_images_without_gt=False)
		return [train_generator,train_dataset.get_dataset_size()],[val_generator,val_dataset.get_dataset_size()],[test_generator,train_dataset.get_dataset_size()]



	def check_GEN_format(self,path):
		print('TODO : check_GEN_format in datas.py')

	def check_VOC_format(self,path):
		print('TODO : check_VOC_format  in datas.py')

	def check_conf(self):
		assert self.datas['DATA_FORMAT'] in ['GEN','VOC','KERAS'], 'Invalid DATA_FORMAT, check your configuration file'
		assert self.datas['DATA_FEED'] in ['GENERATOR','KERAS_DATASET',"IMG"], 'Invalid DATA_FEED, check your configuration file'
		assert self.datas['DATA_TYPE'] in ['IMG'], 'Invalid DATA_TYPE, check your configuration file'
