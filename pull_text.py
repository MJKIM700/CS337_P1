import json
import pandas as pd

# with open("gg2013.json", "r") as in_file:
#     tweet_data = json.load(in_file)
# tweet_text = []
# for t in tweet_data:
#     tweet_text.append(t['text'])

class Tweet(object):
    def __init__(self, id:int, text:str):
        self.id = id
        self.text = text

    def __str__(self):
        string = 'ID: ' + str(self.id) + '\n'
        string += 'Text: ' + self.text + '\n'
        return string

class Data(object):
    def __init__(self, year):
        name = f'gg{year}.json'
        tweet_data = pd.read_json(name)
        tweets = []
        for index,row in tweet_data.iterrows():
            new_tweet = Tweet(row['id'], row['text'])
            tweets.append(new_tweet)
        self.tweets = tweets.copy()

if __name__ == '__main__':#run python3 pull_text.py if you want to see gg2013.json
    Data(2013)