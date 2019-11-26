#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:38:13 2019

@author: admin
"""

import os 
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import urllib.request


#Go to directory
#Max OS Directory
#os.chdir('/Users/admin/Blog_Data/Cawledge_Hawkey')
#os.chdir('C:/Users/travm/Blog_Analysis/Calidge_Hawkey')


''' Potential Data Sources
    1. USCHO.com
    2. Hockeystats.net'''
    
#Beautiful soup to get the schedule and results data from collegestats.net
    
url = 'http://www.collegehockeystats.net/1920/schedules/d1m'

d1m_req = requests.get(url)
print(d1m_req.raise_for_status()) # Check for any errors in the url

#Get the url into a text format
d1m_soup = bs(d1m_req.text)
#create a txt file in python

with open('d1m_2020.txt','w') as d1m_2020:
    d1m_2020.write(str(d1m_soup))

#Get all the box scores for the current season

a_ref_box = d1m_soup.findAll('a')['href']