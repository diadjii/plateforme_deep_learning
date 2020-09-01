import sys,os
from keras.callbacks import ModelCheckpoint, EarlyStopping, LearningRateScheduler, TerminateOnNaN, CSVLogger,ReduceLROnPlateau
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from learning_rate_schedulers import LearningRateCustomScheduler

class Callbacks():
	"""
	This class implements callbacks, callable via a valid configuration.
	It is inspired from the keras callbacks ; see more at https://keras.io/api/callbacks/
	Any callback is initialized via a configuration (dictionnary) named after one
	of the implemented callbacks below.
	"""
#TODO : transcript so that we can launch these callbakcs without the need of all parameters
	def __init__(self,conf):
		self.conf = conf
		self.lr=None
		self.check_conf()

	def ssd_lr_schedule(epoch):
		if epoch <80 :
			return 0.001
		elif epoch < 100 :
			return 0.0001
		else :
			return 0.00001

	def load_callbacks(self):
		print('TODO : add parameter handling ')
		callbacks = self.conf
		callback_list = []
		if "CHECKPOINT" in callbacks:
			"""
			Get model checkpoint callback from keras (https://keras.io/api/callbacks/model_checkpoint/)
			Parameters are extracted from the given configuration
			"""
			checkpoint = callbacks['CHECKPOINT']
			model_checkpoint = ModelCheckpoint(filepath = checkpoint['PATH'],
												monitor = checkpoint['MONITOR'],
												verbose = checkpoint['VB'],
												save_best_only = checkpoint['BEST_ONLY'],
												save_weights_only = checkpoint['WEIGHTS_ONLY'],
												mode = checkpoint['MODE'],
												period = checkpoint['PERIOD'])
			callback_list.append(model_checkpoint)
		if "EARLY_STOPPING" in callbacks:
			"""
			Get early stopping callback from keras (https://keras.io/api/callbacks/early_stopping/)
			Parameters are extracted from the given configuration
			"""
			early_stop = callbacks['EARLY_STOPPING']
			early_stopping = EarlyStopping(monitor = early_stop['MONITOR'],
											min_delta = early_stop['MIN_DELTA'],
											patience = early_stop['PATIENCE'],
											verbose = early_stop['VB'])
			callback_list.append(early_stopping)
		if "LR_SCHEDULER" in callbacks:
			"""
			Get lr scheduler callback defined by the SCHEDULE parameter.
			See learning_rate_schedulers.py file for more details
			Parameters are extracted from the given configuration
			"""
			lr_schedule = callbacks['LR_SCHEDULER']
			if lr_schedule['SCHEDULE']=="ssd_schedule":
				schedule = ssd_lr_schedule
				learning_rate_scheduler = LearningRateScheduler(schedule=schedule,
								verbose =lr_schedule['VB'])
			else:
				self.lr = LearningRateCustomScheduler(lr_schedule)
				learning_rate_scheduler=self.lr.load_lr()

			callback_list.append(learning_rate_scheduler)
		if "TERMINATE_NAN" in callbacks :
			"""
			Get terminate on nan callback from keras (https://keras.io/api/callbacks/terminate_on_nan/)
			Parameters are extracted from the given configuration
			"""
			terminate_on_nan = TerminateOnNaN()
			callback_list.append(terminate_on_nan)

		if "REDUCE_LR_ON_PLATEAU" in callbacks:
			"""
			Get ReduceLROnPlateau callback from keras (https://keras.io/api/callbacks/reduce_lr_on_plateau/)
			Parameters are extracted from the given configuration
			"""
			reduce = callbacks['REDUCE_LR_ON_PLATEAU']
			reduceLR = ReduceLROnPlateau(monitor = reduce['MONITOR'],
										 factor = reduce['FACTOR'],
										 patience = reduce['PATIENCE'],
										 min_lr = reduce['MIN_LR'])
			callback_list.append(reduceLR)

		if "CSVLOGGER" in callbacks :
			"""
			Get CSVLogger callback from keras (https://keras.io/api/callbacks/csv_logger/)
			Parameters are extracted from the given configuration
			"""
			args = callbacks['CSVLOGGER']
			csv_logger = CSVLogger(filename = args['FILENAME'],
								   separator = args['SEP'],
								   append = args['APPEND'])
		self.callbacks = callback_list

	def get_callbacks(self):
		return self.callbacks

	def get_lr(self):
		return self.lr

	def check_conf(self):
		print(' TODO : check callbacks configuration ')
