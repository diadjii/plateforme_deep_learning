import cv2
import os, sys
import numpy as np
from imageio import imread

from keras.models import load_model
from keras.preprocessing import image

sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Datas.datas import DataInstance
from Models.model_instance import ModelInstance
from Visualization.visualization import VisualizationInstance
from Datas.ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast

class InferenceInstance:

	def __init__(self,conf):
		self.parse_conf(conf)
		self.model_instance = self.load_model_instance(conf['MODEL'])

	def parse_conf(self,conf):
		assert conf is not None, 'provided infertence configuration is invalid'
		self.conf= conf
		self.check_conf()

	def close(self):
		del self

	def load_model_instance(self,conf):
		model_instance = ModelInstance(conf)
		model_instance.load_model_from_weights()
		return model_instance

	def inference_on_image(self,img_path=None):

		task_info = self.conf['TASK']['TASK_SPEC']
		if img_path is None :
			img_path = self.conf['DATAS']['DATA_PATH']
		model_type = self.conf['MODEL']['MODEL_TYPE']

		if model_type == "RCNN":
			img = cv2.imread(img_path)
			r = self.model_instance.model.detect([img],verbose=1)[0]
			visu = VisualizationInstance(self.conf['DATAS'])
			visu.show_pred_rcnn(r,img)
		if model_type =="SSD300":
			orig_image = imread(img_path)
			img = image.load_img(img_path, target_size=tuple(task_info['TARGET_SIZE']))
			img = image.img_to_array(img)
			input_images = [img]
			input_images=np.array(input_images)

			model = self.model_instance.model
			y_pred = model.predict(input_images)
			confidence_threshold = task_info['CONFIDENCE_THRESH']
			y_pred_tresh = [y_pred[k][y_pred[k,:,1] > confidence_threshold] for k in range(y_pred.shape[0])]
			y_pred_decoded = decode_detections(y_pred,
												confidence_thresh = confidence_threshold,
												iou_threshold = task_info['IOU'],
												top_k = task_info['TOP_K'],
												normalize_coords = (task_info['NORM']=="True"),
												img_height = task_info['TARGET_SIZE'][0],
												img_width = task_info['TARGET_SIZE'][1])
			print('Predictions : ', y_pred_decoded)
			visu = VisualizationInstance(self.conf['DATAS'])
			visu.show_pred_ssd(y_pred_decoded,orig_image)

	def inference_on_folder(self):
		task_info=self.conf['TASK']['TASK_SPEC']
		folder_path = self.conf['DATAS']['DATA_PATH']
		model_type = self.conf['MODEL']['MODEL_TYPE']
		orig_images = []
		input_images=[]
		image_paths = []
		for root, dirs, files in os.walk(folder_path):
			for i,file in enumerate(files):
				#TODO : introduce batchs of datas here via generators
				if i >100 :
					break
				ext = file.split('.')[-1]
				if ext == "json":
					continue
				img_path = os.path.join(folder_path,file)
				if model_type == "RCNN":
					self.inference_on_image(img_path=img_path)
				if model_type=="SSD300":
					orig_images.append(imread(img_path))
					img = image.load_img(img_path,target_size = tuple(task_info['TARGET_SIZE']))
					img= image.img_to_array(img)
					input_images.append(img)

		if model_type =="SSD300" :
			input_images = np.array(input_images)
			model = self.model_instance.model
			y_pred = model.predict(input_images)
			confidence_threshold = task_info['CONFIDENCE_THRESH']
			y_pred_tresh = [y_pred[k][y_pred[k,:,1] > confidence_threshold] for k in range(y_pred.shape[0])]
			y_pred_decoded = decode_detections(y_pred,
												confidence_thresh = confidence_threshold,
												iou_threshold = task_info['IOU'],
												top_k = task_info['TOP_K'],
												normalize_coords = (task_info['NORM']=="True"),
												img_height = task_info['TARGET_SIZE'][0],
												img_width = task_info['TARGET_SIZE'][1]
												)

			visu = VisualizationInstance(self.conf['DATAS'])
			visu.show_pred_folder_ssd(y_pred_decoded,orig_images)


	def check_conf(self):
		print('TODO : check inference configuration in inferenceInstance class ')
