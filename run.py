
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/accueil')
def accueil():
    return render_template('gestion_datas.html.j2')

if __name__ == '__main__':
    app.run(debug=True)
