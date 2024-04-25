from flask import Flask, request, jsonify
from goose3 import Goose
from flask_cors import CORS

import re
import math
import nltk
import json


ps = nltk.stem.PorterStemmer();


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
    return ". ".join(list(sentences_ranked.keys())[:num_of_sentences]) + "."

app = Flask(__name__)
CORS(app)
headers = { "Accept-Language": "pl,en-US;q=0.7,en;q=0.3" }
goose = Goose({ "http_headers": headers })


@app.route("/scrape", methods=['GET'])
def scrape():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({ "error": "URL parameter is missing" }), 400
        web_text = goose.extract(url=url).cleaned_text
        return jsonify({ "content": web_text })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500


@app.route("/summarize", methods=['POST'])
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
            idf = calc_idf('dataset.csv')
            with open("idf.json", "w") as f:
                json.dump(idf, f)
        except FileNotFoundError:
            return jsonify({ "error": "Internal server error" }), 500

    summary = summarize(req['txt'], idf, req['sentences'])

    return jsonify({ "summary": summary })
