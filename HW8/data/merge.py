import pandas as pd
import numpy as np
import os

#==============================================================================
home = "./"
final_file = "final/Employment_By_Industry.csv"
files = os.listdir(home)
#==============================================================================
#Grab all csv files in the directory
head = ""
dataset_files = []
for file in files:
    if file == home + final_file:
        continue
    if file == "Total.csv":
        head = file
    elif file.endswith(".csv"):
        dataset_files.append(file)


#Create dataframe from Total.csv
head_df = pd.read_csv(home + head)

head_df = head_df.loc[head_df["own_code"] == 5] # 5 is private
head_df = head_df.loc[:, ["area_fips","month1_emplvl"]] #Only keep fips and total employment
head_df = head_df.rename(columns={"area_fips":"fips", "month1_emplvl":"Total"}) #Rename columns
head_df["fips"] = head_df["fips"].astype(str).str.zfill(5) #Pad fips with 0s


#Merge all other csv files into dataframe
columns = []
percent_columns = []
for dataset_file in dataset_files:
    df = pd.read_csv(home + dataset_file) 
    df = df.loc[df["own_code"] == 5] # 5 is private
    df = df.loc[:, ["area_fips","month1_emplvl"]] #Only keep fips and total employment
    df = df.rename(columns={"area_fips":"fips", "month1_emplvl":dataset_file[:-4]}) #Rename columns

    columns.append(dataset_file[:-4]) 
    percent_columns.append(dataset_file[:-4]+"_pct")

    df["fips"] = df["fips"].astype(str).str.zfill(5) #Pad fips with 0s
    head_df = head_df.merge(df, on="fips", how="outer") #Merge
    head_df[dataset_file[:-4]+"_pct"] = head_df[dataset_file[:-4]] / head_df["Total"] #Add percent column

head_df["Largest"] = head_df[columns].idxmax(axis=1) #Add largest column (largest industry by employment)

#Save to csv
head_df.to_csv(home + final_file, index=False)
