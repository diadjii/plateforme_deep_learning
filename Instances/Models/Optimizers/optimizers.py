from keras.optimizers import Adam, SGD

keras_optimizers=['sgd',
				  'rmsprop',
				  'adagrad',
				  'adadelta',
				  'adam',
				  'adamax',
				  'nadam'
				  ]

class Optimizer():

	def __init__(self,conf):
		self.conf=conf
		self.check_conf()

	def load_optimizer(self):
		name = self.conf['NAME']
		#Compute optimizer
		if name in keras_optimizers :
			opt = name
		else :
			opt_options = self.conf
			### SGD optimizer
			if opt_options['NAME']=="SGD":
				opt = SGD(lr=opt_options['LR'],
							momentum = opt_options['MOMENTUM'],
							decay = opt_options['DECAY'],
							nesterov=(opt_options['NESTEROV']=="True"))
		return opt

	def check_conf(self):
		print('TODO : check optimier conf')
