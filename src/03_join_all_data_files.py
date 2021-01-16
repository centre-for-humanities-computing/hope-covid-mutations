"""
Join the 00-10 files into one file
"""

import glob
import pandas as pd

### Define Functions ###

def get_df(filenames):
    df = pd.read_csv(filenames[0], header=None)

    for file in filenames[1:]:
        df_0 = pd.read_csv(file, header = None)
        df = df.append(df_0)

    df = df.drop_duplicates()

    return df

def clean_dates(df):
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

## Run these functions
if __name__ == "__main__":
    filenames_dec = glob.glob("../data/MF_td_202012*.csv")
    filenames_jan = glob.glob("../data/MF_td_2021*.csv")

    filename_dec = "../tweet_volume_data/dec_data.csv"
    filename_jan = "../tweet_volume_data/jan_data.csv"
    
    print("Get data")
    df_dec = get_df(filenames_dec)
    df_jan = get_df(filenames_jan)
    #print("Start cleaning dates")
    #df = clean_dates(df)
    print("Save file")
    df_dec.to_csv(filename_dec, index=False)
    df_jan.to_csv(filename_jan, index=False)
    del df
    