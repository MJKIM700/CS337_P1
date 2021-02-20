import string
import sys
import pull_text
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


def get_tweets(year):
    tweets = pull_text.Data(year).tweets
    tweettext = []
    for tweet in tweets:
        tweettext.append(tweet.text)
    return tweettext


def ngrams_best(in_string, caps):
    ngram_list = []
    capped = False
    if 'best' in in_string:
        split_string = list(in_string.partition('best'))
        for cap in caps:
            if cap in split_string[2]:
                capped = True
                split_string[2] = split_string[2].partition(cap)[0]
        if capped:
            rest_string = split_string[1] + split_string[2]
            rest_string = word_tokenize(rest_string)
            for i in range(len(rest_string)):
                ngram_list.append(rest_string[:i + 1])
    return ngram_list


def valid_award(candidate, ignore_list):
    if candidate[0].lower() != 'best':
        return False
    cand_lower = []
    for c in candidate:
        cand_lower.append(c.lower())
    for iw in ignore_list:
        if iw in cand_lower:
            return False
    if len(candidate) < 3:
        return False
    for punct in string.punctuation.replace('-', '').replace(',', ''):
        for c in candidate:
            if punct in c:
                return False
    tagged = pos_tag(candidate)
    if 'N' not in tagged[-1][1]:
        return False
    if tagged[-1][1] == 'IN' or tagged[-1][1] == 'NNS' or tagged[-1][1] == 'NNPS':
        return False

    return True


ignore = ['who', 'show', 'host', 'for', 'golden', 'globe', 'goldenglobe', 'goldenglobes', 'of', 'dressed', 'fucking',
          "'", 'part', 'red']
cap_words = ['#', ':', 'for', '!', "'", 'http', 'win', 'at', 'nominee', 'award', 'goes', 'is', ',', '-', 'or']


def get_awards(tt):
    ngrams = []
    votes = dict([])
    for t in tt:
        # ngrams += ngrams_right(t, kw_right)
        # ngrams += ngrams_left(t, kw_left)
        ngrams += ngrams_best(t, cap_words)
    # print(ngrams)
    for ng in ngrams:
        if valid_award(ng, ignore):

            ng_str = ' '.join(ng)
            # ng_str = prune_string(ng_str)
            if ng_str in list(votes):
                votes[ng_str] += 1
            else:
                votes[ng_str] = 1
    num_keys = 0
    for key in list(votes):
        if votes[key] > 40:
            num_keys += 1
    return list(votes)


if __name__ == '__main__':
    tweet_text = get_tweets(int(sys.argv[1]))
    get_awards(tweet_text)
