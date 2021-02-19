from nltk.tag import pos_tag
import pull_text



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
        # loop through the list of [[word1, TYPE], [word2, TYPE], ... ]
        for i, curr in enumerate(tWithT_lst[:-1]):
            # if a token and the next token are both Proper Nouns: store them in votes as a single First_Last name
            if (curr[1] == 'NNP') and (tWithT_lst[i+1][1] == 'NNP'):
                first_last = curr[0] +' '+ tWithT_lst[i+1][0]
                if first_last in votes.keys():
                    votes[first_last] += 1
                else:
                    votes[first_last] = 1
        # make a list of the individual Proper Nouns
        properNouns = [word for word, pos in tokensWithTags if pos == 'NNP'] #makes a list of JUST WORDS, not POS
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


#Tests

string1 = "the host this year is Tina Fey"
string2 = "I loved the host's jokes this year. Tina Fey is so funny."
string3 = "Tina Fey did a great job hosting this year"
string4 = "Fey hosts the golden globes for the first time"
string5 = "the person hosting the golden globes this year will be Tina"
string6 = "doesn't have anything about the h word"

sents = [string1, string2, string3, string4, string5, string6]
print(findProperNouns(sents))

