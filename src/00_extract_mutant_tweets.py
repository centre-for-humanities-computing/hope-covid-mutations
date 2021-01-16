"""
Purpose: goes through Twitter corpus data and extracts tweets that include mentions of MF, saves them as a separate dataframe

"""

import pandas as pd
import glob
import ndjson
import re
import string

#mega_path = glob.glob('/data/001_twitter_hope/preprocessed/da/*2021*.ndjson')
#mega_path = glob.glob('/data/001_twitter_hope/preprocessed/da/*202012*.ndjson')
mega_path = glob.glob('/data/001_twitter_hope/preprocessed/da/*.ndjson')
#glob.glob('/home/commando/data_processed/megafiles/da_created_october2020/ultimate_megafile_pieces/*.ndjson')

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

def remove_retweets(ori_data):
    patternDel = "^RT"
    data["text"] = data["text"].astype(str)
    filtering = data['text'].str.contains(patternDel)
    removed_RT = ori_data[~filtering].reset_index(drop=True)
    
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
    test_list = ['b117', 'britisk corona', "mutation", "britiske virus", "engelsk mutation", "engelsk variant",
                "super-covid"] 
    res = [ele for ele in test_list if(ele in tweet)] 

    return res

def extract_wider(row):
    tweet = row["text"].lower()
    test_list = ["britsik", "mutant", "mutation", "mutated", "engelsk"] 
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
    df["mettef"] = df.apply(lambda row: extract_mettef(row), axis = 1)
    df["b117"] = df.apply(lambda row: extract_britisk_corona(row), axis = 1)
    df["wider"] = df.apply(lambda row: extract_wider(row), axis = 1)

    df = df[["created_at", "id", "text", "mettef", "b117", "wider"]]# "neg", "neu", "pos", "compound"]]
    #df = df[df["mettef"] != 0].drop_duplicates().reset_index(drop=True)
    
    filename = "../data/mutant_" + file_name + ".csv"
    df.to_csv(filename, index = False)
    print(df.head())

    print("Save of " + file_name + " done")
    print("-------------------------------------------\n")
        
    i = i+1