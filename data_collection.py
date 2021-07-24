import pandas as pd
import os
from ffurl_db import *
from dfs_utility import *
from season_calc import season_calc
from fanduel_read import fanduel_structure
import numpy as np

#variable checks
year = season_calc()
#year = '2019'
print('Collecting data for the {} season'.format(year))
here = os.getcwd()
off_dir = here + '/offense/'
def_dir = here + '/defense/'
fanduel = find_csv_file(here, suffix = '.csv', data = 'FanDuel')

#fanduel data frame
fdf = pd.read_csv(fanduel)

def directory_check():

    if not os.path.exists(def_dir):
        #os.makedirs(off_dir)
        os.makedirs(def_dir)

directory_check()

def defense_collect(url, stat):

    url = url.format(year)
    stat = def_dir + stat + '.csv'
    de = split_positions(fdf, 'D', 'Position')
    fanduel = fanduel_structure(de)
    fanduel.rename(columns={'Player': 'Tm'}, inplace=True)
    fanduel = fanduel.reindex(columns=['Team','Tm', 'Opp', 'Game', 'Salary'])
    df = pd.read_html(url, header=1)
    df2 = pd.read_html(url)

    #base defensive dataframe
    adv = df[0]
    adv['Pass Ply %'] = (adv['Att']/adv['Ply']).round(3)
    adv['1stD %'] = (adv['1stD'] / adv['Ply']).round(3)
    adv['Yds/Pen'] = (adv['Yds.3'] / adv['Pen']).round(3)
    adv['1stD/Pen %'] = (adv['1stPy'] / adv['Ply']).round(3)
    adv['Cmp %'] = (adv['Cmp']/adv['Att']).round(3)
    adv['Pass Yds/Att'] = (adv['Yds.1']/adv['Att']).round(3)
    adv['Pass TD %'] = (adv['TD']/adv['Att']).round(2)
    adv['Int %'] = (adv['Int']/adv['Att']).round(2)
    adv['1stD/Pass %'] = (adv['1stD.1']/adv['Att']).round(2)
    adv['Rush Ply %'] = (adv['Att.1']/adv['Ply']).round(2)
    adv['Rush Yds/Att'] = (adv['Yds.2']/adv['Att.1']).round(2)
    adv['Rush TD %'] = (adv['TD.1']/adv['Att.1']).round(2)
    adv['1stD/Rush %'] = (adv['1stD.2']/adv['Att.1']).round(2)
    adv = adv.rename(columns={'Att': 'Pass Att', 'Yds.1': 'Pass Yds', 'TD': 'Pass TD', '1stD.1': 'Pass 1stD', 'Att.1': 'Rush Att', 'Yds.2': 'Rush Yds', 'TD.1': 'Rush TD', \
                              '1stD.2': 'Rush 1stD'})
    adv = adv[['Tm', 'Yds', 'Ply', '1stD %', 'Sc%', 'TO%', 'EXP', 'Y/P', 'Pass Ply %', 'Pass Att', 'Cmp %', 'Pass Yds', 'NY/A', 'Pass TD', 'Pass TD %', 'Int', 'Int %', \
               'Pass 1stD', '1stD/Pass %', 'Rush Ply %', 'Rush Att', 'Rush Yds', 'Rush Yds/Att', 'Rush TD', 'Rush TD %', 'Rush 1stD', '1stD/Rush %']]

    #advanced passing
    padv = df2[1]
    padv = padv[['Tm', 'DADOT', 'Air', 'YAC', 'Bltz', 'Bltz%', 'Hrry', 'Hrry%', 'QBKD', 'QBKD%', 'Sk', 'Prss', 'Prss%']]

    adv = pd.merge(fanduel, adv, how="outer", on=["Tm"])
    adv = pd.merge(adv, padv, how='outer', on=['Tm'])
    adv['Game'].replace('', np.nan, inplace=True)
    adv.dropna(subset=['Game'], inplace=True)
    adv.to_csv(def_dir + 'Advanced Defense.csv', index=False)

def rb_points_against(url):

    url = url.format(year)
    #stat = def_dir + stat + '.csv'
    de = split_positions(fdf, 'D', 'Position')
    fanduel = fanduel_structure(de)
    fanduel.rename(columns={'Player': 'Tm'}, inplace=True)
    fanduel = fanduel.reindex(columns=['Team','Tm', 'Opp', 'Game', 'Salary'])
    rb = pd.read_html(url, header=1)
    df = rb[0]

    df['Att/G'] = (df['Att']/df['G']).round(2)
    df['Yds/Att'] = (df['Yds']/df['Att']).round(2)
    df['TD/Att'] = (df['TD']/df['Att']).round(3)
    df['FDPt/Att'] = (df['FDPt']/df['Att']).round(2)
    df['Tgt/G'] = (df['Tgt']/df['G']).round(2)
    df['Cmp %'] = (df['Rec']/df['Tgt']).round(2)
    df['Rec Yds/Rec'] = (df['Yds.1']/df['Rec']).round(2)
    df['TD/Rec'] = (df['TD.1']/df['Rec']).round(3)
    df['FDPt/Rec'] = (df['FDPt']/df['Rec']).round(2)

    df = df.rename(columns={'Yds.1': 'Rec Yds', 'TD.1': 'Rec TDs', 'FDPt.1': 'FDPt/G'})
    df = df[['Tm', 'Att', 'Att/G', 'Yds', 'Yds/Att', 'TD', 'TD/Att', 'FDPt/Att', 'Tgt', 'Rec', 'Cmp %', 'Tgt/G', 'Rec Yds', 'Rec Yds/Rec', 'Rec TDs', 'TD/Rec', 'FDPt/Rec', 'FDPt/G']]


    print(df.head())
    df.to_csv(def_dir + 'rb_ptsAllowed.csv', index=False)

def qb_points_against(url):

    url = url.format(year)
    qb = pd.read_html(url, header=1)
    df = qb[0]

    df['Att/G'] = (df['Att']/df['G']).round(2)
    df['Cmp%'] = (df['Cmp']/df['Att']).round(3)
    df['Yds/Att'] = (df['Yds']/df['Att']).round(2)
    df['TD/Att'] = (df['TD']/df['Att']).round(3)
    df['Int/Att'] = (df['Int']/df['Att']).round(3)
    df['Sk/Att'] = (df['Sk']/(df['Att']+df['Sk'])).round(3)
    df['FDPt/Att'] = (df['FDPt']/df['Att']).round(2)

    df = df.rename(columns={'FDPt.1': 'FDPt/G'})
    df = df[['Tm', 'Att', 'Att/G', 'FDPt/Att', 'Cmp%', 'Yds', 'Yds/Att', 'TD', 'TD/Att', 'Int', 'Int/Att', 'Sk', 'Sk/Att', 'FDPt/G']]

    print(df.head())
    df.to_csv(def_dir + 'qb_ptsAllowed.csv', index=False)

def wr_points_against(url):

    url = url.format(year)
    wr = pd.read_html(url, header=1)
    df = wr[0]

    df['Tgt/G'] = (df['Tgt']/df['G']).round(2)
    df['Rec %'] = (df['Rec']/df['Tgt']).round(3)
    df['Yds/Tgt'] = (df['Yds']/df['Tgt']).round(2)
    df['TD/Tgt'] = (df['TD']/df['Tgt']).round(3)
    df['FDPt/Tgt'] = (df['FDPt']/df['Tgt']).round(2)

    df = df.rename(columns={'FDPt.1': 'FDPt/G'})
    df = df[['Tm', 'Tgt', 'Tgt/G', 'FDPt/Tgt', 'Rec %', 'Yds', 'Yds/Tgt', 'TD', 'TD/Tgt', 'FDPt/G']]

    print(df.head())
    df.to_csv(def_dir + 'wr_ptsAllowed.csv', index=False)

def te_points_against(url):

    url = url.format(year)
    te = pd.read_html(url, header=1)
    df = te[0]

    df['Tgt/G'] = (df['Tgt']/df['G']).round(2)
    df['Rec %'] = (df['Rec']/df['Tgt']).round(3)
    df['Yds/Tgt'] = (df['Yds']/df['Tgt']).round(2)
    df['TD/Tgt'] = (df['TD']/df['Tgt']).round(3)
    df['FDPt/Tgt'] = (df['FDPt']/df['Tgt']).round(2)

    df = df.rename(columns={'FDPt.1': 'FDPt/G'})
    df = df[['Tm', 'Tgt', 'Tgt/G', 'FDPt/Tgt', 'Rec %', 'Yds', 'Yds/Tgt', 'TD', 'TD/Tgt', 'FDPt/G']]

    print(df.head())
    df.to_csv(def_dir + 'te_ptsAllowed.csv', index=False)

defense_collect(def_advanced, 'def_advanced')
rb_points_against(pfr_rb)
qb_points_against(pfr_qb)
wr_points_against(pfr_wr)
te_points_against(pfr_te)
