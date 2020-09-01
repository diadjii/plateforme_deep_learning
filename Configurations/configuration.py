import pandas as pd

class Configuration:

	def __init__(self,path=None):
		self.dic={}
		self.errors = {}

		if path is not None:
			self.parse_json_conf(path)

	def parse_conf(self,conf):
		try:
			self.dic=conf.to_dict()['configuration']
			self.check_conf()
		except ValueError :
			self.errors['parsing_conf_error'] = ' Configuration file corrupted : ensure it is correctly formatted, i.E all the lines have the \'a:b\' format.'
			raise ValueError

	def parse_json_conf(self,path):
		try:
			df = pd.read_json(path)
			self.parse_conf(df)
		except ValueError :
			self.errors['parsing_json_error'] = 'FATAL ERROR : configuration file not found or invalid json \n'
			raise ValueError

	def check_conf(self):
		#Check all the paramaters of the configuration file here
		for elem in ['DATAS','TASK','MODEL']:#TODO : derive this list from config file
			assert elem in self.dic, 'Configuration file do not have a {} argument. Please add one'.format(elem)
		for elem in ['DATA_FORMAT','DATA_PATH','DATA_FEED','DATA_TYPE']:
			assert elem in self.dic['DATAS'], 'Configuration file is missing {} argument in the datas section. Please add one.'.format(elem)
		for elem in ['TASK_NAME','TASK_SPEC']:
			assert elem in self.dic['TASK'], 'Configuration file is missing {} argument in the task section. Please add one '.format(elem)
		for elem in ['MODEL_TYPE','WEIGHTS_PATH']:
			assert elem in self.dic['MODEL'], 'Configuration file is missing {} argument in the model section. Please add one.'.format(elem)
		print('TODO : complete configuration check_conf')
		#TODO : assert values for task, and others miscs 
