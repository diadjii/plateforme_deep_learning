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
        "CLASSES": datas['CLASSES']
    }

    if datas['generator']:
        config_params['configuration']['DATAS']["RESCALE"] = datas['RESCALE']
        config_params['configuration']['DATAS']['TARGET_SIZE'] = datas['TARGET_SIZE']
        config_params['configuration']['DATAS']['BATCH_SIZE'] = datas['BATCH_SIZE']
        config_params['configuration']['DATAS']['CLASS_MODE'] = datas['CLASS_MODE']

    with open(json_url, 'w') as json_file:
        json.dump(config_params, json_file, indent=2)

        return True
