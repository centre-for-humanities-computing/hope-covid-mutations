# source /home/commando/covid_19_rbkh/Preprocessing/text_to_x/bin/activate

import text_to_x as ttx
import pandas as pd

sent_df = pd.read_csv("../b117_data.csv")[1:].rename(columns={"0":"created_at", "1":"id", "2":"text", "3":"mettef", "4":"b117", "5":"wider"})


# VADER SENTIMENT
print("Conducting SA with VADER")
tts = ttx.TextToSentiment(lang='da', method="dictionary")
out = tts.texts_to_sentiment(list(sent_df['text'].values))
sent_df = pd.concat([sent_df, out], axis=1)
print("Joining SA results")
#sent_df = sent_df.join(output_long_df)

print(sent_df.head())

filename = "../b117_data_SA.csv"
sent_df.to_csv(filename, index = False)