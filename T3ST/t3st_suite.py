import re
from itertools import permutations, combinations
import os
import sqlite3
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
import pandas as pd
import numpy as np
import time, os


#updates game history with depth chart positions
def updateGameHistoryWithDepthChartPositions(season):
    directory = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/'
    week_counter = 0
    game = 0
    col = 0
    game_arr = []
    weekly_depth_chart_arr = []
    for file in os.listdir(directory):
        week = re.sub(r"[A-Z]|[a-z]|[.]", '', file)

        #prevent reacquiring weekly depth chart for each game
        if week != week_counter:
            week_counter = week
            game = pd.read_csv(directory + file)
            col = game.columns
            game_arr = game.to_numpy()

            df_list = []
            df = pd.read_html('https://www.spotrac.com/nfl/depth-charts/'+str(season)+'/week-'+week+'/')
            for i in range(0, len(df)):
                if df[i].columns[1] == 'Pos.':
                    df_list.append(df[i][:-1])
            weekly_depth_chart = pd.concat(df_list)
            weekly_depth_chart_arr = weekly_depth_chart.to_numpy()

        print(file)
        for player in range(0,len(game_arr)):
            for entry in range(0,len(weekly_depth_chart_arr)):
                name = str(weekly_depth_chart_arr[entry][0])
                if name[-2:] == 'IR':
                    name = name[:-3]
                if name.split(" ")[0] in str(game_arr[player][4]) and name.split(" ")[1] in str(game_arr[player][4]):
                    game_arr[player][5] = weekly_depth_chart_arr[entry][1]
                    break
                else:
                    game_arr[player][5] = ''
        pd.DataFrame(game_arr).to_csv(directory+file,header=col,index=False)


updateGameHistoryWithDepthChartPositions(2020)