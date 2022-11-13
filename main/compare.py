import pickle
from .models import *
from django.db.models.functions import Lower
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def make_X(task):
    # Get tasks
    tasks = Task.objects.filter(id=task.id)|Task.objects.all().exclude(id=task.id)
    X = [i for i in tasks.values_list(Lower("detail_text"), flat=True)]
    return X

def get_similarities(X):
    # Get term frequency and inversed document frequency
    v = TfidfVectorizer(min_df=3, max_df=0.7, stop_words=stopwords.words('german'))
    tfidf = v.fit_transform(X)

    # Similarity between each of the different data points
    pairwise_similarity = tfidf * tfidf.T

    # Return similarities
    return pairwise_similarity.toarray()


def most_similar(task):
    """
    :task: The task being searched for similar tasks
    :returns: Tuple exsisting of most similar task, similarity
    """
    # Get similarities for tasks
    X = make_X(task)
    similarities = get_similarities(X)

    # Find most similar task
    clone = (0, 0)
    for i, similarity in enumerate(similarities[0][1:]):
        if similarity > clone[1]: clone = (i, similarity)
    return  (X[clone[0]], clone[1])

def get_similar(index, similarities):
    """
    :param index: index in similarities checked for clones (similar tasks)
    :param similarities: np.array of similarities
    """

    # List of tasks being the same as the given task (having extremely similar detail texts)
    similar = list()

    for i, similarity in enumerate(similarities[index]):
        if similarity > 0.85 and i != index:
            # Same task
            if tasks[i] != task:
                similar.append((i, similarity))
    return similar



def main():
    X = make_X(Task.objects.filter(id=1)[0])
    similarities = get_similarities(X)
    print(get_closest_clone(Task.objects.filter(id=1)[0]))