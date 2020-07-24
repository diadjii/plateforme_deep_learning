from flask import Flask, render_template, send_file, redirect, url_for, request

from helpers import generate_config_file

from trainmnist import mnist_model

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
    mnist_model()
    return render_template('visualisation.html.j2')

@app.route('/accueil')
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
