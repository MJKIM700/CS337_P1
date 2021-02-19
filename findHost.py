from nltk.tag import pos_tag
import pull_text
import string
import sys

nono_words = ['golden', 'globe', 'globes', 'Golden', 'Globe', 'Globes', 'goldenglobes', 'GoldenGlobes','RT']

def tweetData(year):
    tweets = pull_text.Data(year).tweets
    return tweets

def processTweets(tweet_data):
    hostTweetTexts = []
    for tweet in tweet_data:
        if "hosts" in tweet.text:
            if ("should" in tweet.text) or ("next year" in tweet.text):
                pass
            else:
                txt = tweet.text_unchanged.translate(str.maketrans('', '', string.punctuation))
                hostTweetTexts.append(txt)
    return hostTweetTexts

def rankProperNouns(lstOfSent):
    votes = {}
    # loop through each tweet in the list of tweets
    for sentence in lstOfSent:
        # tokenize the tweet into tuples: [('word1', 'TYPE'), ('word2', 'TYPE'), ...]
        tokensWithTags = pos_tag(sentence.split())
        # convert tuples into list
        tWithT_lst = []
        for i in tokensWithTags:
            tWithT_lst.append(list(i))
        # loop through the list of [[word1, TYPE], [word2, TYPE], ... ]
        for i, curr in enumerate(tWithT_lst[:-1]):
            # if a token and the next token are both Proper Nouns: store them in votes as a single First_Last name
            if (curr[1] == 'NNP') and (tWithT_lst[i+1][1] == 'NNP'):
                #if any(nono_words) in curr[0] or any(nono_words) in tWithT_lst[i+1][0]:
                if any(ele in curr[0] for ele in nono_words) or any(ele in tWithT_lst[i+1][0] for ele in nono_words):
                    pass
                else:
                    first_last = curr[0] +' '+ tWithT_lst[i+1][0]
                    if first_last in votes.keys():
                        votes[first_last] += 1
                    else:
                        votes[first_last] = 1
        # make a list of the individual Proper Nouns
        properNouns = [word for word, pos in tokensWithTags if pos == 'NNP'] #makes a list of JUST WORDS, not POS
        for word in properNouns:
            if any(ele in word for ele in nono_words):
                properNouns.remove(word)       
        # if list of Proper Nouns is not empty:
        if properNouns != []:
            # loop through the list of Proper Nouns and store them in votes, updating their value if appropriate
            for pn in properNouns:
                if pn in votes.keys():
                    votes[pn] += 1
                else:
                    votes[pn] = 1
        else: continue
    return votes

#def sortDict(voteDict):
    #return dict(sorted(voteDict.items(), key=lambda item: item[1], reverse=True))

def findHosts(Dict):
    lstOfTup = [(k, Dict[k]) for k in sorted(Dict, key=Dict.get, reverse=True)]
    lstOfLst = []
    for i in lstOfTup:
        lstOfLst.append(list(i))
    shortlist = []
    shortlistwNum = []
    i = 0
    while lstOfLst[i][1] >= 100:
        shortlist.append(lstOfLst[i][0])
        shortlistwNum.append(lstOfLst[i])
        i += 1
    shortlistLen = [len(i.split()) for i in shortlist]
    single = []
    double = []
    for i in range(len(shortlist)):
        if shortlistLen[i] == 1:
            single.append(shortlist[i])
        if shortlistLen[i] == 2:
            double.append(shortlist[i])
    potentialHost = []
    for i in range(len(single)):
        for j in range(len(single)):
            if str(single[i] +' '+ single[j]) in double:
                firstLast = str(single[i] +' '+ single[j])
                potentialHost.append(firstLast)
    dictValues = []
    for i in range(len(potentialHost)):
        dictValues.append(Dict.get(potentialHost[i]))
    host1index = dictValues.index(max(dictValues))
    host1 = potentialHost[host1index]
    sortedValues = [val for val in dictValues]
    sortedValues.sort(reverse=True)
    host2value = sortedValues[1]
    host2index = dictValues.index(host2value)
    if dictValues[host2index] >= float(0.5 * Dict.get(host1)):
        host2 = potentialHost[host2index]
        print('Hosts are: {} and {}'.format(host1, host2))
        return host1, host2
    else:
        print('Host is: {}'.format(host1))
        return host1
    return

if __name__ == '__main__':
    rawData = tweetData(int(sys.argv[1]))
    cleanData = processTweets(rawData)
    host_votes = rankProperNouns(cleanData)
    print(findHosts(host_votes))
