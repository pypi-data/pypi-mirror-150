from collections import Counter


def count_word(length, word):
    count = Counter(length)
    return count[word]