from tensorflow.keras.datasets import mnist
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import mpld3

def mnist_model():
    (train_images, train_labels), (val_images, val_labels) = mnist.load_data()

    network = models.Sequential()
    network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
    network.add(layers.Dense(10, activation='softmax'))
    
    network.compile(optimizer='sgd',
    loss='categorical_crossentropy',
    metrics=['accuracy'])

    train_images = train_images.reshape((60000, 28 * 28))
    train_images = train_images.astype('float32') / 255
    val_images = val_images.reshape((10000, 28 * 28))
    val_images = val_images.astype('float32') / 255

    train_labels = to_categorical(train_labels)
    val_labels = to_categorical(val_labels)

    hist = network.fit(train_images, train_labels, epochs=5, batch_size=128, validation_split=.1)
        
    plt.plot(hist.history['accuracy'])
    plt.plot(hist.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Val'], loc='lower right')
    plt.savefig('static/images/mnist.png', dpi=100)
    
    