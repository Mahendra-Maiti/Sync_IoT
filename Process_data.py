from data import *
import pandas as pd


def split_files():
    df=pd.read_csv(DATA_FILE)

    counties=df['County Name'].unique()
    for county in counties:
        print("Processing "+county)
        county_df=df[df['County Name']==county]
        county_measurements=county_df['Sample Measurement']
        file_name=county+".txt"
        county_measurements.to_csv(file_name,index=False,header=False, mode='a')













