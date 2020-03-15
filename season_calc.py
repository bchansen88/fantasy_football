from datetime import datetime

now = datetime

d = datetime.today()

def season_calc():

    now = datetime.today()
    m = now.month
    y = now.year

    if m == 1:

        y = y - 1

    return y

