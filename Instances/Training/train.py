import json
import math
import os, sys
import numpy as np
from math import ceil
import matplotlib.pyplot as plt

sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Datas.datas import DataInstance
from Models.model_instance import ModelInstance
from Visualization.visualization import VisualizationInstance
from Training.utils.learningratefinder import LearningRateFinder

import keras
from keras.preprocessing.image import ImageDataGenerator

class TrainingInstance:

	def __init__(self,conf=None):
		self.conf = {}
		if conf is not None:
			self.parse_conf(conf)

	def parse_conf(self,conf):
		assert conf is not None, 'provided train configuration is invalid'
		self.conf=conf #TODO : use only need parameters

	def close(self):
		del self

	### TASK related
	def start_training(self,find_LR=False):
		print('Starting training instance')
		model_instance = self.load_model_instance(self.conf['MODEL'])
		data_instance = self.load_data_instance(self.conf['DATAS'])
		print('Launch training')
		history = self.launch_training(model_instance,data_instance,self.conf['MODEL'],find_LR)
		self.display(history,model_instance)
		self.write_ouputs(model_instance)

	def find_lr(self):
		self.start_training(find_LR=True)
	### Load related
	def load_data_instance(self,datas):
		data_instance = DataInstance(datas)
		return(data_instance)

	def load_model_instance(self,conf):
		model_instance = ModelInstance(conf)
		model_instance.load_model()
		return model_instance

	def compile_model(self,model_instance):
		model_instance.compile_model()
		# model_instance.model.summary()

	def launch_lr_finder(self,model,datas,options):
		print("[INFO] finding learning rate...")
		lrf = LearningRateFinder(model)
		for i in ['BASE_LR','MAX_LR']:
			assert i in options, " Missing {} parameter in TASK_SPEC ; mandatory to perform LR search ".format(i)
		batch_size = options['BATCH_SIZE']
		aug=ImageDataGenerator()
		trainX = datas[0]
		trainY = datas[1]
		if len(trainX.shape)==2:
			dims = int(math.sqrt(trainX.shape[1]))
			trainX = trainX.reshape(trainX.shape[0],dims,dims,1)
			# trainY = trainY	.reshape(trainY.shape[0],dims,dims,1)

		lrf.find(
			aug.flow(trainX,trainY,batch_size = batch_size),
			# datas[0],
			# datas[1],
			options['BASE_LR'],
			options['MAX_LR'],
			stepsPerEpoch=np.ceil((len(datas[0]) / float(batch_size))),
			batchSize = batch_size)
		lrf.plot_loss()
		# plt.savefig(os.path.join(file_path,"lr_find_plot.png"))
		plt.show()
		print("[INFO] learning rate finder complete")
		print("[INFO] examine plot and adjust learning rates before training")

	def launch_training(self,model_instance,data_instance,conf,find_LR=False):
		model = model_instance.model
		self.compile_model(model_instance)
		callbacks = model_instance.load_callbacks()

		options = self.conf['TASK']['TASK_SPEC']
		if data_instance.datas['DATA_FEED']=="KERAS_DATASET":
			datas = data_instance.load_keras_dataset(model_instance)
			if find_LR:
				###actual task is to find optionnal LR
				self.launch_lr_finder(model,datas,options)
				sys.exit(0)
			history = model.fit(
				datas[0],
				datas[1],
				callbacks=callbacks,
				epochs=options['EPOCHS'],
				batch_size=options['BATCH_SIZE'])
		if data_instance.datas['DATA_FEED']=='GENERATOR':
			generators = data_instance.load_generators(model_instance)
			batch_size=options['BATCH_SIZE']
			train = generators[0]
			val = generators[1]

			#RCNN matterport has its own workflow
			if self.conf['MODEL']['MODEL_TYPE']=="RCNN":
				model.train(train[0],val[0],
							learning_rate = model_instance.rcnnconf.LEARNING_RATE,
							epochs = options['EPOCHS'],
							layers='heads')
				return 0

			if "STEPS_PER_EPOCH" in options:
				steps_per_epoch = options['STEPS_PER_EPOCH']
			else :
				steps_per_epoch = ceil(train[1]/batch_size)
			model.summary()
			history = model.fit_generator(
										  generator = train[0],
										  steps_per_epoch = steps_per_epoch,
										  epochs=options['EPOCHS'],
										  callbacks = callbacks,
										  validation_data = val[0],
										  validation_steps = ceil(val[1]/batch_size)
			)
		return history


	def write_ouputs(self,model_instance):
		if "OUTPUT" not in self.conf :
			return 0
		output = self.conf['OUTPUT']
		save_mode = output['SAVE_MODE']

		if output['OUTPUT_PATH'] == "EXAMPLE_ARCHITECTURE":
			example_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Models","models","examples")
			model_path = os.path.join(example_path,output['OUTPUT_NAME'])
		else:
			model_path = os.path.join(output['OUTPUT_PATH'],output['OUTPUT_NAME'])
		if save_mode =="ALL":
			if self.conf['MODEL']['MODEL_TYPE'] == "RCNN":
				model_instance.model.keras_model.save(model_path)
			else :
				model_instance.model.save(model_path)
		if save_mode == "WEIGHTS_ONLY" :
			if self.conf['MODEL']['MODEL_TYPE'] == "RCNN":
				model_instance.model.keras_model.save_weights(model_path)
			else:
				model_instance.model.save_weights(model_path)
		if save_mode == "JSON" :
			if self.conf['MODEL']['MODEL_TYPE'] == "RCNN":
				json_model = model_instance.model.keras_model.to_json(model_path)
			else :
				json_model = model_instance.model.to_json()
			with open(model_path,'w') as f :
				json.dump(json_model,f,ensure_ascii=False)


	def display(self,history,model_instance):
		visu = VisualizationInstance(self.conf['DATAS'])

		## display LR
		lr = model_instance.get_lr()
		if lr is not None :
			print(type(lr))
			if lr.load_schedule() is not None:
				visu.show_lr(model_instance.get_lr(),self.conf['TASK']['TASK_SPEC']['EPOCHS'])
			else:
				visu.show_cyclic_lr(lr)

		print('TODO : display the history datas ')


