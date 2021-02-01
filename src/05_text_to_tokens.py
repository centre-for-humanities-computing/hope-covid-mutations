# source /home/commando/covid_19_rbkh/Preprocessing/text_to_x/bin/activate

import text_to_x as ttx
import pandas as pd

import re
import string
def remove_mentions(row):
    tweet = row["text"]
    clean_tweet = re.sub(r'@(\S*)\w', '', tweet)
    # Remove URLs
    url_pattern = re.compile(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
    clean_tweet = re.sub(url_pattern, '', clean_tweet)
    
    clean_tweet = clean_tweet.translate(str.maketrans('', '', string.punctuation))
    clean_tweet = clean_tweet.lower()
    return clean_tweet

df = pd.read_csv("../b117_data_SA.csv")#[1:].rename(columns={"0":"created_at", "1":"id", "2":"text", "3":"mettef", "4":"b117", "5":"wider",
df = df.dropna()
df["mentioneless_text"] = df.apply(lambda row: remove_mentions(row), axis = 1)

print(df.head())

#ttt = ttx.TextToTokens()
ttt = ttx.TextToTokens(lang = ["da", "da", "da"],
                                tokenize="stanza",
                                lemmatize="stanza",
                                stemming=None,
                                pos="stanza",
                                mwt="stanza",
                                depparse="stanza",
                                ner="stanza")
out = ttt.texts_to_tokens(list(df['mentioneless_text'].values))

sent_df = pd.concat([df, out], axis=1)

print(sent_df.head())

filename = "../b117_data_SA_tokens.csv"
sent_df.to_csv(filename, index = False)

# broken af send help??????