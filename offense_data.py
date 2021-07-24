import pandas as pd
import os
from ffurl_db import *
from dfs_utility import *
from season_calc import season_calc
from fanduel_read import fanduel_structure
import numpy as np
import re
#variable checks
year = season_calc()
#year = '2019'
print('Collecting data for the {} season'.format(year))
here = os.getcwd()
off_dir = here + '/offense/'
fanduel = find_csv_file(here, suffix = '.csv', data = 'FanDuel')

#fanduel data frame
fdf = pd.read_csv(fanduel)

def directory_check():

    if not os.path.exists(off_dir):
        os.makedirs(off_dir)

directory_check()

def qb_collect(url, fanDf):

    url = url.format(year)
    stat = off_dir + 'qb_stats' + '.csv'
    fdf = split_positions(fanDf, 'QB', 'Position')
    fanDuel = fanduel_structure(fdf)


    df = pd.read_html(url, header=1)
    qb = df[0]
    char = re.compile(r'\d*')
    #qb['Player'] = qb['Player'].replace(char, '', regex=True, inplace=True)
    qb['Player'] = qb['Player'].map(lambda x: x.rstrip(r' *+'))
    qb = split_positions(qb, 'QB', 'FantPos')

    qb = qb.apply(pd.to_numeric, errors="ignore")

    qb['Pass Att/G'] = (qb['Att']/qb['G']).round(2)
    qb['Cmp %'] = (qb['Cmp']/qb['Att']).round(3)
    qb['Pass Yds/Att'] = (qb['Yds']/qb['Att']).round(2)
    qb['Pass TD/Att'] = (qb['TD']/qb['Att']).round(3)
    qb['Int/Att'] = (qb['Int']/qb['Att']).round(3)
    qb['Rush Att/G'] = (qb['Att.1']/qb['G']).round(2)
    qb['Rush Yds/Att'] = (qb['Yds.1']/qb['Att.1']).round(2)
    qb['Rush TD/Att'] = (qb['TD.1']/qb['Att.1']).round(3)
    qb['Volume/G'] = ((qb['Att'] + qb['Att.1'])/qb['G']).round(2)
    qb['Total Yds/Att']=((qb['Yds'] + qb['Yds.1'])/(qb['Att'] + qb['Att.1'])).round(3)
    qb['Total TD/Att'] = ((qb['TD']+qb['TD.1'])/(qb['Att'] + qb['Att.1'])).round(3)
    qb['TO%'] = ((qb['Int']+qb['FL'])/(qb['Att'])+qb['Att.1']).round(3)
    qb['FDPt/Att'] = (qb['FDPt']/(qb['Att'] + qb['Att.1'])).round(2)
    qb['FDPt/G'] = (qb['FDPt']/qb['G']).round(2)
    qb = qb.rename(columns={'Att': 'Pass Att', 'Yds': 'Pass Yds', 'TD': 'Pass TD', 'Att.1': 'Rush Att', 'Yds.1': 'Rush Yds', 'Y/A': 'Rush Yds/Att', 'TD.1': 'Rush TD'})

    qb = qb[['Player', 'Pass Att/G', 'Cmp %', 'Pass Yds', 'Pass Yds/Att', 'Pass TD', 'Pass TD/Att', 'Int/Att', 'Rush Att/G', 'Rush Yds', 'Rush Yds/Att', 'Rush TD', 'Rush TD/Att',\
             'Volume/G', 'Total Yds/Att', 'Total TD/Att', 'TO%', 'FDPt/Att', 'FDPt/G']]

    qb = pd.merge(fanDuel, qb, how="outer", on=["Player"])
    qb = qb[qb['Pass Att/G'].notna()]
    qb.to_csv(stat, index=False)
    print(qb.head(5))

def rb_collect(url, fanDf):

    url = url.format(year)
    stat = off_dir + 'rb_stats' + '.csv'
    fdf = split_positions(fanDf, 'RB', 'Position')
    fanDuel = fanduel_structure(fdf)

    df = pd.read_html(url, header=1)
    rb = df[0]
    rb['Player'] = rb['Player'].map(lambda x: x.rstrip(' *+'))
    rb = split_positions(rb, 'RB', 'FantPos')

    rb = rb.apply(pd.to_numeric, errors="ignore")

    rb['Rush Att/G'] = (rb['Att.1']/rb['G']).round(2)
    rb['Rush TD/Att'] = (rb['TD.1']/rb['Att.1']).round(3)
    rb['Tgt/G'] = (rb['Tgt']/rb['G']).round(2)
    rb['Rec %'] = (rb['Rec']/rb['Tgt']).round(3)
    rb['Rec Yds/Tgt'] = (rb['Yds.2']/rb['Tgt']).round(2)
    rb['Rec TD/Tgt'] = (rb['TD.2']/rb['Tgt']).round(3)
    rb['Volume/G'] = ((rb['Tgt'] + rb['Att.1'])/rb['G']).round(2)
    rb['Total Yds/Att']=((rb['Yds.1'] + rb['Yds.2'])/(rb['Att.1'] + rb['Tgt'])).round(2)
    rb['Total TD/Att'] = ((rb['TD.1']+rb['TD.2'])/(rb['Att.1'] + rb['Tgt'])).round(3)
    rb['FDPt/Att'] = (rb['FDPt']/(rb['Att.1'] + rb['Tgt'])).round(2)
    rb['FDPt/G'] = (rb['FDPt']/rb['G']).round(2)
    rb = rb.rename(columns={'Att.1': 'Rush Att', 'Yds.1': 'Rush Yds', 'TD.1': 'Rush TD', 'Yds.2': 'Rec Yds', 'Y/A': 'Rush Yds/Att', 'TD.2': 'Rec TD', 'Y/R': 'Yds/Rec'})

    rb = rb[['Player', 'Rush Att/G', 'Rush Yds', 'Rush Yds/Att', 'Rush TD', 'Rush TD/Att', 'Tgt/G', 'Rec %', 'Rec Yds/Tgt', 'Rec TD/Tgt', 'Yds/Rec', 'Volume/G', 'Total Yds/Att',\
             'Total TD/Att', 'FDPt/Att', 'FDPt/G']]

    rb = pd.merge(fanDuel, rb, how="outer", on=["Player"])
    rb = rb[rb['Rush Att/G'].notna()]
    rb.to_csv(stat, index=False)
    print(rb.head(5))

def wr_collect(url, fanDf):

    url = url.format(year)
    stat = off_dir + 'wr_stats' + '.csv'
    fdf = split_positions(fanDf, 'WR', 'Position')
    fanDuel = fanduel_structure(fdf)

    df = pd.read_html(url, header=1)
    wr = df[0]
    wr['Player'] = wr['Player'].map(lambda x: x.rstrip(' *+'))
    wr = split_positions(wr, 'WR', 'FantPos')

    wr = wr.apply(pd.to_numeric, errors="ignore")

    wr['Tgt/G'] = (wr['Tgt']/wr['G']).round(2)
    wr['Rec %'] = (wr['Rec']/wr['Tgt']).round(3)
    wr['Rec Yds/Tgt'] = (wr['Yds.2']/wr['Tgt']).round(2)
    wr['Rec TD/Tgt'] = (wr['TD.2']/wr['Tgt']).round(3)
    wr['FDPt/Att'] = (wr['FDPt']/(wr['Att.1'] + wr['Tgt'])).round(2)
    wr['FDPt/G'] = (wr['FDPt']/wr['G']).round(2)
    wr = wr.rename(columns={'Yds.2': 'Rec Yds', 'TD.2': 'Rec TD', 'Y/R': 'Yds/Rec'})

    wr = wr[['Player', 'Tgt/G', 'Rec %', 'Rec Yds', 'Rec Yds/Tgt', 'Rec TD', 'Rec TD/Tgt', 'Yds/Rec', 'FDPt/Att', 'FDPt/G']]

    wr = pd.merge(fanDuel, wr, how="outer", on=["Player"])
    wr = wr[wr['Tgt/G'].notna()]
    wr.to_csv(stat, index=False)
    print(wr.head(5))

def te_collect(url, fanDf):

    url = url.format(year)
    stat = off_dir + 'te_stats' + '.csv'
    fdf = split_positions(fanDf, 'TE', 'Position')
    fanDuel = fanduel_structure(fdf)

    df = pd.read_html(url, header=1)
    te = df[0]
    te['Player'] = te['Player'].map(lambda x: x.rstrip(' *+'))
    te = split_positions(te, 'TE', 'FantPos')

    te = te.apply(pd.to_numeric, errors="ignore")

    te['Tgt/G'] = (te['Tgt']/te['G']).round(2)
    te['Rec %'] = (te['Rec']/te['Tgt']).round(3)
    te['Rec Yds/Tgt'] = (te['Yds.2']/te['Tgt']).round(2)
    te['Rec TD/Tgt'] = (te['TD.2']/te['Tgt']).round(3)
    te['FDPt/Att'] = (te['FDPt']/(te['Att.1'] + te['Tgt'])).round(2)
    te['FDPt/G'] = (te['FDPt']/te['G']).round(2)
    te = te.rename(columns={'Yds.2': 'Rec Yds', 'TD.2': 'Rec TD', 'Y/R': 'Yds/Rec'})

    te = te[['Player', 'Tgt/G', 'Rec %', 'Rec Yds', 'Rec Yds/Tgt', 'Rec TD', 'Rec TD/Tgt', 'Yds/Rec', 'FDPt/Att', 'FDPt/G']]

    te = pd.merge(fanDuel, te, how="outer", on=["Player"])
    te = te[te['Tgt/G'].notna()]
    te.to_csv(stat, index=False)
    print(te.head(5))

qb_collect(fantasy, fdf)
rb_collect(fantasy, fdf)
wr_collect(fantasy, fdf)
te_collect(fantasy, fdf)
