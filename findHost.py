from nltk.tag import pos_tag
import pull_text
import string

#tweets = pull_text.Data(year).tweets
#tweets[index].text
#for tweet in tweets:
#    tweet.text

spec_char = ['@', '#', '&']
nono_words = ['golden', 'globe', 'globes', 'Golden', 'Globe', 'Globes', 'goldenglobes', 'GoldenGlobes','RT']


tweets = pull_text.Data(2013).tweets

hostTweetTexts = []
for tweet in tweets:
    if "hosts" in tweet.text:
        if ("should" in tweet.text) or ("next year" in tweet.text):
            pass
        else:
            txt = tweet.text_unchanged.translate(str.maketrans('', '', string.punctuation))
            hostTweetTexts.append(txt)
"""
wfhost = []
for tweet in tweets:
    if "ferrell" in tweet.text and "hosts" in tweet.text: 
        txt = tweet.text.translate(str.maketrans('', '', string.punctuation))
        txt.replace("ferrell", "FERRELL")
        txt.replace("host", "HOST")
        wfhost.append(txt)
print(wfhost)
"""
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
        #i = 0
        #curr = properNouns[i]
        #if len(properNouns) > 1:
        #    while curr != properNouns[-1]:
        #        new_curr = properNouns[i+1]
        #        if any(ele in curr for ele in nono_words):
        #            properNouns.remove(curr)
        #            curr = new_curr
        #        else:
        #            i += 1
        #            curr = properNouns[i]


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

def findHosts(sortedDict):
    lstOfTup = [(k, sortedDict[k]) for k in sorted(sortedDict, key=sortedDict.get, reverse=True)]
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
    print(shortlist)
    shortlistLen = [len(i.split()) for i in shortlist]
    print(shortlistLen)
    single = []
    double = []
    for i in range(len(shortlist)):
        if shortlistLen[i] == 1:
            single.append(shortlist[i])
        if shortlistLen[i] == 2:
            double.append(shortlist[i])
    print(single)
    print(double)
    potentialHost = []
    for i in range(len(single)):
        for j in range(len(single)):
            print('combo is: ' + str(single[i]) +' '+ str(single[j]))
            if str(single[i] +' '+ single[j]) in double:
                firstLast = str(single[i] +' '+ single[j])
                potentialHost.append(firstLast)
                print('inserting pair: ' + firstLast)
    print('potentialHost is: ' + str(potentialHost))
    
    return
"""
    for i in shortlistCopy:

            single.append(shortlist[i])
        else:
            double.append(shortlist[i])
    print(single)
    print(double)
    return
    """
"""
    potentialHosts = []
    for i, j in single:
        for k in double:
            if single[i] in double[k] and single[j] in double[k]:
                if double[k] not in potentialHosts:
                    potentialHosts.append(double[k])
                else: continue
    return potentialHosts
"""
        #if i is a substring of another name and j is a substring of same name,
            #select full name
        #if i[0] is one word, put in one list: singlelst
        #if i[0] is two words, put in another list: doublelst
        #if i and j in singlelst are substrings of k in doublelst:
            #possiblehost.append(doublelst[k])
    
    #print(shortList)


#Tests
"""
string1 = "the host this year is Tina Fey"
string2 = "I loved the host's jokes this year. Tina Fey is so funny."
string3 = "Tina Fey did a great job hosting this year"
string4 = "Fey hosts the golden globes for the first time"
string5 = "the person hosting the golden globes this year will be Tina"
string6 = "doesn't have anything about the h word"

sents = [string1, string2, string3, string4, string5, string6]
print(findProperNouns(sents))
"""

#print(rankProperNouns(hostTweetTexts))

host_votes = rankProperNouns(hostTweetTexts)
#print(sortDict(host_votes))
print(findHosts(host_votes))


