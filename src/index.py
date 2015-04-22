import pickle
from itertools import islice
from collections import defaultdict

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


DATA = "../data/data.txt"


def name_index(index, lines):
    wine_id = lines[1][13:][:-1]
    wine_name = lines[0][11:][:-1]

    if wine_id not in index:
        index[wine_id] = []

    index[wine_id].append(wine_name)


def wine_index(index, lines):
    wine_id = lines[1][13:][:-1]
    review_text = lines[8][13:].lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = filter(lambda token: token not in stopwords.words('english'), tokenizer.tokenize(review_text))

    for token in tokens:
        if token not in index:
            index[token] = defaultdict(int)
        index[token][wine_id] += 1


def rating_index(index, lines):
    wine_id = lines[1][13:][:-1]
    rating = lines[4][15:]

    if wine_id not in index:
        index[wine_id] = defaultdict(int)

    index[wine_id][rating] += 1


def create_index(DATA, fun):
    index = {}
    with open(DATA) as f:
        while True:
            lines = list(islice(f, 10))
            if not lines:
                break
            fun(index, lines)

    return index


def dump_index(index, f):
    pickle.dump(index, open(f, "wb"))


def load_index(f):
    return pickle.load(open(f, "rb"))
