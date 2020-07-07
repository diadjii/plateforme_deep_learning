import os, json 

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, 'tmp', 'config.json')

def generate_config_file(datas):
    with open(json_url,'w') as json_file:
        json.dump(datas, json_file, indent=2)

        return True