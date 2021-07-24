import pandas as pd
from dfs_utility import *
import os

here = os.getcwd()

fanduel = find_csv_file(here, suffix = '.csv', data = 'FanDuel')

df = pd.read_csv(fanduel)

qb = split_positions(df, 'QB', 'Position')
rb = split_positions(df, 'RB', 'Position')
wr = split_positions(df, 'WR', 'Position')
te = split_positions(df, 'TE', 'Position')
de = split_positions(df, 'D', 'Position')

def fanduel_structure(df):

    df.rename(columns={'Nickname': 'Player', 'Position': 'Pos', 'Opponent': 'Opp'}, inplace=True)
    df = df.reindex(columns=['Player', 'Pos', 'Team', 'Salary', 'Injury Indicator', 'Opp', 'Game'])
    return df


if __name__ == '__main__':
    x = fanduel_structure(qb)
    print(x)
