from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import ConfusionMatrixDisplay

from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from Scripts.helpers import get_random_string


class ConfusionMatrix:

    def __init__(self):
        self.gnb = GaussianNB()
        self.data = {}
        self.label = {}
        self.cm = None

    def generate_matrix(self, test, preds):
        self.cm = confusion_matrix(test, preds)

    def train_classifier(self, data, target):
        # Trainning classifier
        self.data = data
        self.label = target

        model = self.gnb.fit(data, target)

        return model

    def make_predictions(self, test):
        # Make predictions
        predicts = self.gnb.predict(test)

        return predicts

    def generate_image(self):

        figsize = (7, 7)

        annot = np.empty_like(self.cm).astype(str)

        fig, ax = plt.subplots(figsize=figsize)
        ax.margins(x = 0.1, y= 0.1)
        sns.heatmap(self.cm, annot=True, fmt='', ax=ax)

        img_name = get_random_string()
        b, t = plt.ylim() # discover the values for bottom and top
        b += 0.5 # Add 0.5 to the bottom
        t -= 0.5 # Subtract 0.5 from the top
        plt.ylim(b, t) # update the ylim(bottom, top) values
        plt.savefig('static/images/outputs/confusion_matrix/' + img_name, dpi=300, bbox_inches='tight')

        return img_name + '.png'
