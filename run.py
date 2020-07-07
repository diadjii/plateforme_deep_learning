from flask import Flask, render_template, send_file, redirect, url_for, request

from helpers import generate_config_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Telecharger')
def download_file():
    path = "static/config.json"
    return send_file(path, as_attachment=True)

@app.route('/accueil')
def accueil():
    return render_template('gestion_datas.html.j2')

@app.route('/config/generate', methods=['POST','GET'])
def generate_config():
    if request.method =="POST":

        datas = request.form

        config_params = {}

        config_params['configuration'] = {}
        
        config_params['configuration']['DATAS'] = {
            "DATA_FORMAT" : datas['DATA_FORMAT'],
        	"DATA_FEED" : datas['DATA_FEED'],
        	"DATA_PATH" : datas['DATA_PATH'],
        	"DATA_TYPE" : datas['DATA_TYPE'],
        	"RESHAPE" : datas['RESHAPE'],
            "CLASSES":datas['CLASSES']
        }
        
        if datas['generator']:
            config_params['configuration']['DATAS']["RESCALE"] = datas['RESCALE']
            config_params['configuration']['DATAS']['TARGET_SIZE'] = datas['TARGET_SIZE']
            config_params['configuration']['DATAS']['BATCH_SIZE'] = datas['BATCH_SIZE']
            config_params['configuration']['DATAS']['CLASS_MODE'] = datas['CLASS_MODE']
            
        response = "true"
        if generate_config_file(config_params) != True:
          response = "false"
        
        return response
    else:
        path =  path = "tmp/config.json"
        return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
