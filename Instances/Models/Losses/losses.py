import sys,os
from keras.losses import mean_squared_error as mse

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from keras_ssd_loss import SSDLoss

keras_losses = ['categorical_crossentropy',
				'mean_squared_error',
				'mean_absolute_error',
				'mean_absolute_percentage_error',
				'mean_squared_percentage_error',
				'mean_squared_logarithmic_error',
				'squared_hinge',
				'hinge',
				'categorical_hinge',
				'logcosh',
				'huber_loss',
				'categorical_crossentropy',
				'sparse_categorical_crossentropy',
				'binary_crossentropy',
				'kullback_leibler_divergence',
				'poisson',
				'cosine_proximity',
				'is_categorical_crossentropy',
				]

class Loss():

	def __init__(self,conf):
		self.conf=conf
		self.check_conf()

	def load_loss_function(self,model=None):
		name = self.conf['NAME']
		if name in keras_losses :
			loss = name
		else:
			loss_options = self.conf
			if name == "RCNN_LOSS":
				model.keras_model._losses = []
				model.keras_model._per_input_losses = {}
				loss_names = ["rpn_class_loss",
							  "rpn_bbox_loss",
							  "mrcnn_class_loss",
							  "mrcnn_bbox_loss",
							  "mrcnn_mask_loss"
							  ]
				for name in loss_names:
					layer = model.keras_model.get_layer(name)
					if layer.output in model.keras_model.losses:
						continue
					loss = (
					tf.reduce_mean(layer.output, keepdims=True)
					* model.config.LOSS_WEIGHTS.get(name,1)
					)
					model.keras_model.add_loss(loss)
			if name=="SSD_LOSS":
				loss = SSDLoss(neg_pos_ratio = loss_options['NPR'],
								alpha=loss_options['ALPHA'])
				loss = loss.compute_loss

		# print(' VERBOSE LOSS : ',loss)
		return loss


	def check_conf(self):
		print(' TODO : check loss configuration')
