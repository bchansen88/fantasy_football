import pandas as pd
import os
from ffurl_db import *
from dfs_utility import *
from season_calc import season_calc
from fanduel_read import fanduel_structure
import numpy as np
import re

df = pd.read_html('https://www.rotowire.com/football/nfl-odds.php')
print(df)
