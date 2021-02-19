import pull_text
import sys
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from fuzzywuzzy import fuzz
import spacy

OFFICIAL_AWARDS_1 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_2 = ['cecil b. demille award', 'best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television']
ignore = ['cecil', 'b.', 'demille', 'animated', 'http', 'mad', 'motion', ')', '(', 'at', '"', '``', 'television', 'musical', '“', 'goes', 'screenplay', 'performance', 'i', 'or', 'upset', 'happy', 'sad', 'good', 'bad', 'funny', 'cool', 'awful', 'terrible', 'supporting', 'series', 'these', 'did', 'actor', 'actress', 'oscars', 'even', ',', "n't", 'nominee','tv', 'mini-series', 'miniseries', 'of', '?', 'was', 'get', 'film', 'language', 'comedy', 'drama', 'in', 'are', 'goldenglobes', 'the', 'song', 'original', 'rt', '!', '#', 'for', 'is', 'want', '@', "'", 'best', 'golden', 'globes', 'should', 'have', 'been', '-', ':', 'picture', 'director', '.', 'introduce', 'a', 'an', 'foreign', 'oscar', 'introduces', 'score', 'original', 'he', 'she', 'they', 'and', 'as', "'ve", 'not', 'on', 'oscarnoms', 'ovation']

def handle_high_score(candidate_dict: dict, award: str, tweet: str, score: int):
    if award in candidate_dict:
        if tweet in candidate_dict[award]:
            print('did not put', tweet, 'into', award, 'because it was already in')
            pass
        else:
            candidate_dict[award].append(tweet)
    else:
        candidate_dict[award] = [tweet]
    print('put', tweet, 'into', award, 'because the match score was', score)
    return candidate_dict

def check_people(tokens):
    sp = spacy.load('en_core_web_sm')
    people = []
    detoken = detokenize(tokens)
    sen = sp(detoken)
    for entity in sen.ents:
        if entity.label_ == 'PERSON':
            people.append(entity.text)
    return people

def detokenize(tokens):
    string = ''
    for token in tokens:
        string += token + ' '
    string = string.rstrip(' ')
    return string

def make_string_combinations(tokenized_string: list, direction: str, person: bool):
    combos = []
    count = 0

    while count < len(tokenized_string):
        if tokenized_string[count].lower() in ignore:
            tokenized_string.remove(tokenized_string[count])
            count -= 1
        count += 1
    if person:
        return check_people(tokenized_string)
    if len(tokenized_string) == 0:
        return []
    if direction == 'left':
        tokenized_string.reverse()
    curr_idx = 1
    while curr_idx < len(tokenized_string):
        if direction == 'left' and curr_idx > 1:
            target = tokenized_string[0:curr_idx]
            target.reverse()
            combos.append(detokenize(target))
        else:
            combos.append(detokenize(tokenized_string[0:curr_idx]))
        curr_idx += 1
    return combos

def get_presenters(year):
    key_words = ['presenters', 'presenter', 'presenting', 'presents', 'present']
    tweets = pull_text.Data(year).tweets
    if year == 2013 or year == 2015:
        awards = OFFICIAL_AWARDS_1.copy()
    else:
        awards = OFFICIAL_AWARDS_2.copy()
    # key_words.extend(awards)
    award_candidate_sents = dict()

    for tweet in tweets:
        try:
            cont_nom = False
            for word in key_words:
                if fuzz.partial_token_sort_ratio(word, tweet.text) > 90:#if the tweet doesn't contain one of the key_words, go to the next tweet
                    cont_nom = True
                    break
            if not cont_nom:
                continue
        except:
            continue
        high_match_idx = -1
        high_match_score = -1
        equal_scores = []
        for idx, award in enumerate(awards):
            score = fuzz.token_set_ratio(tweet.text, award)
            if score > high_match_score:
                high_match_idx = idx
                high_match_score = score
                equal_scores = []
            elif score == high_match_score:
                equal_scores.append(awards[high_match_idx])
                high_match_idx = idx
                high_match_score = score
        if high_match_score > 50:
            if len(equal_scores) > 0:
                for candidate in equal_scores:
                    award_candidate_sents = handle_high_score(award_candidate_sents, candidate, tweet.text_unchanged, high_match_score)
            award_candidate_sents = handle_high_score(award_candidate_sents, awards[high_match_idx], tweet.text_unchanged, high_match_score)
    # print(award_candidate_sents)
    final_nominees = dict()
    awards_no_candidates = dict()
    for award in awards:
        bucket = []
        person = True
        if award in award_candidate_sents:
            all_candidates = award_candidate_sents[award]
        else:
            similar_award_candidates = awards.copy()
            similar_award_candidates.remove(award)
            most_similar = ''
            high_score = 0
            for similar in similar_award_candidates:
                score = fuzz.ratio(award, similar)
                if score > high_score:
                    high_score = score
                    most_similar = similar
            awards_no_candidates[award] = most_similar
            continue
        for candidate in all_candidates:
            tokenized = word_tokenize(candidate)
            nom_idx = -1
            for word in key_words:
                for idx, token in enumerate(tokenized):
                    if word == token:
                        nom_idx = idx
                        break
                if nom_idx != -1:
                    break
            if nom_idx == 0 or nom_idx == -1:
                bucket.extend(make_string_combinations(tokenized, 'right', person))
            elif nom_idx == len(tokenized) - 1:
                bucket.extend(make_string_combinations(tokenized, 'left', person))
            else:
                bucket.extend(make_string_combinations(tokenized[0:nom_idx], 'left', person))
                bucket.extend(make_string_combinations(tokenized[nom_idx + 1:], 'right', person))
        final_nominees[award] = bucket
    complete_presenters = dict()
    for award in awards:
        if award in awards_no_candidates:
            use_award = awards_no_candidates[award]
            if use_award in final_nominees:
                bucket = final_nominees[use_award]
            else:
                continue
            dist = FreqDist(bucket)
            common = dist.most_common(4)
            if len(common) > 2:
                complete_presenters[award] = [common[1][0], common[0][0]]
            elif len(common) == 1:
                complete_presenters[award] = [bucket[0]]
            else:
                complete_presenters[award] = []
        else:
            bucket = final_nominees[award]
            dist = FreqDist(bucket)
            common = dist.most_common(3)
            if len(common) > 1:
                complete_presenters[award] = [common[1][0], common[0][0]]
            elif len(common) == 1:
                complete_presenters[award] = [common[0][0]]
            else:
                complete_presenters[award] = []
    print(complete_presenters)
    return complete_presenters




if __name__ == '__main__':
    get_presenters(int(sys.argv[1]))
