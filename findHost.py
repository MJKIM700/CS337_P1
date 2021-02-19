
string1 = "the host this year is ale cardozo"
string2 = "I loved the host's jokes this year. ale cardozo is so funny."
string3 = "ale cardozo did a great job hosting this year"
string4 = "cardozo hosts the golden globes for the first time"
string5 = "the person hosting the golden globes this year will be ale"
string6 = "doesn't have anything about the h word"

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

#arrOfTokensR = ["tonight", "the", "host", "ale", "cardozo", "will", "speak"]
#arrOfTokensL = ["that", "was", "great", "ale", "cardozo", "hosted", "well"]

#print(find_permutations(arrOfTokensR, 'right'))
#print(find_permutations(arrOfTokensL, 'left'))

#perms1 = find_permutations(arrOfTokensR, 'right')
#perms2 = find_permutations(arrOfTokensL, 'left')

print(intersect(perms1, perms2))

#arr_of_tokens = [tokens1, tokens2, tokens3, tokens4, tokens5, tokens6]




#lst = strWithHost(arr_of_tokens)

#print('\n\n')
#for i in range(len(lst)):
#    print(lst[i])
#    print('\n') 

#print('\n' + 'there are {} sentences with the word host'.format(len(lst)))
