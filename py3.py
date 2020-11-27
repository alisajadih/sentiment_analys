from functools import reduce
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def calc_orientation(positives, negatives, comments):
    stem_positives = set()
    stem_negatives = set()
    porter = PorterStemmer()
    for item in positives:
        stem_positives.add(porter.stem(item))
    for item in negatives:
        stem_negatives.add(porter.stem(item))

    def positive_map(c):
        comment_tokens = word_tokenize(c)

        def calc_number(acc, curr):
            return acc + (1 if curr in comment_tokens else 0)
        return reduce(calc_number, stem_positives, 0)

    def negative_map(c):
        comment_tokens = word_tokenize(c)

        def calc_number(acc, curr):
            return acc + (-1 if curr in comment_tokens else 0)
        return reduce(calc_number, stem_negatives, 0)

    positives_aspect = list(map(positive_map, comments))
    negative_aspect = list(map(negative_map, comments))
    final_aspects = [a + b for a, b in zip(positives_aspect, negative_aspect)]
    return final_aspects


def print_result(comments_orientation_numbers):
    for index, orient in enumerate(comments_orientation_numbers):
        print(index+1, '.')
        print('\t', f"sentiment={'positive' if orient > 0 else 'negative'}")
        print('\t', f"score: {orient}")


def print_overal(status, percent):
    print('\nOverall:')
    print('\tRecommendation:', status)
    print('\tRecommendation Score:', f'% {percent*100:.1f}')


def sentiment_analys(positives, negatives, comments):
    comments_orientation_numbers = calc_orientation(
        positives, negatives, comments)

    length_of_positives = len(
        list(filter(lambda x: x > 0, comments_orientation_numbers)))
    print_result(comments_orientation_numbers)
    print_overal('Buy' if length_of_positives > len(comments_orientation_numbers) /
                 2 else 'Not Buy', length_of_positives/len(comments_orientation_numbers))


with open("./positive-words.txt") as positive_file, open("./negative-words.txt") as negative_file, open('./Canon G3.txt') as comments_file:
    positives_resolve_file = [
        x for x in positive_file.read().split('\n') if x != '']
    negatives_resolve_file = [
        x for x in negative_file.read().split('\n') if x != '']
    comments_resolve_file = comments_file.read()

    positives = [x for x in positives_resolve_file if not x.startswith(';')]
    negatives = [x for x in negatives_resolve_file if not x.startswith(';')]
    comments = comments_resolve_file.split('[t]')[1:]

    sentiment_analys(positives, negatives, comments)
