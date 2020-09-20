import json_utils as jsu
from mrcnn import visualize
from matplotlib import pyplot as plt
import numpy as np
import colorsys
import os
import sys
import cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), 'utils'))


class VisualizationInstance:

	def __init__(self, conf=None):
		self.conf = conf
		self.check_conf()

	def check_annotations(self):
		datas_conf = self.conf['DATAS']
		if datas_conf['LABEL_FORMAT'] == 'VIA_JSON':
			annotation = jsu.json.load(
			    open(os.path.join(datas_conf['DATA_PATH'], datas_conf['LABEL_NAME'])))
			jsu.display_from_annotation(annotation,
										images_dir=datas_conf['DATA_PATH'],
										resize=[800, 800],
										ext='tif')
			print('TODO : afficher les annotaqtions via ')

	def show_lr(self, lr, epochs):
		N = np.arange(0, epochs)
		if lr.load_schedule() is not None:
			lr.load_schedule().plot(N)
			plt.show()

	def show_cyclic_lr(self, lr):
		N = np.arange(0, len(lr.load_lr().history["lr"]))
		plt.figure()
		plt.plot(N, lr.load_lr().history["lr"])
		plt.title("Cyclical Learning Rate (CLR)")
		plt.xlabel("Training Iterations")
		plt.ylabel("Learning Rate")
		plt.show()

	def show_pred_rcnn(self, r, img):
		hsv = [(i / 2, 1, 1.0) for i in range(len(self.conf['CLASSES']))]
		colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
		classes = self.conf['CLASSES']
		for i in range(0, len(r["scores"])):
			(startY, startX, endY, endX) = r["rois"][i]
			classID = r['class_ids'][i]
			label = classes[classID]
			score = r['scores'][i]
			color = colors[classID]

			cv2.rectangle(img, (startX, startY), (endX, endY), color, 2)
			text = "{} : {:.3f}".format(label, score)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			# cv2.putText(img,text,(startX,y), cv2.FONT_HERSHEY_SIMPLEX,
			# 0.6,color,2)

		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		for i in range(0, r["rois"].shape[0]):
			classID = r['class_ids'][i]
			mask = r['masks'][:, :, i]
			color = colors[classID]

			img = visualize.apply_mask(img, mask, color, alpha=0.5)

		target_size = self.conf['OUTPUT_VIZU_SIZE']
		img = cv2.resize(img, (target_size[0], target_size[1]))
		cv2.imshow("Output image", img)
		cv2.waitKey()

	def show_pred_ssd(self, preds, img):

		# Set the colors for the bounding boxes
		classes = self.conf['CLASSES']
		colors = plt.cm.hsv(np.linspace(0, 1, len(classes))).tolist()
		img_height = self.conf['TARGET_SIZE'][0]
		img_width = self.conf['TARGET_SIZE'][1]
		plt.figure(figsize=(20, 12))
		plt.imshow(img)
		current_axis = plt.gca()

		for box in preds[0]:
			# Transform the predicted bounding boxes for the 300x300 image to the original image dimensions.
			xmin = box[2] * img.shape[1] / img_width
			ymin = box[3] * img.shape[0] / img_height
			xmax = box[4] * img.shape[1] / img_width
			ymax = box[5] * img.shape[0] / img_height
			color = colors[int(box[0])]
			label = '{}: {:.2f}'.format(classes[int(box[0])], box[1])
			current_axis.add_patch(plt.Rectangle(
			    (xmin, ymin), xmax-xmin, ymax-ymin, color=color, fill=False, linewidth=2))
			current_axis.text(xmin, ymin, label, size='x-large',
			                  color='white', bbox={'facecolor': color, 'alpha': 1.0})
		plt.show()

	def show_pred_folder_ssd(self, preds, imgs):
		classes = self.conf['CLASSES']
		colors = plt.cm.hsv(np.linspace(0, 1, len(classes))).tolist()
		img_height = self.conf['TARGET_SIZE'][0]
		img_width = self.conf['TARGET_SIZE'][1]

		for i in range(len(imgs)):
			if(len(preds[i]) != 0):
				img = imgs[i]
				plt.figure(figsize=(20, 12))
				plt.imshow(imgs[i])
				current_axis = plt.gca()
				for box in preds[i]:
					# Transform the predicted bounding boxes for the 300x300 image to the original image dimensions.
					xmin = box[2] * img.shape[1] / img_width
					ymin = box[3] * img.shape[0] / img_height
					xmax = box[4] * img.shape[1] / img_width
					ymax = box[5] * img.shape[0] / img_height
					color = colors[int(box[0])]
					label = '{}: {:.2f}'.format(classes[int(box[0])], box[1])
					current_axis.add_patch(plt.Rectangle(
					    (xmin, ymin), xmax-xmin, ymax-ymin, color=color, fill=False, linewidth=2))
					current_axis.text(xmin, ymin, label, size='x-large',
					                  color='white', bbox={'facecolor': color, 'alpha': 1.0})
				plt.show()

	def check_conf(self):
		print(' TODOd : check visualisation conf ')

	def close(self):
		del self

	def display_train_val(self, hist):   
		#Accuracy Model Graph           
		plt.plot(hist.history['accuracy'])
		plt.plot(hist.history['val_accuracy'])

		plt.title('Model accuracy')

		plt.ylabel('Accuracy')
		plt.xlabel('Epoch')

		plt.legend(['Train', 'Val'], loc='lower right')

		plt.savefig('/home/ibson/Documents/plateforme_deep_learning/static/images/mnistaccuracy.png', dpi=100)

		plt.clf()
         
		#Loss Model Graphe
		plt.plot(hist.history['loss'])
		plt.plot(hist.history['val_loss'])
			
		plt.title('Model loss')
			
		plt.ylabel('Loss')
		plt.xlabel('Epoch')
			
		plt.legend(['Train', 'Val'], loc='lower right')

		plt.savefig('/home/ibson/Documents/plateforme_deep_learning/static/images/mnistloss.png', dpi=100)
