import math
from operator import attrgetter
from collections import namedtuple

from nltk.corpus import stopwords
import numpy as np
from numpy.linalg import svd as singular_value_decomposition
from SumUtil import get_words, get_sentences
import nltk

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

SentenceInfo = namedtuple("SentenceInfo", ("sentence", "order", "rating",))


def normalize_word(word):
    return word.lower()


def create_dict(txt, stop_words):

    words = get_words(txt)
    words = tuple(words)

    words = map(normalize_word, words)

    unique_words = frozenset(w for w in words if w not in stop_words)

    return dict((w, i) for i, w in enumerate(unique_words))


def create_matrix(sentences, dictionary):
    words_count = len(dictionary)
    sentences_count = len(sentences)
    if words_count < sentences_count:
        print("Warning: number of words is lower than number of sentences.")

    matrix = np.zeros((words_count, sentences_count))
    for col, sentence in enumerate(sentences):
        words = get_words(sentence)
        for word in words:
            if word in dictionary:
                row = dictionary[word]
                matrix[row, col] += 1

    return matrix


def compute_term_frequency(matrix, factor=0.4):
    max_word_frequencies = np.max(matrix, axis=0)
    rows, cols = matrix.shape
    for row in range(rows):
        for col in range(cols):
            max_word_frequency = max_word_frequencies[col]
            if max_word_frequency != 0:
                frequency = matrix[row, col] / max_word_frequency
                matrix[row, col] = factor + (1.0 - factor) * frequency

    return matrix


def compute_ranks(sigma, v_matrix, min_dim=3, rr=1 / 1):
    assert len(sigma) == v_matrix.shape[0]

    dimensions = max(min_dim,
                     int(len(sigma) * rr))
    powered_sigma = tuple(s ** 2 if i < dimensions else 0.0
                          for i, s in enumerate(sigma))
    ranks = []
    for column_vector in v_matrix.T:
        rank = sum(s * v ** 2 for s, v in zip(powered_sigma, column_vector))
        ranks.append(math.sqrt(rank))
    return ranks

def get_best_sentences(sentences, count, rating, *args, **kwargs):
    rate = rating
    if isinstance(rating, dict):
        assert not args and not kwargs
        rate = lambda s: rating[s]

    infos = (SentenceInfo(s, o, rate(s, *args, **kwargs))
             for o, s in enumerate(sentences))

    # sort sentences by rating in descending order
    infos = sorted(infos, key=attrgetter("rating"), reverse=True)
    # get `count` first best rated sentences
    infos = infos[:min(count, len(infos))]
    # sort sentences by their order in document
    infos = sorted(infos, key=attrgetter("order"))

    return tuple(i.sentence for i in infos)
def summarize(text, max_no_of_sentences=10):
    dictionary = create_dict(text, stop_words=stopwords.words('english'))
    sentences = get_sentences(text)
    matrix = create_matrix(sentences, dictionary)
    matrix = compute_term_frequency(matrix)
    u, sigma, v = singular_value_decomposition(matrix, full_matrices=False)
    ranks = iter(compute_ranks(sigma, v))
    return get_best_sentences(sentences, max_no_of_sentences, lambda s: next(ranks))
