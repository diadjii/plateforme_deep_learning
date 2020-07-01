
from flask import Flask, render_template, send_file, redirect, url_for

import numpy

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

if __name__ == '__main__':
    app.run(debug=True)
