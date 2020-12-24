# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 20:47:01 2020

@author: travm
"""

import os
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req  
from datetime import datetime as dt

'''This python script will call on multiple functions and build in the 
hockey data for further analysis'''

#Step 1. Get all the txt file links
os.chdir('C:/Blog_Data/Calledge_Hawkey')

from TextData_Generator import winner_loser, home_away, mergeDict, dictkvswap,\
ScoringShotsGoalTending, hockeyStatsDF

#Step run hockey data scraper to get updated list of stats
d1mLinkList = []
with open('d1m_textscoreurl20142021.txt','r') as d1mData:
    line = d1mData.readlines()
    for link in line:
        d1mLinkList.append(link.replace('\n',''))

#Read the data and create a really long list with list compression
def linkListReader(linkList):
    '''
    

    Parameters
    ----------
    linkList : list
         a list of list str that will be opened and stored in a list as html
         text.

    Returns
    -------
    list of links and their associated html text

    '''
    '''Iniatiate an empty list'''
    linkHTML = []
    
    '''read teh links and get the data'''
    for link in linkList:
        linkGet = req.get(link)
        print(linkGet.status_code)
        if linkGet.status_code == 200:
            linkHTML.append(bs(linkGet.text))
        else:
            print(link)
            
    return linkHTML

d1mLinkHTML = linkListReader(d1mLinkList)

d1mDatahtml = hockeyStatsDF(d1mLinkHTML)

#Create into a dataframe
d1mHockeyDataDF = pd.DataFrame({
    'Date'                     : d1mDatahtml[0],
    'startTime'            : d1mDatahtml[1],
    'endTime'              : d1mDatahtml[2],
    'totalTime'            : d1mDatahtml[3],
    'attendance'           : d1mDatahtml[4],
    'homeTeam'             : d1mDatahtml[5],
    'awayTeam'             : d1mDatahtml[6],
    'game_type'            : d1mDatahtml[7],
    'winner'          : d1mDatahtml[8],
    'loser'           : d1mDatahtml[9],
    'venueLoc'             : d1mDatahtml[10],
    'homescore'            : d1mDatahtml[11],
    'homegoalsallowed'         : d1mDatahtml[12],
    'homeemptynetgoalsallowed' : d1mDatahtml[13],
    'homeadjustedgoalsallowed' : d1mDatahtml[14],
    'homeshotsonGoal'          : d1mDatahtml[15],
    'awayscorelist'            : d1mDatahtml[16],
    'awaygoalsallowed'         : d1mDatahtml[17],
    'awayemptynetgoalsallowed' : d1mDatahtml[18],
    'awayadjustedgoalsallowed' : d1mDatahtml[19],
    'awayshotsonGoal'          : d1mDatahtml[20],
    })

#Run the arenaData python file
#os.system('Arena_Data.py')
    
#Join the 2 DataFrames
d1mHockeyDataDF_Arena = d1mHockeyDataDF.copy()
# pd.merge(d1mHockeyDataDF,arenaDF,left_on='venueLoc',right_on='Team')

#Season Data
#hockeySeason
def seasonHockey(dateobject):
    if (dateobject > pd.Timestamp(2014,9,1)) & (dateobject < pd.Timestamp(2015,5,1)):
        return '2014-2015 Season'
    elif (dateobject > pd.Timestamp(2015,9,1)) & (dateobject < pd.Timestamp(2016,5,1)):
        return '2015-2016 Season'
    elif (dateobject > pd.Timestamp(2016,9,1)) & (dateobject < pd.Timestamp(2017,5,1)):
        return '2016-2017 Season'
    elif (dateobject > pd.Timestamp(2017,9,1)) & (dateobject < pd.Timestamp(2018,5,1)):
        return '2017-2018 Season'
    elif (dateobject > pd.Timestamp(2018,9,1)) & (dateobject < pd.Timestamp(2019,5,1)):
        return '2018-2019 Season'
    elif (dateobject > pd.Timestamp(2019,9,1)) & (dateobject < pd.Timestamp(2020,5,1)):
        return '2019-2020 Season'
    elif (dateobject > pd.Timestamp(2020,9,1)) & (dateobject < pd.Timestamp(2021,5,1)):
        return '2020-2021 Season'

#Turn the date object into a datetime object
d1mHockeyDataDF_Arena['Date'] = d1mHockeyDataDF_Arena['Date'].apply(lambda x: pd.to_datetime(dt.strptime(x,'%m/%d/%Y')))
d1mHockeyDataDF_Arena['hockeySeason'] = d1mHockeyDataDF_Arena['Date'].apply(lambda x: seasonHockey(x))

#Total Adjusted Goals, adjusted goals
d1mHockeyDataDF_Arena['TotalAdjusted_Goals']  = d1mHockeyDataDF_Arena['homeadjustedgoalsallowed'] + d1mHockeyDataDF_Arena['awayadjustedgoalsallowed']
d1mHockeyDataDF_Arena['TotalShotson_Goal']    = d1mHockeyDataDF_Arena['homeshotsonGoal'].astype(int) + d1mHockeyDataDF_Arena['awayshotsonGoal'].astype(int)
d1mHockeyDataDF_Arena['homeshareShotsonGoal'] = d1mHockeyDataDF_Arena['homeshotsonGoal'].astype(int)/d1mHockeyDataDF_Arena['TotalShotson_Goal'].astype(int)
d1mHockeyDataDF_Arena['awayshareShotsonGoal'] = d1mHockeyDataDF_Arena['awayshotsonGoal'].astype(int)/d1mHockeyDataDF_Arena['TotalShotson_Goal'].astype(int)
d1mHockeyDataDF_Arena['shotsonGoalDifference'] = d1mHockeyDataDF_Arena['homeshotsonGoal'].astype(int) - d1mHockeyDataDF_Arena['awayshotsonGoal'].astype(int)



#Create running sum statistics
# teamSelector = list(d1mHockeyDataDF_Arena.columns[[1,6,7,8,9,10,15,16,20,21,27,28]])
# teamStats = d1mHockeyDataDF_Arena[teamSelector]

teamStats_TeamList = list(d1mHockeyDataDF_Arena['homeTeam'].drop_duplicates())
def winlosstie(value,team):
    #the value if the dataframe value whether it be win loss or tie
    if value == team:
        return 1
    elif value =='Tie':
        return 2    
    else:
        return 0

def winPredict(teamList,dataframe):
    TeamsDataFrameList = []
    for team in teamList:
        print(team)
        teamPerfyear = dataframe.loc[(dataframe['homeTeam'] ==team) | (dataframe['awayTeam'] == team)]
        #Create the goals for series
        homeGame = teamPerfyear.loc[teamPerfyear['homeTeam'] == team]
        homeGame['GF'] = teamPerfyear.loc[teamPerfyear['homeTeam'] == team]['awayadjustedgoalsallowed']
        homeGame['GA'] = teamPerfyear.loc[teamPerfyear['homeTeam'] == team]['homeadjustedgoalsallowed']
        homeGame['SOG'] = teamPerfyear.loc[teamPerfyear['homeTeam'] ==team]['homeshotsonGoal']
        homeGame['SOGA'] = teamPerfyear.loc[teamPerfyear['homeTeam']==team]['awayshotsonGoal']
        awayGame = teamPerfyear.loc[teamPerfyear['awayTeam'] == team]
        awayGame['GF'] = teamPerfyear.loc[teamPerfyear['awayTeam'] == team]['homeadjustedgoalsallowed']
        awayGame['GA'] = teamPerfyear.loc[teamPerfyear['awayTeam'] == team]['awayadjustedgoalsallowed']
        awayGame['SOG'] = teamPerfyear.loc[teamPerfyear['awayTeam'] ==team]['awayshotsonGoal']
        awayGame['SOGA'] = teamPerfyear.loc[teamPerfyear['awayTeam']==team]['homeshotsonGoal']
        #Concatenate the 2 dataframe
        teamPred = pd.concat([homeGame,awayGame]).sort_values('Date')
        teamPred['Team'] = team
        teamPred['Wins'] = teamPred['winner'].apply(lambda x: winlosstie(x,team)).replace(2,0)
        teamPred['Losses'] = teamPred['loser'].apply(lambda x: winlosstie(x,team)).replace(2,0)
        teamPred['Ties']   = teamPred['winner'].apply(lambda x: winlosstie(x,team)-1).replace(-1,0)
        teamPred['Total']  = teamPred['Wins'] + teamPred['Losses'] + teamPred['Ties']
        #Let's get the winning percentage by season
        teamPred['Season Game'] = teamPred.groupby(by='hockeySeason')['Total'].cumsum()
        teamPred['Season Wins'] = teamPred.groupby(by='hockeySeason')['Wins'].cumsum()
        teamPred['Winning %'] = teamPred['Season Wins']/teamPred['Season Game']
        teamPred['Season GF']= teamPred.groupby(by='hockeySeason')['GF'].cumsum()
        teamPred['Season SOG'] = teamPred.groupby(by='hockeySeason')['SOG'].cumsum()
        teamPred['Season GA'] = teamPred.groupby(by='hockeySeason')['GA'].cumsum()
        teamPred['Season SOGA'] =teamPred.groupby(by='hockeySeason')['SOGA'].cumsum()
        teamPred['Season GD'] = teamPred['Season GF'] - teamPred['Season GA']
        teamPred['Season SOGD'] = teamPred['Season SOG'] - teamPred['Season SOGA']
        teamPred['Goals Per Game (mean)'] = teamPred['Season GF']/teamPred['Season Game']
        teamPred['SOG per Game (mean)'] = teamPred['Season SOG']/teamPred['Season Game']
        teamPred['SOGA per Game (mean)'] = teamPred['Season SOGA']/teamPred['Season Game']
        teamPred['Total Goals Per Game (mean)'] = (teamPred['Season GF']+teamPred['Season GA'])/teamPred['Season Game']
        teamPred['Expected Winning %'] = 0.5 + teamPred['Season GD']/(teamPred['Total Goals Per Game (mean)']*teamPred['Season Game'])
        teamPred['Error'] = teamPred['Winning %'] - teamPred['Expected Winning %']
        teamPred['Expected Winning GF/GA'] = teamPred['Season GF']**2/(teamPred['Season GF']**2 + teamPred['Season GA']**2)
        TeamsDataFrameList.append(teamPred)
    return TeamsDataFrameList

d1mHockeyDataDF_Arena['homeshotsonGoal']=d1mHockeyDataDF_Arena['homeshotsonGoal'].astype(int)

d1mHockeyDataDF_Arena['awayshotsonGoal']=d1mHockeyDataDF_Arena['awayshotsonGoal'].astype(int)
#Create a large dataframe
hockeyPredictionData = pd.concat(winPredict(teamStats_TeamList,d1mHockeyDataDF_Arena))

#College Hockey Data
hockeyPredictionData.to_csv('hockeyData14_21.csv')

hockeyPredicitonSeasonData = hockeyPredictionData.set_index('hockeySeason')
hockeyPredictionData.plot(x='Expected Winning %',y='Winning %',kind='scatter',color='Team',colormap='viridis')
hockeyPredictionDataPrecise=hockeyPredictionData.loc[hockeyPredictionData['Season Game'] >= 10]


    
