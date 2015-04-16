from itertools import islice
from collections import defaultdict
import matplotlib.pyplot as plt


_DATA = "../data/cellartracker.txt"


def rating_dist():
    acc = defaultdict(int)
    with open(_DATA) as f:
        for line in islice(f, 4, None, 10):
            try:
                r = int(line[15:])
            except:
                r = -1
            acc[r] += 1
    return acc


def plot_dict(d):
    plt.bar(d.keys(), d.values())
    plt.show()


def user_freq():
    acc = defaultdict(int)
    with open(_DATA) as f:
        for line in islice(f, 6, None, 10):
            acc[line[line.index(":") + 2:]] += 1
    return acc
