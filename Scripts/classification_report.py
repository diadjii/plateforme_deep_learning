# Standard scientific Python imports
import matplotlib.pyplot as plt
import numpy as np 

# Import classifiers and performance metrics
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import RocCurveDisplay

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist, cifar10

class ClassificationReport():

    def print_classification_report(self, y_true, y_pred):
        print("Classification Report")
        print(classification_report(y_true, y_pred))
        acc_sc = accuracy_score(y_true, y_pred)
        print("Accuracy : "+ str(acc_sc))
        return acc_sc

    def mean_average_precision(self, y_true, y_pred):
        average_precision = average_precision_score(y_true, y_pred)
        return average_precision

    def area_under_curve(self, y_true, y_pred):
        roc_auc = roc_auc_score(y_true, y_pred)
        return roc_auc

    def precision_recall(self, y_true, y_pred, average_precision):
        precisions, recalls, _ = precision_recall_curve(y_true, y_pred, pos_label=5)
        PrecisionRecallDisplay(precision = precisions, recall = recalls, average_precision = average_precision, estimator_name = "AP").plot()
        plt.title('Metrique Precision & Recall')
        plt.savefig('static/images/outputs/metriquePR.png', dpi=100)
        plt.clf()

    
    def receiver_operator(self, y_true, y_pred, area_under_curve):
        fpr, tpr, _ = roc_curve(y_true, y_pred, pos_label=5)
        RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=area_under_curve, estimator_name="AUC").plot()
        plt.title('Metrique Receiver Operator Curve')
        plt.savefig('static/images/outputs/metriqueROC.png', dpi=100)
        plt.clf()


    def dense_model_0(self):
        model = Sequential()
        model.add(Dense(10, input_shape=(28 * 28,), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model


    def classification_mnist(self):
        (X_train, Y_train), (X_test, Y_test) = mnist.load_data()

        X_train = X_train.reshape((60000, 28 * 28))
        X_train = X_train.astype('float32') / 255

        X_test = X_test.reshape((10000, 28 * 28))
        X_test = X_test.astype('float32') / 255

        Y_train = to_categorical(Y_train, 10)
        Y_test_10 = to_categorical(Y_test, 10)

        model_dense_0 = self.dense_model_0()
        model_dense_0.fit(X_train, Y_train, epochs=10, batch_size=128)

        #Prediction du modele
        pred_val_dense0 = np.argmax(model_dense_0.predict(X_test), axis=-1)
        #Classification report
        self.print_classification_report(Y_test, pred_val_dense0)
                
        pred_val_dense10 = to_categorical(pred_val_dense0, 10)
        #mean Average Precision 
        mAP = self.mean_average_precision(Y_test_10, pred_val_dense10)
        #Area Under the Curve
        auc = self.area_under_curve(Y_test_10, pred_val_dense10)
        #Precision and Recall
        self.precision_recall(Y_test, pred_val_dense0, mAP)
        #Receiver Operator Curve
        self.receiver_operator(Y_test, pred_val_dense0, auc)