# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:10:55 2020

@author: travm
"""

#this script will the pull the rink size and get the year opened too 
#yay

import os 
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import urllib.request

arena_url = 'https://www.collegehockeynews.com/almanac/arenas.php'

arena_req = requests.get(arena_url)
arenaBS = bs(arena_req.text)

#Get the table data 
arena_DF = pd.read_html(arena_req.text)[0]

sheet_size = arena_DF['Sheet Size']
sheetLength_iter = []
sheetWidth_iter = []
for sheet in sheet_size:
    sheetLs = sheet.split('x')
    sheetLength_iter.append(sheetLs[0])
    sheetWidth_iter.append(sheetLs[1])
    
sheetLength = pd.Series(sheetLength_iter)
sheetWidthDF  = pd.DataFrame(pd.Series(sheetWidth_iter))

arenaDF = pd.merge(arena_DF,sheetWidthDF,left_index=True,right_index=True)
arenaDF.loc[arenaDF['Team']=='Mass.-Lowell','Team'] = 'UMass Lowell'
arenaDF.loc[arenaDF['Team']=='Lake Superior','Team'] = 'Lake Superior State'
arenaDF.loc[arenaDF['Team']=='Minnesota-Duluth','Team'] = 'Minnesota Duluth'
arenaDF.loc[arenaDF['Team']=='Army','Team'] = 'Army West Point'
arenaDF.loc[arenaDF['Team']=='Nebraska-Omaha','Team'] = 'Omaha'
arenaDF.loc[arenaDF['Team']=='Connecticut','Team'] = 'UConn'
arenaDF.loc[arenaDF['Team']=='American Int\'l','Team'] = 'American International'
arenaDF.loc[arenaDF['Team']=='Alabama-Huntsville','Team'] = 'Alabama Huntsville'
arenaDF.loc[arenaDF['Team']=='Alaska-Anchorage','Team'] = 'Alaska Anchorage'

arenaDF = arenaDF.rename(columns={0:'Rink Width'}).drop(columns='Unnamed: 4')