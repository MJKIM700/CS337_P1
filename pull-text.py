import json

with open("gg2013.json", "r") as in_file:
    tweet_data = json.load(in_file)
tweet_text = []
for t in tweet_data:
    tweet_text.append(t['text'])