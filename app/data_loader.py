import pickle
import thirsty
from collections import defaultdict
from tf_idf_index import dd, ll

def main():
	user_rating_index = pickle.load(open("pickles/user_ratings.p", "rb"))
	inverted_index = pickle.load(open("pickles/tfidf_inverted_index.p", "rb"))
	user_term_index = pickle.load(open("pickles/user_term.p", "rb"))
	beer_rating_index = pickle.load(open("pickles/beer_ratings.p", "rb"))
	beer_name_index = pickle.load(open("pickles/beer_name.p", "rb"))
	pmi_index = pickle.load(open("pickles/pmi_index.p", "rb"))
	beer_term_index = pickle.load(open("pickles/beer_term.p", "rb"))
	
	return thirsty.Thirsty(inverted_index, beer_rating_index, beer_name_index, user_rating_index, pmi_index, beer_term_index, user_term_index, 10000)