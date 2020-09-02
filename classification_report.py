# Standard scientific Python imports
import matplotlib.pyplot as plt

import numpy as np 

# Import datasets, classifiers and performance metrics
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
#import mnist dataset
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist, cifar10

class ClassificationReport():

    def random_image(self, train_image, train_label):
        random_index = np.random.randint(0,train_image.shape[0])
        plt.imshow(train_image[random_index], cmap='BuPu_r')
        plt.title(train_label[random_index])
        plt.axis("Off")
        plt.show()

    def print_classification_report(self, y_true, y_pred):
        print("Classification Report")
        print(classification_report(y_true, y_pred))
        acc_sc = accuracy_score(y_true, y_pred)
        print("Accuracy : "+ str(acc_sc))
        return acc_sc

    def dense_model_0(self):
        model = Sequential()
        model.add(Dense(10, input_shape=(28 * 28,), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model
    
    def precision_recall(self, estimator, x_test, y_test):
        disp = plot_precision_recall_curve(estimator, x_test, y_test)
        disp.ax_.set_title('Precision-Recall curve: ')

    def classification_mnist(self):
        (X_train, Y_train), (X_test, Y_test) = mnist.load_data()

        X_train = X_train.reshape((60000, 28 * 28))
        X_train = X_train.astype('float32') / 255

        X_test = X_test.reshape((10000, 28 * 28))
        X_test = X_test.astype('float32') / 255

        Y_train = to_categorical(Y_train, 10)
        #Y_test_10 = to_categorical(Y_test, 10)

        model_dense_0 = self.dense_model_0()
        model_dense_0.fit(X_train, Y_train, epochs=10, batch_size=128)

        pred_val_dense0 = model_dense_0.predict_classes(X_test)
        self.print_classification_report(Y_test, pred_val_dense0)
        



