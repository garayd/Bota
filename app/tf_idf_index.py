import pickle
import string
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

DATA = "../data/Beeradvocate.txt"


# So pickle doesnt complain
def dd():
    return defaultdict(int)


def ll():
    return []


tfidf_inverted_index = defaultdict(dd)
beer_ratings_index = defaultdict(ll)
user_ratings_index = defaultdict(ll)
beer_name_index = {}
beer_id_index = {}
pmi_index = defaultdict(dd)
beer_term_index = defaultdict(dd)
user_term_index = defaultdict(dd)
total_reviews = 100000


def tfidf_data():

    with open(DATA) as f:

        beer_name    = ""
        beer_id      = 0
        brewer_id    = 0
        beer_ABV     = 0
        beer_style   = ""
        appearance   = 0
        aroma        = 0
        palate       = 0
        taste        = 0
        overall      = 0
        review_time  = 0
        profile_name = ""
        review_text  = ""

        data = [beer_name, beer_id, brewer_id, beer_ABV, beer_style,
                appearance, aroma, palate, taste, overall, review_time, profile_name, review_text]

        for line_num, line in enumerate(f):
            index_mod = line_num % 14
            if index_mod <= 12:
                data[index_mod] = line[line.index(":") + 2:][:-1]
            else:
                global total_reviews
                if (total_reviews <= 0):
                    dump_indeces()
                    return
                text = data[12].lower().translate(None, string.punctuation)
                tokens = nltk.word_tokenize(text)
                filtered = [w for w in tokens if w not in stopwords.words('english')]
                stemmer = PorterStemmer()

                for token in filtered:
                    token = stemmer.stem(token)
                    beer_term_index[data[1]][token] += 1
                    user_term_index[data[11]][token] += 1
                    tfidf_inverted_index[token][data[1]] += 1

                beer_ratings_index[data[1]].append({"appearance": data[5], "aroma": data[6], "palate": data[7], "taste": data[8], "overall": data[9]})

                user_ratings_index[data[11]].append({"appearance": data[5], "aroma": data[6], "palate": data[7], "taste": data[8], "overall": data[9], "beer_id": data[1]})

                beer_name_index[data[1]] = data[0]
                beer_id_index[data[0]] = data[1]
                total_reviews -= 1


def dump_indeces():
    pickle.dump(tfidf_inverted_index, open("pickles/tfidf_inverted_index.p", "wb"))
    pickle.dump(beer_ratings_index, open("pickles/beer_ratings.p", "wb"))
    pickle.dump(user_ratings_index, open("pickles/user_ratings.p", "wb"))
    pickle.dump(beer_name_index, open("pickles/beer_name.p", "wb"))
    pickle.dump(beer_term_index, open("pickles/beer_term.p", "wb"))
    pickle.dump(user_term_index, open("pickles/user_term.p", "wb"))
