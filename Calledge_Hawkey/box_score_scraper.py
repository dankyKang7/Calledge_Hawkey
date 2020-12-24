#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:19:45 2019

@author: admin
"""

#This python query will take in the txt file of the urls and create a dataframe
#with all the meta data of the game this woudl include:

#  1. Score
#  2. Time 
#  3. Team reocrds
#  4. Hockey arenas https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_ice_hockey_arenas

import os 
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
from datetime import datetime as dt
from dateutil.parser import parse
#oepn the txt file and dump into list
#Change the workign directory
#dir1 = '/Users/admin/Blog_Data/Cawledge_Hawkey/Raw_Data/Calledge_Hawkey'
dir1 = 'D:\Blog\Data_Analysis\Calledge_Hawkey-master'
os.chdir(dir1)


with open ('d1m_1920_boxscoreurl.txt','r') as bs_urls_1920:
    url_list=bs_urls_1920.readlines()
   
url_list_2 = []
for url in url_list:
    url_list_2.append(url[:-1])
           
#Open the first line and test the code then automate

req_1 = requests.get('http://www.collegehockeystats.net/1920/boxes/mosuwmu1.o11')
print(req_1.raise_for_status()) # Check for any errors in the url


req1Bs = bs(req_1.text)

#Get the header information

target_data = req1Bs.div.p

date_vs = target_data.b.text.split(',')

day = date_vs[0]
dayOfyear= date_vs[1].lstrip()
year_type = date_vs[2].split('\n')
teamLocStr = year_type[1]
year = year_type[0].strip()

game_type = year_type[2].strip()
#Need function to determine if home/away or tournament
def team_location(teamLoc_str):
    #Find the target between first team abbreviation and capital letter
    teamLocation = []
    conf_tourney = []
    detStr = re.search('(?<=\)).*?(?=[A-Z])',teamLoc_str).group(0).strip()
    if detStr == 'at':
        away = re.search('^.*?(?=\()',teamLoc_str).group(0).strip()
        home = re.search('(?<=\sat\s).*?(?=\()',teamLoc_str).group(0).strip()
        teamLocation.append(away)
        teamLocation.append(home)
        gameType = 'home/away game'
    elif detStr == 'vs':
        tourneyTeam1 = re.search('^.*?(?=\()',teamLoc_str).group(0).strip()
        tourneyTeam2 = re.search('(?<=\svs\s).*?(?=\()',teamLoc_str).group(0).strip()
        teamLocation.append(tourneyTeam1)
        teamLocation.append(tourneyTeam2)
        gameType = 'Tournament Game'
    else:
        print('The string is not matched correctly!')
    return teamLocation, gameType
    

    
        


#Sweet now we need the time
final_score = target_data.p.b.text
finalScore_list = re.split(': |,',final_score)

#Now match the score with the home or away team
score_1 = finalScore_list[0].strip()
score_2 = finalScore_list[1].strip()

teamScore_pattern = '^.*?(?=\s\d)'
Score_pattern     = '(?<=\s\w)*\d'  

def score_assignment(scores):
    #This function takes in a list of scores
    #and outputs a dictionary with teamname:score
    teamScore_pattern = '^.*?(?=\s\d)'
    Score_pattern     = '(?<=\s\w)*\d'  
    values=[]
    score_keys=[]
    for score in scores:
        keys=len(scores)
        score_team = re.search(teamScore_pattern,score).group(0).strip()
        score_int  = int(re.search(Score_pattern,score).group(0).strip())
        values.append(score_int)
        score_keys.append(score_team)
    score_dict= {k:v for k,v in zip(score_keys,values)}
    return score_dict

def winner(scoringDict,home,away):
    if scoringDict[home] > scoringDict[away]:
        resultW = 'Home Team'
        resultL = 'Away Team'
    elif scoringDict[home] < scoringDict[away]:
        resultW = 'Away Team'
        resultL = 'Home Team'
    else:
        resultW = resultL = 'Tie'
    return resultW, resultL

game_1 = score_assignment(finalScore_list)
w_l = winner(game_1,home,away)
winningTeam = w_l[0]
losingTeam  = w_l[1]
homescore = game_1[home]
awayscore = game_1[away]
#Let's find out who won the game

#find the attendence and time data
attendance_gameTime = target_data.p.parent.next_sibling.text
attd_GT_list = re.split('\n|,',attendance_gameTime)[5:7]

attendance_str = attd_GT_list[0]
time_str       = attd_GT_list[1]
attendance     = int(re.search('(?<=:).*\d',attendance_str).group(0).strip())

#Pull the start time and end time and total time
b_targets = target_data.p.parent.next_sibling.find_all('b')
# 3, 4, 5 correspond to start time, end time, total time
start_time=b_targets[3].text 
startTime_dt = dt.strptime(start_time,'%I:%M %p')
end_time  =b_targets[4].text
endTime_dt = dt.strptime(end_time,'%I:%M %p')
total_time=b_targets[5].text
totalTime = dt.strptime(total_time,'%H:%M')
totalTime_minutes = totalTime.hour*60 +totalTime.minute
#Get the dt data
date_strp = date + ' '+ year
date = parse(date_strp)
timezone = 1

#Create the dataframe
column_names = ['Date','Day','startTime','endTime','totalTime','attendance',
                'homeTeam','awayTeam','gameType','homeScore','awayScore',
                'winner','loser']
values = [date,day,startTime_dt,endTime_dt,totalTime_minutes,
          attendance,home,away,game_type,homescore,awayscore,
          winningTeam,losingTeam]

#Create a dataframe
spreadsheet1 = pd.DataFrame(columns=column_names)

#We'll have to the columns into individual dataframes







