import math
import re
import math

import nltk
import json

from flask import jsonify

from article_summaries.apps.summary.summarizers import Luhn, LSA

ps = nltk.stem.PorterStemmer();

def wadim_summarize(text, num_sentences):
    try:
        with open("idf.json", "r") as f:
            idf = json.load(f)
    except FileNotFoundError:
        print("Calculating IDF...")
        try:
            idf = calc_idf('./apps/summary/dataset.csv')
            with open("idf.json", "w") as f:
                json.dump(idf, f)
        except FileNotFoundError as e:
            return jsonify({ "error": f"Internal server error {e}" }), 500

    summary = summarize(text, idf, num_sentences)
    return summary

def lsa_summarize(text, num_sentences):
    return LSA.summarize(text, num_sentences)

def luhn_summarize(text, num_sentences):
    return Luhn.summarize(text, num_sentences)
def tokenize(line):
    tokens = re.sub('[^a-zA-Z]', ' ', str(line)).lower().split(' ')
    tokens = [ps.stem(t) for t in tokens]
    return tokens


def count_words(words):
    counts = dict()

    for w in words:
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1

    return counts


def calc_tf(text):
    words = tokenize(text)
    word_count = len(words)

    tf = dict()
    for (word, count) in count_words(words).items():
        tf[word] = count / word_count

    return tf


def calc_idf(filename):
    idf = dict()

    with open(filename, "r") as f:
        df = dict()

        article_count = 0
        for article in f:
            article_count += 1
            words = set(tokenize(article))
            for w in words:
                if w in df:
                    df[w] += 1
                else:
                    df[w] = 1

        for word in df.keys():
            idf[word] = math.log(article_count / (df[word] + 1))

    return idf


def rank_sentence(sentence, idf):
    rank = 0.0

    tf = calc_tf(sentence)
    for w in tf.keys():
        if w in idf:
            rank += tf[w] * idf[w]

    return rank


def summarize(article, idf, num_of_sentences):
    article = "".join(line.rstrip("\n") for line in article)
    sentences_ranked = {k: rank_sentence(k, idf) for k in article.split(". ")}
    sentences_ranked = {key: value
        for key, value in sorted(sentences_ranked.items(),
                                 key=lambda item: item[1])}
    return ". ".join(list(sentences_ranked.keys())[:int(num_of_sentences)]) + "."