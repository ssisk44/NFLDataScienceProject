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

    for file in os.listdir(directory):
        game = pd.read_csv(directory + file)
        col = game.columns
        game_arr = game.to_numpy()
        week = re.sub(r"[A-Z]|[a-z]|[.]", '', file)

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
                if str(game_arr[player][4]) == str(weekly_depth_chart_arr[entry][0]):
                    game_arr[player][5] = weekly_depth_chart_arr[entry][1]
                    break
        pd.DataFrame(game_arr).to_csv(directory+file,header=col,index=False)
        exit()

updateGameHistoryWithDepthChartPositions(2020)