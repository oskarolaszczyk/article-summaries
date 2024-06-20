import re


def get_sentences(txt):
    return txt.split('.')

def get_words(txt):
    only_words_text = re.compile(r'[^0-9^a-z^A-Z\s]').sub('',txt)
    return only_words_text.split(' ')
