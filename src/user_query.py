from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


def clean_query(query):
    tokenizer = RegexpTokenizer(r'\w+')
    return filter(lambda token: token not in stopwords.words('english'), tokenizer.tokenize(query.lower()))


def expand_query(tokenized_query):
    pass


def cache_query():
    pass
