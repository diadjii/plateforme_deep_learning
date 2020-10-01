import os
from werkzeug.utils import secure_filename

from flask import Flask, render_template, send_file, redirect, url_for, request, jsonify
from flask_socketio import SocketIO, send, emit
from tensorflow.keras.datasets import mnist

from Configurations.configuration import Configuration
from Instances.Training.train import TrainingInstance
from Instances.Inference.inference import InferenceInstance
from Instances.Visualization.visualization import VisualizationInstance
from Instances.Models.model_instance import ModelInstance
from Scripts.trainmnist import Visualisation
from Scripts.confusionmatrix import ConfusionMatrix
from Scripts.helpers import generate_config_file
from Scripts.masquage import AfficherMasque
from Scripts.detection_objets import ObjectDetection
from Scripts.classification_report import ClassificationReport
from Scripts.pc_state import PCState

app = Flask(__name__)
socketio = SocketIO(app)

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
    model = Visualisation()
    hist = model.mnist_model()
    graphe = Visualisation()
    graphe.display_train_val(hist)

    return "ok"

@app.route('/visualisation/auc-roc-map-p-r')
def courbe():
    return render_template('generation_courbes.html.j2')

@app.route('/display-metriques')
def visualisationcourbe():
    clr = ClassificationReport()

    clr.classification_mnist()

    return "ok"

@app.route('/mask')
def mask():
    return render_template('mask.html.j2')


@app.route('/mask/show', methods=['GET', 'POST'])
def showmask():
    if request.method == 'POST':
        image = request.files['image_mask']
            
        imagename = secure_filename(image.filename)

        image.save(os.path.join('static/images/outputs', imagename))

        mask = AfficherMasque(os.path.join('static/images/outputs', imagename))

        mask.affiche(0.5)
    
        return render_template('showmask.html.j2', imagename = imagename)
    else:
        image_name= request.args.get('name')
        alpha = request.args.get('alpha')

        mask = AfficherMasque(os.path.join('static/images/outputs', image_name))
                
        mask.affiche(float(alpha))
                
        return 'ok'


@app.route('/configuration')
def accueil():
    return render_template('gestion_datas.html.j2')

@app.route('/config/generate', methods=['POST', 'GET'])
def generate_config():
    if request.method == "POST":
        response = "true"
        if generate_config_file(request.form) != True:
            response = "false"
        return response
    else:
        path = "tmp/config.json"

        return send_file(path, as_attachment=True)


@app.route('/training')
def start_training():
    conf = Configuration("tmp/test_minist.json")
    task_name = conf.dic['TASK']['TASK_NAME']

    if len(conf.errors) == 0:
        if task_name == 'TRAIN':
            ti = TrainingInstance(conf.dic)
            ti.start_training()
            ti.close()
        if task_name == 'INFERENCE':
            ei = InferenceInstance(conf.dic)
            data_type = conf.dic['TASK']['TASK_SPEC']['DATA_TYPE']
            if data_type == "IMAGE":
                ei.inference_on_image()
            elif data_type == "IMAGE_FOLDER":
                ei.inference_on_folder()
                ei.close()
        if task_name == 'FIND_LR':
            ti = TrainingInstance(conf.dic)
            ti.find_lr()
            ti.close()
        if task_name == 'CHECK_ANNOTATIONS':
            vi = VisualizationInstance(conf.dic)
            vi.check_annotations()
            vi.close()


@app.route('/confusion_matrix')
def page_confusion_matrix():
    return render_template('confusion_matrix.html.j2')

@socketio.on('generate_matrix')
#@app.route('/generate_matrix')
def get_confusion_matrix():
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    conf = ConfusionMatrix()
    # reshape image from 3D --> 1D
    new_train_images = train_images.reshape((60000, 28*28))
    new_test_images = test_images.reshape(10000, 28*28)

    conf.train_classifier(new_train_images, train_labels)
    send("Entrainement du Classifier en cours ...")
    # prediction ==> image test
    preds = conf.make_predictions(new_test_images)
    send("Prediction en cours...")

    conf.generate_matrix(test_labels, preds)
    send("Generation de la Matrice en cours ...")

    img_name = conf.generate_image()
    
    emit("response_generate_matrix",img_name)

@app.route('/detection_objets')
def detection():
    return render_template('detection_objets.html.j2')

@app.route('/go_detect_objects', methods=['POST'])
def go_detect_objets():
    if request.method == "POST":
        img = request.files['image']

        imagename = secure_filename(img.filename)
        img.save(os.path.join('tmp/', imagename))
        obj = ObjectDetection(os.path.join('tmp/',imagename))
        
        if obj.detect_objects() :
            return obj.results
        else:
            return False

@app.route('/state')
def get_state():
    pc_state = PCState()
    data = pc_state.get_info()

    return data

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
    socketio.run(app)
