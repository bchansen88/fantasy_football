import pandas as pd
from os import listdir
import os


def find_csv_file(path_to_dir, suffix = '', data = ''):

    files = listdir(path_to_dir)
    files = [file for file in files if file.endswith(suffix)]
    for f in files:
        return f if f.find(data) != -1 else None

def split_positions(df, pos, column):

    df = df.loc[df[column] == pos]
    return df 
