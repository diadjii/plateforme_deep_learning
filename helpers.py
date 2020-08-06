import os
import json

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, 'tmp', 'config.json')


def generate_config_file(datas):
    config_params = {}

    config_params['configuration'] = {}

    config_params['configuration']['DATAS'] = {
        "DATA_FORMAT": datas['DATA_FORMAT'],
        "DATA_FEED": datas['DATA_FEED'],
        "DATA_PATH": datas['DATA_PATH'],
        "DATA_TYPE": datas['DATA_TYPE'],
        "RESHAPE": datas['RESHAPE'],
        "CLASSES": datas['CLASSES'],
    }

    config_params['configuration']['MODEL'] = {
        "MODEL_TYPE": datas['MODEL[MODEL_TYPE]'],
        "WEIGHTS_PATH": datas['MODEL[WEIGHTS_PATH]'],
        "LOGS_PATH": datas['MODEL[LOGS_PATH]'],
        "IMG_SHAPE": datas['MODEL[IMG_SHAPE]'],
        "BATCH_SIZE": datas['MODEL[BATCH_SIZE]'],
        "CALLBACKS": {},
    }

    config_params['configuration']['TASK'] = {
        "TASK_NAME": datas['TASK[TASK_NAME]'],
        "TASK_SPEC": {
            "EPOCHS": datas['TASK[TASK_SPEC][EPOCHS]'],
            "BATCH_SIZE": datas['TASK[TASK_SPEC][BATCH_SIZE]']
        }
    }

    if 'generator' in datas.keys():
        config_params['configuration']['DATAS']["RESCALE"] = datas['RESCALE']
        config_params['configuration']['DATAS']['TARGET_SIZE'] = datas['TARGET_SIZE']
        config_params['configuration']['DATAS']['BATCH_SIZE'] = datas['BATCH_SIZE']
        config_params['configuration']['DATAS']['CLASS_MODE'] = datas['CLASS_MODE']

    if 'compilation' in datas.keys():
        config_params['configuration']['MODEL']['COMPILATION'] = {
            "LOSS":{
                "NAME":datas['MODEL[COMPILATION][LOSS][NAME]']
                },
            "OPT":{
                "NAME":datas['MODEL[COMPILATION][OPT][NAME]']
                },
            "METRICS":datas['MODEL[COMPILATION][METRICS]']
        }
    with open(json_url, 'w') as json_file:
        json.dump(config_params, json_file, indent=2)

        return True
