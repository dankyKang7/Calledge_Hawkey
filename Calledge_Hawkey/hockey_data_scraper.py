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
    
yearList = ['1415','1516','1617','1718','1819','1920','2021']
urlList = []
for year in yearList:
    url1 = 'http://www.collegehockeystats.net/'
    url2 = '/schedules/d1m'
    urlList.append(url1+year+url2)


#Change the workign directory
#dir1 = '/Users/admin/Blog_Data/Cawledge_Hawkey/Raw_Data/Calledge_Hawkey'
dir1 = 'C:/Blog_Data/Calledge_Hawkey/'
os.chdir(dir1)

textlinks = []
for url in urlList:
    d1m_req = requests.get(url)
    print(d1m_req.raise_for_status()) # Check for any errors in the url
    print(d1m_req.status_code)
    #Get the url into a text format
    d1m_soup = bs(d1m_req.text)
    #create a txt file in python

    with open('d1m_2020.txt','w') as d1m_2020:
       d1m_2020.write(str(d1m_soup))
    
    #Get all the textbox scores for the current season
    for link in d1m_soup.find_all('a',href=re.compile('textbox')):
        textlinks.append(str(link))
    
    
#Add the links to main url
# Target Link
#url2='http://www.collegehockeystats.net''+ 'links'+"/1819/boxes/mniayrk1.o06'

baseurl = 'http://www.collegehockeystats.net'


textList = []

for link in textlinks:
    textList.append(re.findall(r'(?<=")(?:\\.|[^"\\])*(?=")',link))

scrapeTexturls = []

for url in textList:
    str_url =str(url) #now a string with brackets at the first adn last elemtn
    str_url_base = str_url[2:-2]
    
    finalurl = baseurl + str_url_base
    scrapeTexturls.append(finalurl)
    
#Now that we have the urls let's dump them into a txt file and open them with a
#script.

with open('d1m_textscoreurl20142021.txt','w') as d1m1920_bs:
    for url in scrapeTexturls:
        d1m1920_bs.write(url+'\n')


    