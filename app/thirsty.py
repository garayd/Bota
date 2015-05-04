import math
from collections import defaultdict
from operator import itemgetter

import nltk
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction import DictVectorizer
from sklearn.random_projection import SparseRandomProjection

import numpy as np
import scipy.spatial.distance as cos
import numpy as np
import matplotlib.pyplot as plt


class Thirsty:

    def __init__(self, inverted_index, beer_rating_index, beer_name_index, user_rating_index, pmi_index, beer_term_index, user_term_index, N):

        self.inverted_index    = inverted_index
        self.beer_rating_index = beer_rating_index
        self.beer_name_index   = beer_name_index
        self.user_rating_index = user_rating_index
        self.pmi_index         = pmi_index
        self.beer_term_index   = beer_term_index
        self.user_term_index   = user_term_index
        self.N                 = N

    def idf(self, term):
        return math.log(self.N / len(self.inverted_index[term]))

    def beer_norm(self, beer_id, tokens):
        acc = 0
        for token in tokens:
            if token in self.beer_term_index[beer_id]:
                acc += 1
        return acc

    def beer_norm2(self, beer_id, tokens):
        acc = 0
        for term, count in self.beer_term_index[beer_id].iteritems():
            acc += count
        return acc

    def avg_beer_rating(self, beer_id):
        appearance = 0.0
        aroma = 0.0
        overall = 0.0
        palate = 0.0
        taste = 0.0
        t = 0.0
        for dict in self.beer_rating_index[beer_id]:
            t += 1.0
            appearance += float(dict['appearance'])
            aroma += float(dict['aroma'])
            overall += float(dict['overall'])
            palate += float(dict['palate'])
            taste += float(dict['taste'])

        return {'appearance': appearance / t, 'aroma': aroma / t, 'overall': overall / t, 'palate': palate / t, 'taste': taste / t}

    def pmi(self, x, y):
        length = float(len(self.pmi_index))
        p_xy = max(self.pmi_index[x][y], self.pmi_index[y][x]) / length
        p_x = self.pmi_index[x][x] / length
        p_y = self.pmi_index[y][y] / length
        t = math.log(float(p_xy) / (float(p_y * p_x)))
        return t / (-1 * math.log(p_xy))

    def correlated_terms(self, term, x):
        acc = []
        p = sorted(self.pmi_index[term].items(), key=itemgetter(1), reverse=True)[:100]
        for key, elem in p:
            acc.append((key, self.idf(key) * self.pmi(term, key)))
        x = sorted(acc, key=itemgetter(1), reverse=True)[1:x + 1]
        return [i for i, j in x]

    def user_similarity(self, beer_id, user):
        v = DictVectorizer(sparse=False)
        D = [self.beer_term_index[beer_id], self.user_term_index[user]]
        X = v.fit_transform(D)
        return cos.cosine(X[0], X[1])

    def beer_similarity(self, beer1, beer2):
        v = DictVectorizer(sparse=False)
        D = [self.beer_term_index[beer1], self.beer_term_index[beer2]]
        X = v.fit_transform(D)
        return cos.cosine(X[0], X[1])

    def rank(self, beers, tokens):
        acc = []
        for beer_id, score in beers.iteritems():
            if self.user is not None:
                sim = self.user_similarity(beer_id, self.user)
            else:
                sim = 1.0
            rating = 1.0
            for elem in self.sort_by:
                rating = rating * self.avg_beer_rating(beer_id)[elem]
            t = self.beer_name_index[beer_id], rating * score * sim, beer_id
            acc.append(t)

        result = sorted(acc, key=itemgetter(1), reverse= True)

        if self.verbose:
            return tokens
        else:
            return {"list":result}

    def beer_query(self, query, user):

        beer_id = ""
        for k, v in self.beer_name_index.items():
            if v == query:
                beer_id = k
                avg = self.avg_beer_rating(beer_id)
                break
        user_sim = self.user_similarity(beer_id, user)
        acc = []

        for k, v in self.beer_term_index[beer_id].items():
            acc.append((k, v * self.idf(k)))

        acc = sorted(acc, key=itemgetter(1), reverse=True)[:10]
        acc = [i for i, j in acc]
        sim_beers = []

        for beer in self.beer_term_index:
            sim_beers.append((beer, self.beer_similarity(beer, beer_id)))

        sim_beers = sorted(sim_beers, key=itemgetter(1), reverse=True)[:10]
        sim_beers = [self.beer_name_index[i] for i, j in sim_beers]

        return {"beer": [query, avg['appearance'], avg['aroma'], avg['overall'], avg['palate'], avg['taste'], user_sim, sim_beers, acc]}

    def query(self, query, sort_by=['overall'], user=None, expansion=0, verbose=False):
        if query in self.beer_name_index.values():
            return self.beer_query(query, user)
        stemmer = PorterStemmer()
        query_tokens = nltk.word_tokenize(query)
        query_tokens = [stemmer.stem(w) for w in query_tokens]

        self.verbose = verbose
        self.sort_by = sort_by
        self.user = user
        self.expansion = expansion
        corr_tokens = []

        if expansion > 0:
            for term in query_tokens:
                corr_tokens += self.correlated_terms(term, expansion)

        query_tokens += corr_tokens

        if (("or" in query_tokens) | ("and" in query_tokens)):
            beers = self.boolean_search(query_tokens)
        else:
            beers = self.search(query_tokens)

        return self.rank(beers, query_tokens)

    def search(self, tokens):
        beer_scores = defaultdict(int)
        for token in tokens:
            if token in self.inverted_index:
                for beer_id in self.inverted_index[token]:
                    beer_scores[beer_id] += self.inverted_index[token][beer_id] * self.idf(token)

        for beer_id in beer_scores:
            beer_scores[beer_id] = beer_scores[beer_id] / float(self.beer_norm2(beer_id, tokens))

        return beer_scores

    def boolean_search(self, query_tokens):
        and_indeces = [(i, x) for i, x in enumerate(query_tokens) if x == "and"]
        or_indeces  = [(i, x) for i, x in enumerate(query_tokens) if x == "or"]
        l = sorted(or_indeces + and_indeces, key=itemgetter(0))
        if (len(l) == 0):
            return self.search(query_tokens)
        else:
            for i, j in l:
                a = self.search(query_tokens[:i])
                b = self.boolean_search(query_tokens[i + 1:])
                if j == "or":
                    return self.union(a, b)
                else:
                    return self.interesct(a, b)

    def interesct(self, a, b):
        acc = defaultdict(int)
        for beer_id1, score1 in a.items():
            for beer_id2, score2 in b.items():
                if beer_id1 == beer_id2:
                    acc[beer_id1] += score1 + score2
        return acc

    def union(self, a, b):
        acc = defaultdict(int)
        for beer_id1, score1 in a.items():
            acc[beer_id1] = score1
        for beer_id2, score2 in b.items():
            acc[beer_id2] = max(acc[beer_id2], score2)
        return acc

    def heatmap(self, l):
        stemmer = PorterStemmer()
        l = [stemmer.stem(w) for w in l]
        length = len(l)
        X = np.zeros((length, length))
        for i, v1 in enumerate(l):
            for j, v2 in enumerate(l):
                X[i, j] = self.pmi(v1, v2)

        plt.imshow(X, interpolation='none', cmap=plt.cm.Greys)
        plt.colorbar()

        plt.xticks(range(length), l, rotation=90)
        plt.yticks(range(length), l)
        plt.show()

    def cluster_users(self, dim):
        v = DictVectorizer(sparse=False)
        D = []
        U = []
        for user, dic in self.user_term_index.items():
            U.append(user)
            D.append(dic)
        X = v.fit_transform(D)
        cluster = SparseRandomProjection(n_components=dim)
        return cluster.fit_transform(X)

    def cluster_beers(self, dim):
        v = DictVectorizer(sparse=False)
        D = []
        U = []
        for beer, dic in self.beer_term_index.items():
            U.append(beer)
            D.append(dic)
        X = v.fit_transform(D)
        cluster = SparseRandomProjection(n_components=dim)
        return cluster.fit_transform(X)
