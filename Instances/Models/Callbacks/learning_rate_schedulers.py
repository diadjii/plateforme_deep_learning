# import the necessary packages
import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import *
import sys,os

sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),'utils'))
from generic_utils import launch_func

class LearningRateCustomScheduler():
	"""
	This class implements customs learning rates, callable via a valid configuration.
	It is inspired from various source,such as :
	- Leslie Smith in his 2015 paper, Cyclical Learning Rates for Training Neural Networks.
	- Adrian Rosebrock from his blog pyimagesearch (https://www.pyimagesearch.com/2019/07/29/cyclical-learning-rates-with-keras-and-deep-learning/)
	- Brad Kenstler for his implementation of cyclic LR. (https://github.com/bckenstler/CLR)

	LR scheduler is initialized via a configuration (dictionnary) composed of
	the following mandatory keys :
	"TYPE" : type of LR scheduler. Authorized values are LR_DECAY and CYCLIC_LR
	"SCHEDULE" : type of schedule. Authorized values are STEP, LINEAR ,POLY and NONE
	Other keys are not shared by all configurations and are explained below
	"""
	def __init__(self,config):
		self.check_config(config)
		self.type = config['TYPE']
		self.lr=None
		self.schedule=None
		if self.type == "CYCLIC_LR":
			"""
			Cyclic Learning rate is to be loaded
			The LR scheduler is initialized via a configuration (dictionnary)
			composed of the following optionnal keys :

			BASE_LR : initial learning rate which is the lower boundary in
				the cycle.
			MAX_LR : upper boundary in the cycle.
			STEP_SIZE : number of iterations per hal cycle

			To know more about this, refer to the CyclicLR class below.
			"""
			print("[INFO] using 'cycling' learning rate ...")
			self.lr = CyclicLR(config)
			# CyclicLR(
			# 	base_lr = config['base_lr'],
			# 	max_lr = config['max_lr'],
			# 	step_size = config['step_size'],
			# 	# gamma = config['gamma'],
			# 	# scale_fn = config['scale_fn'],
			# 	# scale_mode = config['scale_mode'],
			# 	mode = config['mode']
			# )
		if self.type == "LR_DECAY":
			 # check to see if step-based learning rate decay should be used
			if config["SCHEDULE"] == "STEP":
				"""
				Step scheduled learning rate is to be loaded
				The LR scheduler is initialized via a configuration (dictionnary)
				composed of the following mandatory keys :

				INIT_ALPHA : initial learning rate which is the top boundary
				FACTOR : factor by which the initial lr is multiplied ; should be <1
				DROP_EVERY : number of epochs before dropping the lr

				To know more about this, refer to the StepDecay class below.
				"""
				print("[INFO] using 'step-based' learning rate decay...")
				self.schedule = StepDecay(config)
				# self.schedule = StepDecay(
				# 	initAlpha=config['init_alpha'],
				# 	factor=config['factor'],
				# 	dropEvery=config['drop_every'])

			# check to see if linear learning rate decay should should be used
			elif config["SCHEDULE"] == "LINEAR":
				"""
				linear scheduled learning rate is to be loaded
				The LR scheduler is initialized via a configuration (dictionnary)
				composed of the following mandatory keys :

				INIT_ALPHA : initial learning rate which is the top boundary
				MAX_EPOCHS : maximum of epochs the model should be trained

				To know more about this, refer to the PolynomialDecay class below.
				"""
				print("[INFO] using 'linear' learning rate decay...")
				config['POWER']=1
				self.schedule = PolynomialDecay(config)
				# self.schedule = PolynomialDecay(
				# 	maxEpochs=config['MAX_EPOCHS'],
				# 	initAlpha=config['INIT_ALPHA'],
				# 	power=1)

			 # check to see if a polynomial learning rate decay should be used
			elif config["SCHEDULE"] == "POLY":
				"""
				polynomial scheduled learning rate is to be loaded
				The LR scheduler is initialized via a configuration (dictionnary)
				composed of the following optionnal keys :

				INIT_ALPHA : initial learning rate which is the top boundary
				MAX_EPOCHS : maximum of epochs the model should be trained
				POWER : power by which the lr is decaying. 1 would result in
					linear decay

				To know more about this, refer to the PolynomialDecay class below.
				"""
				print("[INFO] using 'polynomial' learning rate decay...")
				self.schedule = PolynomialDecay(config)
				# self.schedule = PolynomialDecay(
				# 	maxEpochs=config['epochs'],
				# 	initAlpha=config['init_alpha'],
				# 	power=config['power'])

			if self.schedule is not None:
				self.lr = LearningRateScheduler(self.schedule)
			else :
				print('TODO : add ERROR HERE : bad value for schedule parameter ')

	def load_lr(self):
		return self.lr

	def load_schedule(self):
		return self.schedule

	def check_config(self,config):
		print('TODO : chck config LR ')
		for i in ['SCHEDULE','TYPE'] :
			assert i in config, " CONFIGURATION ERROR FOR LR_SCHEDULER : {} should be added to the configuration file".format(i)
		assert config['SCHEDULE'] in ['STEP','LINEAR','POLY','NONE'], "CONFIGURATINO ERROR FOR LR_SCHEDULER : bad SCHEDULER value "
		assert config['TYPE'] in ['CYCLIC_LR', 'LR_DECAY'],"CONFIGURATINO ERROR FOR LR_SCHEDULER : bad TYPE value "

class LearningRateDecay:
	def plot(self, epochs, title="Learning Rate Schedule"):
		# compute the set of learning rates for each corresponding
		# epoch
		lrs = [self(i) for i in epochs]

		# the learning rate schedule
		plt.style.use("ggplot")
		plt.figure()
		plt.plot(epochs, lrs)
		plt.title(title)
		plt.xlabel("Epoch #")
		plt.ylabel("Learning Rate")

class StepDecay(LearningRateDecay):
	# def __init__(self, initAlpha=0.01, factor=0.25, dropEvery=10):
	# 	# store the base initial learning rate, drop factor, and
	# 	# epochs to drop every
	# 	self.initAlpha = initAlpha
	# 	self.factor = factor
	# 	self.dropEvery = dropEvery

	def __init__(self, config):
		# store the base initial learning rate, drop factor, and
		# epochs to drop every
		self.check_config(config)
		self.initAlpha = config['INIT_ALPHA']
		self.factor = config['FACTOR']
		self.dropEvery = config['DROP_EVERY']

	def __call__(self, epoch):
		# compute the learning rate for the current epoch
		exp = np.floor((1 + epoch) / self.dropEvery)
		alpha = self.initAlpha * (self.factor ** exp)

		# return the learning rate
		return float(alpha)

	def check_config(self,config):
		for i in ['INIT_ALPHA','FACTOR','DROP_EVERY']:
			assert i in config, "Missing parameter {} in configuration at LR_SCHEDULER level".format(i)

class PolynomialDecay(LearningRateDecay):
	# def __init__(self, MAX_EPOCHS=100, INIT_ALPHA=0.01, power=1.0):
	# 	# store the maximum number of epochs, base learning rate,
	# 	# and power of the polynomial
	# 	self.maxEpochs = MAX_EPOCHS
	# 	self.initAlpha = INIT_ALPHA
	# 	self.power = power
	def __init__(self, config):
		# store the maximum number of epochs, base learning rate,
		# and power of the polynomial
		self.check_conf(config)
		self.maxEpochs = config['MAX_EPOCHS']
		self.initAlpha = config['INIT_ALPHA']
		self.power = config['POWER']

	def __call__(self, epoch):
		# compute the new learning rate based on polynomial decay
		decay = (1 - (epoch / float(self.maxEpochs))) ** self.power
		alpha = self.initAlpha * decay

		# return the new learning rate
		return float(alpha)

	def check_conf(self,config):
		for i in ['MAX_EPOCHS','INIT_ALPHA','POWER']:
			assert i in config,"Missing parameter {} in configuration at LR_SCHEDULER level ".format(i)


class CyclicLR(Callback):
    """This callback implements a cyclical learning rate policy (CLR).
    The method cycles the learning rate between two boundaries with
    some constant frequency, as detailed in this paper (https://arxiv.org/abs/1506.01186).
    The amplitude of the cycle can be scaled on a per-iteration or
    per-cycle basis.
    This class has three built-in policies, as put forth in the paper.
    "triangular":
        A basic triangular cycle w/ no amplitude scaling.
    "triangular2":
        A basic triangular cycle that scales initial amplitude by half each cycle.
    "exp_range":
        A cycle that scales initial amplitude by gamma**(cycle iterations) at each
        cycle iteration.
    For more detail, please see paper.

    # Example
        ```python
            clr = CyclicLR(base_lr=0.001, max_lr=0.006,
                                step_size=2000., mode='triangular')
            model.fit(X_train, Y_train, callbacks=[clr])
        ```

    Class also supports custom scaling functions:
        ```python
            clr_fn = lambda x: 0.5*(1+np.sin(x*np.pi/2.))
            clr = CyclicLR(base_lr=0.001, max_lr=0.006,
                                step_size=2000., scale_fn=clr_fn,
                                scale_mode='cycle')
            model.fit(X_train, Y_train, callbacks=[clr])
        ```
    # Arguments
        base_lr: initial learning rate which is the
            lower boundary in the cycle.
        max_lr: upper boundary in the cycle. Functionally,
            it defines the cycle amplitude (max_lr - base_lr).
            The lr at any cycle is the sum of base_lr
            and some scaling of the amplitude; therefore
            max_lr may not actually be reached depending on
            scaling function.
        step_size: number of training iterations per
            half cycle. Authors suggest setting step_size
            2-8 x training iterations in epoch.
        mode: one of {triangular, triangular2, exp_range}.
            Default 'triangular'.
            Values correspond to policies detailed above.
            If scale_fn is not None, this argument is ignored.
        gamma: constant in 'exp_range' scaling function:
            gamma**(cycle iterations)
        scale_fn: Custom scaling policy defined by a single
            argument lambda function, where
            0 <= scale_fn(x) <= 1 for all x >= 0.
            mode paramater is ignored
        scale_mode: {'cycle', 'iterations'}.
            Defines whether scale_fn is evaluated on
            cycle number or cycle iterations (training
            iterations since start of cycle). Default is 'cycle'.

			All credits goes to bckenstler, see more at https://github.com/bckenstler
    """

    # def __init__(self, base_lr=0.001, max_lr=0.006, step_size=2000., mode='triangular',
    #              gamma=1., scale_fn=None, scale_mode='cycle'):
    #     super(CyclicLR, self).__init__()
	#
    #     self.base_lr = base_lr
    #     self.max_lr = max_lr
    #     self.step_size = step_size
    #     self.mode = mode
    #     self.gamma = gamma
    #     if scale_fn == None:
    #         if self.mode == 'triangular':
    #             self.scale_fn = lambda x: 1.
    #             self.scale_mode = 'cycle'
    #         elif self.mode == 'triangular2':
    #             self.scale_fn = lambda x: 1/(2.**(x-1))
    #             self.scale_mode = 'cycle'
    #         elif self.mode == 'exp_range':
    #             self.scale_fn = lambda x: gamma**(x)
    #             self.scale_mode = 'iterations'
    #     else:
    #         self.scale_fn = scale_fn
    #         self.scale_mode = scale_mode
    #     self.clr_iterations = 0.
    #     self.trn_iterations = 0.
    #     self.history = {}
	#
    #     self._reset()

    def __init__(self, config):
        super(CyclicLR, self).__init__()

        base_lr = config['BASE_LR']
        max_lr = config['MAX_LR']
        step_size = config['STEP_SIZE']
        mode = config['MODE']
        gamma = 1.
        scale_fn = None
        scale_mode='cycle'
        #TODO : allow the 3 last parameters in config
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size = step_size
        self.mode = mode
        self.gamma = gamma
        if scale_fn == None:
            if self.mode == 'triangular':
                self.scale_fn = lambda x: 1.
                self.scale_mode = 'cycle'
            elif self.mode == 'triangular2':
                self.scale_fn = lambda x: 1/(2.**(x-1))
                self.scale_mode = 'cycle'
            elif self.mode == 'exp_range':
                self.scale_fn = lambda x: gamma**(x)
                self.scale_mode = 'iterations'
        else:
            self.scale_fn = scale_fn
            self.scale_mode = scale_mode
        self.clr_iterations = 0.
        self.trn_iterations = 0.
        self.history = {}

        self._reset()


    def _reset(self, new_base_lr=None, new_max_lr=None,
               new_step_size=None):
        """Resets cycle iterations.
        Optional boundary/step size adjustment.
        """
        if new_base_lr != None:
            self.base_lr = new_base_lr
        if new_max_lr != None:
            self.max_lr = new_max_lr
        if new_step_size != None:
            self.step_size = new_step_size
        self.clr_iterations = 0.

    def clr(self):
        cycle = np.floor(1+self.clr_iterations/(2*self.step_size))
        x = np.abs(self.clr_iterations/self.step_size - 2*cycle + 1)
        if self.scale_mode == 'cycle':
            return self.base_lr + (self.max_lr-self.base_lr)*np.maximum(0, (1-x))*self.scale_fn(cycle)
        else:
            return self.base_lr + (self.max_lr-self.base_lr)*np.maximum(0, (1-x))*self.scale_fn(self.clr_iterations)

    def on_train_begin(self, logs={}):
        logs = logs or {}

        if self.clr_iterations == 0:
            K.set_value(self.model.optimizer.lr, self.base_lr)
        else:
            K.set_value(self.model.optimizer.lr, self.clr())

    def on_batch_end(self, epoch, logs=None):

        logs = logs or {}
        self.trn_iterations += 1
        self.clr_iterations += 1

        self.history.setdefault('lr', []).append(K.get_value(self.model.optimizer.lr))
        self.history.setdefault('iterations', []).append(self.trn_iterations)

        for k, v in logs.items():
            self.history.setdefault(k, []).append(v)

        K.set_value(self.model.optimizer.lr, self.clr())
