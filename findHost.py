from nltk.tag import pos_tag

def hasHost(array_str):
    with_host = []
    for i in len(array_str):
        if "host" in array_str[i]:
            with_host.append(array_str[i])
    return with_host

def tweetsWithHost(arr_tweetText_tokenized):
    """filters out the tweets without the word host,
    ends up with only tweets that have the word host"""
    with_host = []
    # loop through the array of tweet texts
    for i in range(len(arr_tweetTextTokens)):
        # loop through each token in the tweet texts
        for j in range(len(arr_tweetTextTokens[i])):
            # if host is one of the tokens: put it in the list
            if "host" in arr_tweetTextTokens[i][j]:
                with_host.append(arr_tweetTextTokens[i])
                continue
    return with_host

def find_permutations(arr_tokens, direction):
    """finds the Tip 2 permutations of a list after/before a keyword (host here)"""
    host_index = 0
    for token in arr_tokens:
        if 'host' in token:
            host_index = arr_tokens.index(token)
            break
    if direction == 'right':
        new_arr = arr_tokens[host_index + 1:]
        perms =[new_arr[0]]
        while len(new_arr) >= 2:
            new_arr[0] = new_arr[0] +' '+ new_arr[1]
            new_arr.remove(new_arr[1])
            perms.append(new_arr[0])
        return perms
    if direction == 'left':
        new_arr = arr_tokens[0:host_index]
        perms = [new_arr[-1]]
        while len(new_arr) >= 2:
            new_arr[-1] = new_arr[-2] +' '+ new_arr[-1]
            new_arr.remove(new_arr[-2])
            perms.append(new_arr[-1])
        return perms

def intersect(lst1, lst2):
    """finds the common strings in two lists"""
    set1 = set(lst1)
    return set1.intersection(lst2)

def votes(lstOfPermLists):
    #vote_tracker is a dict with keys = perms, values = num of votes
    vote_tracker = {}
    for lst in lstOfPernLists:
        for perm in lst:
            #if the perm is already in vote_tracker: increase num of votes for that perm
            if perm in vote_tracker.keys():
                vote_tracker[perm] += 1
            #if the perm is not in vote_tracker: include it and set vote to 1
            else:
                vote_tracker[perm] = 1


def findProperNouns(lstOfSent):
    votes = {}
    # loop through each tweet in the list of tweets
    for sentence in lstOfSent:
        # tokenize the tweet into tuples: [('word1', 'TYPE'), ('word2', 'TYPE'), ...]
        tokensWithTags = pos_tag(sentence.split())
        # convert tuples into list
        tWithT_lst = []
        for i in tokensWithTags:
            tWithT_lst.append(list(i))
        print('tWithT is: ' + str(tWithT_lst))
        # loop through the list of [[word1, TYPE], [word2, TYPE], ... ]
        for i, j in enumerate(tWithT_lst[:-1]):
            # if a token and the next token are both Proper Nouns: store them in votes as a single First_Last name
            if (j[1] == 'NNP') and (tWithT_lst[i+1][1] == 'NNP'):
                first_last = j[0] +' '+ tWithT_lst[i+1][0]
                if first_last in votes.keys():
                    votes[first_last] += 1
                else:
                    votes[first_last] = 1
            # make a list of the individual Proper Nouns
            properNounsTup = [word for word, pos in tokensWithTags if pos == 'NNP'] #makes a list of JUST WORDS, not POS
            print('properNounsTup is: ' + str(properNounsTup))
            # if list of Proper Nouns is not empty:
            if properNounsTup != []:
                # loop through the list of Proper Nouns and store them in votes, updating their value if appropriate
                for k, l in enumerate(properNounsTup):
                    if l in votes.keys():
                        print('l is in dict and is: ' + l)
                        #print('l[0] is in dict and is: ' + l[0])
                        votes[l] += 1
                    else:
                        print('l is not in dict and is: ' + l)
                        #print('l[0] is not in dict and is: ' + l[0])
                        votes[l] = 1
            else: continue
    # return the votes dictionary
    return votes
                    

def PNVotes(lstOfSentences):
    votes = {}
    #PNs = []
    for sentence in lstOfSentences:
        PNsInSent = findProperNouns(sentence)
        print(PNsInSent)
        for pn in PNsInSent:
            if pn in votes.keys():
                votes[pn] += 1
            else:
                votes[pn] = 1
    return votes


#Tests

string1 = "the host this year is Tina Fey"
string2 = "I loved the host's jokes this year. Tina Fey is so funny."
string3 = "Tina Fey did a great job hosting this year"
string4 = "Fey hosts the golden globes for the first time"
string5 = "the person hosting the golden globes this year will be Tina"
string6 = "doesn't have anything about the h word"

sents = [string1, string2, string3, string4, string5, string6]

#print(PNVotes(sents))
print(findProperNouns(sents))

#tuplst = [(1,2), ('a','b'), ("hello","bye"), ([], [1, 2, 3])]
#for index, tuple in enumerate(tuplst):
#    pn = tuple[0]
#    typ = tuple[1]
#    print(tuple[0])
#arr = []
#for i in tuplst:
#    arr.append(tuplst[i][1])
#print(arr)
#arr = []
#for i in tuplst:
#    arr.append(list(i))
#print(arr)
#arr2 = []
#for i, j in enumerate(arr[:-1]):
#    if j[1] != arr[i+1][1]:
#        arr2.append(j)
#print(arr2)



tokens1 = string1.lower().split()
tokens2 = string2.lower().split()
tokens3 = string3.lower().split()
tokens4 = string4.lower().split()
tokens5 = string5.lower().split()
tokens6 = string6.lower().split()

"""
for i in range(1,7):
    print(vars()['tokens' + str(i)])
"""

#lst = strWithHost(arr_of_tokens)

#print('\n\n')
#for i in range(len(lst)):
#    print(lst[i])
#    print('\n') 

#print('\n' + 'there are {} sentences with the word host'.format(len(lst)))



#arrOfTokensR = ["tonight", "the", "host", "ale", "cardozo", "will", "speak"]
#arrOfTokensL = ["that", "was", "great", "ale", "cardozo", "hosted", "well"]

#print(find_permutations(arrOfTokensR, 'right'))
#print(find_permutations(arrOfTokensL, 'left'))

#perms1 = find_permutations(arrOfTokensR, 'right')
#perms2 = find_permutations(arrOfTokensL, 'left')

#print(intersect(perms1, perms2))

#arr_of_tokens = [tokens1, tokens2, tokens3, tokens4, tokens5, tokens6]


