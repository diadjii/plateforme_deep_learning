from tensorflow.keras.datasets import mnist
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt


class Visualisation():

    def __init__(self):
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = mnist.load_data()
        self.network = models.Sequential()

    def mnist_model(self):
        self.network.add(layers.Dense(
            512, activation='relu', input_shape=(28 * 28,)))
        self.network.add(layers.Dense(10, activation='softmax'))
        self.network.compile(
            optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

        self.train_images = self.train_images.reshape((60000, 28 * 28))
        self.train_images = self.train_images.astype('float32') / 255

        self.test_images = self.test_images.reshape((10000, 28 * 28))
        self.test_images = self.test_images.astype('float32') / 255

        self.train_labels = to_categorical(self.train_labels)
        self.test_labels = to_categorical(self.test_labels)

        hist = self.network.fit(self.train_images, self.train_labels, epochs=5, batch_size=128, validation_split=.1)

        return hist

    def display_train_val(self, hist):
                # Accuracy Model Graph
        plt.plot(hist.history['acc'])
        plt.plot(hist.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='lower right')
        plt.savefig('static/images/outputs/mnistaccuracy.png', dpi=100)
        plt.clf()

        # Loss Model Graphe
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='lower right')
        plt.savefig('static/images/outputs/mnistloss.png', dpi=100)
        plt.clf()
