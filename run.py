import os

from flask import Flask, render_template, send_file, redirect, url_for, request

from werkzeug.utils import secure_filename

from helpers import generate_config_file

from trainmnist import Visualisation

from masquage import AfficherMasque

app = Flask(__name__)
 

@app.route('/')
def index():
    return render_template('gestion_datas.html.j2')


@app.route('/Telecharger')
def download_file():
    path = "static/config.json"
    return send_file(path, as_attachment=True)


@app.route('/visualisation')
def test_mnist():
    return render_template('visualisation.html.j2')


@app.route('/display-graphe')
def start_visualisation():
    graphe = Visualisation()
    graphe.mnist_model()
    graphe.hist()

    return "ok"


@app.route('/mask')
def mask():
    return render_template('mask.html.j2')


@app.route('/mask/show', methods=['GET', 'POST'])
def showmask():
    if request.method == 'POST':
        image = request.files['image_mask']
        imagename = secure_filename(image.filename)
        image.save(os.path.join('static/images', imagename))
        mask = AfficherMasque(os.path.join('static/images', imagename))
        mask.affiche(0.5)

    return render_template('showmask.html.j2', imagename = imagename)

@app.route('/configuration')
def accueil():
    return render_template('gestion_datas.html.j2')


@app.route('/config/generate', methods=['POST', 'GET'])
def generate_config():
    if request.method == "POST":
        print(request.form)
        response = "true"
        if generate_config_file(request.form) != True:
            response = "false"

        return response
    else:
        path = "tmp/config.json"

        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
