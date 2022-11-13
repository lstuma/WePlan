import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from .models import *
from django.db.models.functions import Lower


def vectorizer(X):
    # Vectorize text input X
    v = CountVectorizer(max_features=50, min_df=7, max_df=0.7, stop_words=stopwords.words('german'))
    return v.fit_transform(X).toarray()


model = None
try:
    # Load model
    with open('text_classifier', 'rb') as training_model:
        model = pickle.load(training_model)
except:
    model = None

def train():
    global model

    # Prepare training data
    tasks = Task.objects.filter(estimated=False).exclude(duration=None)
    X = [i for i in tasks.values_list(Lower("detail_text"), flat=True)]

    y_dur = tasks.values_list("duration", flat=True)
    #y_qu = tasks.values_list("quantity", flat=True)

    #y = np.array([d/q for d,q in zip(y_dur, y_qu)])

    y = np.array(y_dur)

    print(len(y))

    # Convert text to numbers
    X = vectorizer(X)

    # Get term frequency and inverse document frequency
    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()

    print(X.shape)
    print(y.shape)
    print(X)

    # Train model with training data
    classifier = RandomForestRegressor(n_estimators=1000, random_state=0)
    classifier.fit(X, y)

    # Save model
    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(classifier, picklefile)

    model = classifier


def save_to_model():
    global model
    tasks = Task.objects.exclude(duration=False)
    X = [i for i in tasks.values_list(Lower("detail_text"), flat=True)]

    # Convert text to numbers
    X = vectorizer(X)

    # Get term frequency and inverse document frequency
    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()

    y_pred = model.predict(X)
    print(y_pred)

    for task, d_stk in zip(tasks, y_pred):
        task.duration = d_stk #* task.quantity
        task.save()



def evaluate_model(X_test=None, y_test=None):
    global model
    # Predict values
    y_pred = [i for i in model.predict(X_test)]

    # Print out accuracy of model
    print(metrics.accuracy_score(y_test, y_pred))

    import matplotlib.pyplot as plt
    # Get confusion matrix
    metrics.plot_confusion_matrix(model, X_test, Y_test)
    plt.show()


def main():
    global model
    train()
    save_to_model()
