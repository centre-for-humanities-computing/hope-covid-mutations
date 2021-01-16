"""
Purpose: goes through Twitter corpus data and extracts tweets that include mentions of MF, saves them as a separate dataframe

"""

import pandas as pd
import glob
import ndjson
import re
import string

mega_path = glob.glob('../data/mutant*.csv')
i = 0



for file in mega_path:
    
    print(file)
    file_name = re.findall(r'(td.*)\.csv', file)[0]
    
    print(file)
    print("Opening " +  file_name)
          
    df = pd.read_csv(file, lineterminator='\n')
    print(df.head())
    print("Begin processing " +  file_name)
    
    df["b117"] = df["b117"].astype(str)
    df1 = df[df["b117"] != "[]"].drop_duplicates().reset_index(drop=True)
    filename = "../b117_data/b117_" + file_name + ".csv"
    df1.to_csv(filename, index = False)
    
    df["wider"] = df["wider"].astype(str)
    df2 = df[df["wider"] != "[]"].drop_duplicates().reset_index(drop=True)
    filename = "../b117_data/wider_" + file_name + ".csv"
    df2.to_csv(filename, index = False)

    print("Save of " + file_name + " done")
    print("-------------------------------------------\n")
        
    i = i+1