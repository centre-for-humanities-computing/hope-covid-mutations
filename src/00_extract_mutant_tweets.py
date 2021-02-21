"""
Purpose: goes through Twitter corpus data and extracts tweets that include mentions of MF, saves them as a separate dataframe

"""

import pandas as pd
import glob
import ndjson
import re
import string

mega_path = glob.glob('/data/001_twitter_hope/preprocessed/da/*.ndjson')

i = 0

remove = string.punctuation
remove = remove.replace("#", "") # don't remove hashtags
pattern = r"[{}]".format(remove) # create the pattern

def retrieve_retweets(row):
    if re.match("^RT", row):
        RT = True
    else:
        RT = False
    return RT

def remove_retweets(data):
    patternDel = "^RT"
    data["text"] = data["text"].astype(str)
    filtering = data['text'].str.contains(patternDel)
    removed_RT = data[~filtering].reset_index(drop=True)
    
    return removed_RT

def extract_usernames(row):
    username_list = list(re.findall(r'@(\S*)\w', row["text"]))
    return username_list

def extract_mettef(row):
    tweet = row["text"].lower()
    substring = "#mettef"
    if substring in tweet:
        mettef = tweet
    else:
        mettef = 0
    return mettef

def extract_britisk_corona(row):
    tweet = row["text"].lower()
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    test_list = ['b117', 'b.1.1.7', 'b1.1.7','britisk corona','britiske corona', "britiske virus","britisk virus", "engelsk mutation", "engelsk variant", "engelsk corona", "super-covid", "super covid", "boris-mutationen"] 
    res = [ele for ele in test_list if(ele in tweet)] 

    return res

def extract_wider(row):
    tweet = row["text"].lower()
    test_list = ["britsik", "mutant", "mutated", "engelsk", "mink", "mutation", "england", "britiske"] 
    res = [ele for ele in test_list if(ele in tweet)] 

    return res


for file in mega_path:
    testset = []
    
    file_name = re.findall(r'(td.*)\.ndjson', file)[0]
    
    print(file)
    print("Opening " +  file_name)
          
    with open(file, 'r') as myfile:
        head=myfile.readlines()

    for i in range(len(head)):
        try:
            testset.extend(ndjson.loads(head[i]))
        except:
            print("err in ", file)
            pass
    
    data = pd.DataFrame(testset)
    del testset
    print("Begin processing " +  file_name)
    
    print(data.head())

    df = remove_retweets(data)
    
    #df = data
    df["b117"] = df.apply(lambda row: extract_britisk_corona(row), axis = 1)
    df["wider"] = df.apply(lambda row: extract_wider(row), axis = 1)

    df = df[["created_at", "id", "text", "b117", "wider"]]# "neg", "neu", "pos", "compound"]]
    #df = df[df["mettef"] != 0].drop_duplicates().reset_index(drop=True)
    
    filename = "../data/mutant_" + file_name + ".csv"
    df.to_csv(filename, index = False)
    print(df.head())

    print("Save of " + file_name + " done")
    print("-------------------------------------------\n")
        
    i = i+1