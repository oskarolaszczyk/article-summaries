import re
import math
import sys
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
    article = " ".join(line.rstrip("\n") for line in article)
    sentences_ranked = {k: rank_sentence(k, idf) for k in article.split(". ")}
    return ". ".join(list(sentences_ranked.keys())[:num_of_sentences]) + "."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} NUM_OF_SENTENCES", file=sys.stderr)
        exit(1)

    num_of_sentences = sys.argv[1]
    idf = dict()

    try:
        with open("idf.json", "r") as f:
            idf = json.load(f)
    except FileNotFoundError:
        print("Calculating IDF...")
        try:
            idf = calc_idf('dataset.csv')
            with open("idf.json", "w") as f:
                json.dump(idf, f)
        except FileNotFoundError as e:
            print(f"Dataset not found: {e}", file=sys.stderr)
            exit(1)

    article = sys.stdin.readlines()
    summary = summarize(article, idf, int(num_of_sentences))
    print(summary)
