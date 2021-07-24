import pandas as pd


#urls for defensive analytics
pfr_rb = 'https://www.pro-football-reference.com/years/{}/fantasy-points-against-RB.htm'
pfr_te = 'https://www.pro-football-reference.com/years/{}/fantasy-points-against-TE.htm'
pfr_qb = 'https://www.pro-football-reference.com/years/{}/fantasy-points-against-QB.htm'
pfr_wr = 'https://www.pro-football-reference.com/years/{}/fantasy-points-against-WR.htm'
def_advanced = 'https://www.pro-football-reference.com/years/{}/opp.htm#all_advanced_defense'
#def_pass = 'https://www.pro-football-reference.com/years/{}/opp.htm#all_rushing'
fo_def = 'https://www.footballoutsiders.com/stats/teamdef/{}'
fo_dl = 'https://www.footballoutsiders.com/stats/dl/{}'

#urls for offensive analytics
fantasy = 'https://www.pro-football-reference.com/years/{}/fantasy.htm'

def stats_req(url, year):

    url = url.format(year)

    df = pd.read_html(url)
    return df
