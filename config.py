import os, json

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, 'static', 'config.json')

def init_params():
    config_params = {}

    config_params['configuration'] = {}

    config_params['configuration']['DATAS'] = {
        "DATA_FORMAT" : "KERAS",
    	"DATA_FEED" : "KERAS_DATASET",
    	"DATA_PATH" : "MNIST",
    	"DATA_TYPE" : "IMG",
    	"RESHAPE" : "True"
    }
    config_params['configuration']['TASK'] = {
    	"TASK_NAME" : "TRAIN",
    	"TASK_SPEC" : {
    	    "EPOCHS" : 12,
    	    "BATCH_SIZE" : 128
    	}
    }
    config_params['configuration']['MODEL'] = {
        "MODEL_TYPE" : "DENSE_MNIST",
    	"WEIGHTS_PATH" : "KERAS_EASY",
    	"TASK" : "TRAIN",
    	"COMPILATION" : {
    		"LOSS" : {
    			"NAME" : "categorical_crossentropy"
    		},
    		"OPT" : {
    			"NAME" : "rmsprop"
    		},
    		"METRICS" : ["accuracy"]
    	}
    }
    config_params['configuration']['OUTPUT'] = {
        "SAVE_MODE" : "ALL",
    	"OUTPUT_PATH" : "EXAMPLE_ARCHITECTURE",
    	"OUTPUT_NAME" : "dense_mnist.h5"
    }

    with open(json_url,'w') as json_file:
        json.dump(config_params, json_file, indent=2)

init_params()
