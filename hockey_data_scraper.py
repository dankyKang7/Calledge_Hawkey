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
url2='http://www.collegehockeystats.net/1819/boxes/mniayrk1.o06'
url_1819 = 'http://www.collegehockeystats.net/1819/schedules/d1m'
#Change the workign directory
dir1 = '/Users/admin/Blog_Data/Cawledge_Hawkey/Raw_Data/Calledge_Hawkey'
os.chdir(dir1)

d1m_req = requests.get(url)
print(d1m_req.raise_for_status()) # Check for any errors in the url

#Get the url into a text format
d1m_soup = bs(d1m_req.text)
#create a txt file in python

with open('d1m_2020.txt','w') as d1m_2020:
    d1m_2020.write(str(d1m_soup))

#Get all the box scores for the current season
links =[]
for link in d1m_soup.find_all('a',href=re.compile('^/1920/boxes')):
    links.append(str(link))
    
    
#Add the links to main url
# Target Link
#url2='http://www.collegehockeystats.net''+ 'links'+"/1819/boxes/mniayrk1.o06'

baseurl = 'http://www.collegehockeystats.net'

#get only the text href of the string links
boxscore_list = []
for link in links:
    boxscore_list.append(re.findall(r'(?<=")(?:\\.|[^"\\])*(?=")',link))

scrape_urls = []
for url in boxscore_list:
    str_url =str(url) #now a string with brackets at the first adn last elemtn
    str_url_base = str_url[2:-2]
    
    finalurl = baseurl + str_url_base
    scrape_urls.append(finalurl)
    
    
#Now that we have the urls let's dump them into a txt file and open them with a
#script.

with open('d1m_1920_boxscoreurl.txt','w') as d1m1920_bs:
    for url in scrape_urls:
        d1m1920_bs.write(url+'\n')
\
#Now we can scrape the urlboxscore data into a table that compiles this.
#Might use a dataframe stack/concatentate
    
#Target Data
#Open the url of the first point int eh list
box1 = requests.get(scrape_urls[79])
print(box1.raise_for_status())
box1_soup = bs(box1.text)

with open('box_score_1.txt','w') as box_79:
    box_79.write(str(box1_soup))
    
    