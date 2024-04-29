from flask import Blueprint, jsonify, request

import re
import math
import nltk
import json


ps = nltk.stem.PorterStemmer();

summary_bp = Blueprint(
    "summary_bp", __name__, template_folder="templates", static_folder="static"
)


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


@summary_bp.route("/", methods=['POST'])
def summarize_endpoint():
    req = request.get_json()

    if not 'txt' in req:
        return jsonify({ "error": "No article content provided" }), 400
    if not 'sentences' in req:
        return jsonify({ "error": "Number of sentences not provided" }), 400

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

    summary = summarize(req['txt'], idf, req['sentences'])

    return jsonify({ "summary": summary })
