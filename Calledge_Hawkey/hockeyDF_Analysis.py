# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 22:36:51 2020

@author: travm
"""

import os 
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import requests as req
from datetime import datetime as dt
from dateutil.parser import parse
import matplotlib.pyplot as plt
from ggplot import *

with open('HockeyData.csv','r') as dataCsv:
    analysisDataframe = pd.read_csv(dataCsv)



#Data I'd like to inspect
    
#Total Shots on goals
#% share of shots on goal
# look at the subgroups
#Total Adjusted Goals
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
    

#Turn the date object into a datetime object
analysisDataframe['Date'] = analysisDataframe['Date'].apply(lambda x: pd.to_datetime(dt.strptime(x,'%m/%d/%Y')))
analysisDataframe['hockeySeason'] = analysisDataframe['Date'].apply(lambda x: seasonHockey(x))

#Total Adjusted Goals, adjusted goals
analysisDataframe['TotalAdjusted_Goals']  = analysisDataframe['homeadjustedgoalsallowed'] + analysisDataframe['awayadjustedgoalsallowed']
analysisDataframe['TotalShotson_Goal']    = analysisDataframe['homeshotsonGoal'] + analysisDataframe['awayshotsonGoal']
analysisDataframe['homeshareShotsonGoal'] = analysisDataframe['homeshotsonGoal']/analysisDataframe['TotalShotson_Goal']
analysisDataframe['awayshareShotsonGoal'] = analysisDataframe['awayshotsonGoal']/analysisDataframe['TotalShotson_Goal']
analysisDataframe['shotsonGoalDifference'] = analysisDataframe['homeshotsonGoal'] - analysisDataframe['awayshotsonGoal']



#Create running sum statistics
teamSelector = list(analysisDataframe.columns[[1,6,7,8,9,10,15,16,20,21,27,28]])
teamStats = analysisDataframe[teamSelector]

teamStats_TeamList = list(analysisDataframe['homeTeam'].drop_duplicates())
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
        teamPred = pd.concat([homeGame,awayGame])
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

#Create a large dataframe
hockeyPredictionData = pd.concat(list_1)

hockeyPredicitonSeasonData = hockeyPredictionData.set_index('hockeySeason')
hockeyPredictionData.plot(x='Expected Winning %',y='Winning %',kind='scatter',color='Team',colormap='viridis')
hockeyPredictionDataPrecise=hockeyPredictionData.loc[hockeyPredictionData['Season Game'] >= 10]
#Plots
fig, ax = plt.subplots()

ax.scatter(hockeyPredictionDataPrecise['Expected Winning %'],hockeyPredictionDataPrecise['Winning %'])

fig, ax = plt.subplots()

ax.hist(hockeyPredictionDataPrecise['Error'],bins=100)
#Winning %'s
und=hockeyPredictionData.loc[hockeyPredictionData['Team'] == 'NDK']
und = und.sort_values(by='Date')
fig, ax = plt.subplots()

ax.plot(und['Date'],und['Winning %'])
ax.plot(und['Date'],und['Expected Winning %'])
ax.plot(und['Date'],und['Expected Winning GF/GA'])

#Combine into 1 large dataframe
#Create team statistics?
#create a new dataframe
columnSelector = list(analysisDataframe.columns[[1,6,7,8,9,10,12,15,17,20,28]])
winPrediction = analysisDataframe[columnSelector].to_csv('C:/Users/travm/Dropbox/Personal/hockeyData.csv')
 

analysisDataframe.to_csv('C:/Users/travm/Desktop/Data_Analysis/hockeyData.csv')
#Distribution of ice hockey rinks/
#Seaons

fig, axs = plt.subplots(1, 2, sharey=True,tight_layout=True)

axs[0].hist(analysisDataframe['homeshotsonGoal'],bins=40)

axs[1].hist(analysisDataframe['awayshotsonGoal'],bins=40)
title = 'home vs. away shots on goal'
plt.show()

#Hockey Arena Widths
analysisRinkWidth = analysisDataframe[['Arena','Team','0']].drop_duplicates(subset='Arena')
#Have to create a summary table 
analysisRinkWidthSummary = pd.Index(analysisRinkWidth['0']).value_counts().sort_index()
analysisRinkWidthSummary = pd.DataFrame(analysisRinkWidthSummary).reset_index().rename(columns={'index':'RinkWidth (feet)','0':'Rink Count'})
analysisRinkWidthSummary['% of Rinks'] = analysisRinkWidthSummary['Rink Count'].apply(lambda x: x/analysisRinkWidthSummary.sum(axis=0)[1])

fig, ax1 = plt.subplots()
ax1.pie(analysisRinkWidthSummary['% of Rinks'],labels=analysisRinkWidthSummary['RinkWidth (feet)'],autopct='%1.1f%%',explode = (0.1,0,0,0,0,0))
plt.title('Ice Arena Width in D1 Men\'s College Hockey')
