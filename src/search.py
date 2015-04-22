import user_query
import index
import tools

import math
from collections import defaultdict
from operator import itemgetter


WINE_INDEX = index.load_index('wine_index.p')
RATING_INDEX = index.load_index('rating_index.p')
NAME_INDEX = index.load_index('name_index.p')


def tf_idf(term):
    return math.log(tools.NUMBER_OF_WINES / len(WINE_INDEX[term]))


def wine_norm(wine_id):
    return len(RATING_INDEX[wine_id])


def wine_return(wines):
    acc = []
    for wine_id, score in wines:
        acc.append((NAME_INDEX[wine_id], score))
    return acc


def query_search(query, version='tf-idf', expansion=False):
    query_tokens = user_query.clean_query(query)

    if version == 'tf-idf':
        wines = tf_idf_search(query_tokens)

    return wine_return(wines)


def tf_idf_search(tokens):
    wine_scores = defaultdict(int)
    for token in tokens:
        if token in WINE_INDEX:
            for wine in WINE_INDEX[token]:
                wine_scores[wine] += WINE_INDEX[token][wine] * tf_idf(token)

    for wine in wine_scores:
        wine_scores[wine] = wine_scores[wine] / float(wine_norm(wine))

    return sorted(wine_scores.items(), key=itemgetter(1), reverse=True)
