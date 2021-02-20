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
        if "host" in tweet.text:
            if ("should" in tweet.text) or ("next year" in tweet.text):
                pass
            else:
                txt = tweet.text_unchanged.translate(str.maketrans('', '', string.punctuation))
                hostTweetTexts.append(txt)
    return hostTweetTexts

def rankProperNouns(lstOfSent):
    """takes the text from tweets and ranks the Proper Nouns by the number of times they appear"""
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

def findHosts(Dict):
    """takes a dictionary w/ Proper Nouns as keys and votes as values, returns the host(s)"""
    # convert the dictionary of votes to a list of tuples
    lstOfTup = [(k, Dict[k]) for k in sorted(Dict, key=Dict.get, reverse=True)]
    # convert the list of tuples [(key, value), ... ] to a list of lists [[key, value], ... ]
    lstOfLst = []
    for i in lstOfTup:
        lstOfLst.append(list(i))
    # shorten the list to the proper nouns with 100+ votes
    shortlist = []
    shortlistwNum = []
    i = 0
    while lstOfLst[i][1] >= 100:
        shortlist.append(lstOfLst[i][0])
        shortlistwNum.append(lstOfLst[i])
        i += 1
    shortlistLen = [len(i.split()) for i in shortlist]
    # separate proper nouns into two lists: single holds single-word nouns, double holds two-word nouns
    single = []
    double = []
    for i in range(len(shortlist)):
        if shortlistLen[i] == 1:
            single.append(shortlist[i])
        if shortlistLen[i] == 2:
            double.append(shortlist[i])
    # loop through single and get every possible pair combo of two proper nouns
    # if any of these pairs match a two-word key, it might be a first and last name
    # store combos of first and last name that match two-word keys in potentialHost
    potentialHost = []
    for i in range(len(single)):
        for j in range(len(single)):
            if str(single[i] +' '+ single[j]) in double:
                firstLast = str(single[i] +' '+ single[j])
                potentialHost.append(firstLast)
    # compare the number of votes between the top two 2-word (first-last name) keys
    dictValues = []
    for i in range(len(potentialHost)):
        dictValues.append(Dict.get(potentialHost[i]))
    host1index = dictValues.index(max(dictValues))
    # host1 is the first+last name with most votes
    host1 = potentialHost[host1index]
    sortedValues = [val for val in dictValues]
    sortedValues.sort(reverse=True)
    host2value = sortedValues[1]
    host2index = dictValues.index(host2value)
    # if the first+last name with second most votes has at least 50% 
    # as many votes as the first+last name with the most votes,
    # the first+last name with 2nd most votes may be 2nd host
    if dictValues[host2index] >= float(0.5 * Dict.get(host1)):
        host2 = potentialHost[host2index]
        #print('Hosts are: {} and {}'.format(host1, host2))
        return [host1, host2]
    else:
        #print('Host is: {}'.format(host1))
        return [host1]
    return

def runHosts(year):
    rawData = tweetData(year)
    cleanData = processTweets(rawData)
    host_votes = rankProperNouns(cleanData)
    host_s = findHosts(host_votes)
    return host_s
    

if __name__ == '__main__':
    runHosts(int(sys.argv[1]))
    #output = runHosts(int(sys.argv[1]))
    #if len(output) == 1:
        #print('host is: ' + str(output))
    #if len(output) == 2:
        #print('hosts are {} and {}'.format(str(output[0]), str(output[1])))
