import pandas as pd
import os
from ffurl_db import *
from season_calc import season_calc

#variable checks
year = season_calc()
here = os.getcwd()
raw_dir = here + '\\raw_data'
def_dir = raw_dir + '\\defense\\{}'.format(year)
off_dir = raw_dir + '\\offense\\{}'.format(year)

def directory_check():

    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)
        os.makedirs(off_dir)
        os.makedirs(def_dir)

directory_check()

def defense_collect(url, stat):

    url = url.format(year)
    stat = stat + '.csv'

    df = pd.read_html(url)
    df = df[0].dropna(axis=0, thresh=4)
    df.to_csv(stat, index=False)

defense_collect(fo_def, 'defensive efficiency')