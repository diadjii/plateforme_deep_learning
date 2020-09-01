# This is he main script for the Supervised Learning Platform
# This script will handle the configuration validation and
# launch the adequate runs to be launched.
#
#

import os
import sys
from colorama import Fore
from colorama import Style

#Previous implementations were made to be executed in the src folder so let's put our execution path there
# sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

##################
## GET ARGUMENTS
##################
from Configurations.configuration import Configuration
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--configuration", required=True,
	help="name of the configuration file that will be processed ")
args = vars(ap.parse_args())

conf = Configuration(args['configuration'])

##################
## TRAINING
##################
from Instances.Training.train import TrainingInstance
from Instances.Inference.inference import InferenceInstance
from Instances.Visualization.visualization import VisualizationInstance

task_name = conf.dic['TASK']['TASK_NAME']

if task_name=='TRAIN':
	ti = TrainingInstance(conf.dic)
	ti.start_training()
	ti.close()
if task_name=='INFERENCE':
	ei = InferenceInstance(conf.dic)
	data_type = conf.dic['TASK']['TASK_SPEC']['DATA_TYPE']
	if data_type == "IMAGE":
		ei.inference_on_image()
	elif data_type == "IMAGE_FOLDER":
		ei.inference_on_folder()
	ei.close()
if task_name=='FIND_LR':
	ti = TrainingInstance(conf.dic)
	ti.find_lr()
	ti.close()
if task_name == 'CHECK_ANNOTATIONS':
	vi = VisualizationInstance(conf.dic)
	vi.check_annotations()
	vi.close()
