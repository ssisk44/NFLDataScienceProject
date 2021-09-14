import os
import sqlite3
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
import numpy as np
import time, os

#change to dictionary with team abbrevs
teams_list = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Football Team']

def main():
    # insertDBData()
    updateOddsDates()




##### WORKSHOPING #####
def getNFLPlayersScores():
    chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    soup_list = []
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    # for loop for each team and week
    driver.get('https://www.pro-football-reference.com/years/2020/week_1.htm')
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 500);")
    e1 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/span')
    e2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
    time.sleep(2)

    action = ActionChains(driver)
    action.move_to_element(e1).perform()
    action.move_to_element(e2).click().perform()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    crude = soup.find('pre', id='csv_games')
    soup_list.append(crude)
    df = pd.DataFrame(soup_list)
    df.to_csv(r'2020NFLWeek1Team1Team2PlayerResults.csv', index=False)
    driver.close()

    df = pd.read_csv('2020NFLScheduleAndResults.csv').to_numpy()
    arr = df[0][2].split('\n')
    arr.remove('')

    newarr = []
    for i in range(0, len(arr)):
        if arr[i][0] != '':
            newarr.append(arr[i].split(','))
    header = newarr[0]
    pd.DataFrame(newarr[1:]).to_csv('2020NFLScheduleAndResults.csv', index=False, header=header)

def calculateTeamRecordByWeekPerSeason():
    # team week record
    records_array = []
    for team in range(0, len(teams_list)):
        records_array.append([])

    for team in range(0, len(records_array)):
        for week in range(0, 18):  # +1 more than weeks for total
            records_array[team].append([])

    for team in range(0, len(records_array)):
        for week in range(0, 18):
            records_array[team][week].append(0)
            records_array[team][week].append(0)
            records_array[team][week].append(0)

    print(len(records_array))
    print(len(records_array[0]))
    print(len(records_array[0][0]))

    print(records_array)

    df = pd.read_csv('2020NFLScheduleAndResults.csv').to_numpy()
    for game in range(0, 256):
        home_team = ''
        away_team = ''
        index_winner = int(teams_list.index(df[game][4]))
        index_loser = int(teams_list.index(df[game][6]))

        if int(df[game][8]) == int(df[game][9]):  # tie
            records_array[index_winner][int(df[game][0]) - 1][2] = records_array[index_winner][int(df[game][0]) - 1][
                                                                       2] + 1
            records_array[index_loser][int(df[game][0]) - 1][2] = records_array[index_loser][int(df[game][0]) - 1][
                                                                      2] + 1

        else:
            records_array[index_winner][int(df[game][0]) - 1][0] = records_array[index_winner][int(df[game][0]) - 1][
                                                                       0] + 1
            records_array[index_loser][int(df[game][0]) - 1][1] = records_array[index_loser][int(df[game][0]) - 1][
                                                                      1] + 1

    print(records_array[0][0][0])


##### DATABASE #####
def createDBTable():
    try:
        sqliteConnection = sqlite3.connect('C:/Users/samue/OneDrive/Documents/sqlite/testdb.db')
        sqlite_create_table_query = '''CREATE TABLE PlayersData (
                                    date datetime,
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    team TEXT NOT NULL,
                                    salary REAL NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

def insertDBData():
    try:
        sqliteConnection = sqlite3.connect('C:/Users/samue/OneDrive/Documents/sqlite/testdb.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO SqliteDb_developers
                              (id, name, email, joining_date, salary) 
                               VALUES 
                              (1,'James','james@pynative.com','2019-03-17',8000)"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



##### ODDS AND SCHEDULE #####
def getNFLSeasonScoresByGameByWeek(season): ###need to delete string header and playoffs indicator when inserting new season data
    chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    soup_list = []
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.get('https://www.pro-football-reference.com/years/'+str(season)+'/games.htm')
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 500);")
    e1 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/span')
    e2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
    time.sleep(2)

    action = ActionChains(driver)
    action.move_to_element(e1).perform()
    action.move_to_element(e2).click().perform()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    crude = soup.find('pre', id='csv_games')
    soup_list.append(crude)
    df = pd.DataFrame(soup_list)
    df.to_csv(r'2020NFLScheduleAndResults.csv', index=False)
    driver.close()

def cleanNFLOdds(filename):
    df = pd.DataFrame(pd.read_excel("nfl2020odds.xlsx"))
    df.to_csv('nfl2020odds.csv', index=False)

def updateOddsDates():
    df = pd.read_csv('nfl2020odds.csv')
    col = df.columns
    df = df.to_numpy()
    for record in range(0,len(df)):
        if len(str(df[record][0])) == 3:
            date = '2021-0' + str(df[record][0])[0] + '-' + str(str(df[record][0])[1:])
            df[record][0] = date
        else:
            date = '2021-' + str(df[record][0])[:2] + '-' + str(str(df[record][0])[2:])
            df[record][0] = date
    pd.DataFrame(df).to_csv('nfl2020odds_correctdates.csv', index=False, header=col)

def createOddsToResultsDictionary():
    odds = pd.read_csv('nfl2020odds.csv').to_numpy()
    odds_teams_list = []
    for i in range(0,32):
        odds_teams_list.append(odds[i][3])
    odds_teams_list.sort()

    res = {} #Raiders says LAChargers, Chargers says LARams, Rams says LasVegas,         Patriots, Giants            Jets,Saints
    for key in teams_list:
        for value in odds_teams_list:
            res[key] = value
            odds_teams_list.remove(value)
            break
    x = res['New England Patriots']
    res['New England Patriots'] = res['New York Giants']
    res['New York Giants'] = x

    x = res['New York Jets']
    res['New York Jets'] = res['New Orleans Saints']
    res['New Orleans Saints'] = x

    x = res['Las Vegas Raiders']
    y = res['Los Angeles Chargers']
    z = res['Los Angeles Rams']
    res['Las Vegas Raiders'] = z
    res['Los Angeles Chargers'] = x
    res['Los Angeles Rams'] = y

    # for item in res.items():
    #     print(item)
    return res

def combineOddsANDSchedule():
    games = pd.read_csv('2020NFLScheduleAndResults.csv')
    odds = pd.read_csv('nfl2020odds_correctdates.csv')
    combined_arr = []
    for game in range(0, len(games)):
        arr = []
        V_odds_index = game * 2
        H_odds_index = game * 2 + 1
        W_odds_index = V_odds_index
        L_odds_index = H_odds_index
        if odds[V_odds_index][8] < odds[H_odds_index][8]:
            W_odds_index = H_odds_index
            L_odds_index = V_odds_index

        if game[0] <= 17: #only regular season
            arr.append(game[:4])
            arr.append(defineAwayTeam(game[4],game[6],game[5]))
            arr.append(defineHomeTeam(game[4], game[6], game[5]))
            arr.append(game[4])
            arr.append(game[6])

            arr.append((game[8]))
            arr.append((game[10]))
            arr.append((game[11]))
            arr.append((odds[W_odds_index][4]))
            arr.append((odds[W_odds_index][5]))
            arr.append((odds[W_odds_index][6]))
            arr.append((odds[W_odds_index][7]))
            arr.append((odds[W_odds_index][8]))

            arr.append((game[9]))
            arr.append((game[12]))
            arr.append((game[13]))
            arr.append((odds[L_odds_index][4]))
            arr.append((odds[L_odds_index][5]))
            arr.append((odds[L_odds_index][6]))
            arr.append((odds[L_odds_index][7]))
            arr.append((odds[L_odds_index][8]))




def defineHomeTeam(winner,loser,value): # value = @ of matchup, returns home team
    if str(value) == '@':
        return winner
    else:
        return loser

def defineAwayTeam(winner,loser,value): # value = @ of matchup, returns away team
    if str(value) == '@':
        return loser
    else:
        return winner




main()
