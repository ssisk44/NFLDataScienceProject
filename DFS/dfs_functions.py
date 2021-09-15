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

file = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/09132021BALLV_reduced_players.csv'

team_abbrev_list = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers',
                    'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
                    'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts',
                    'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers',
                    'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots',
                    'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles',
                    'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers',
                    'Tennessee Titans', 'Washington Football Team', 'Oakland Raiders', 'Washington Redskins']

team_abbrev_dict_2019 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
                    'Buffalo Bills': 'buf', 'Carolina Panthers': 'car',
                    'Chicago Bears': 'chi', 'Cincinnati Bengals': 'cin', 'Cleveland Browns': 'cle',
                    'Dallas Cowboys': 'dal', 'Denver Broncos': 'den',
                    'Detroit Lions': 'det', 'Green Bay Packers': 'gnb', 'Houston Texans': 'htx',
                    'Indianapolis Colts': 'clt',
                    'Jacksonville Jaguars': 'jax', 'Kansas City Chiefs': 'kan',
                    'Los Angeles Chargers': 'sdg',
                    'Los Angeles Rams': 'ram', 'Miami Dolphins': 'mia', 'Minnesota Vikings': 'min',
                    'New England Patriots': 'nwe',
                    'New Orleans Saints': 'nor', 'New York Giants': 'nyg', 'New York Jets': 'nyj',
                    'Philadelphia Eagles': 'phi',
                    'Pittsburgh Steelers': 'pit', 'San Francisco 49ers': 'sfo', 'Seattle Seahawks': 'sea',
                    'Tampa Bay Buccaneers': 'tam',
                    'Tennessee Titans': 'oti', 'Oakland Raiders': 'rai', 'Washington Redskins': 'was'}

team_abbrev_dict_2021 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
                    'Buffalo Bills': 'buf', 'Carolina Panthers': 'car',
                    'Chicago Bears': 'chi', 'Cincinnati Bengals': 'cin', 'Cleveland Browns': 'cle',
                    'Dallas Cowboys': 'dal', 'Denver Broncos': 'den',
                    'Detroit Lions': 'det', 'Green Bay Packers': 'gnb', 'Houston Texans': 'htx',
                    'Indianapolis Colts': 'clt',
                    'Jacksonville Jaguars': 'jax', 'Kansas City Chiefs': 'kan', 'Las Vegas Raiders': 'rai',
                    'Los Angeles Chargers': 'sdg',
                    'Los Angeles Rams': 'ram', 'Miami Dolphins': 'mia', 'Minnesota Vikings': 'min',
                    'New England Patriots': 'nwe',
                    'New Orleans Saints': 'nor', 'New York Giants': 'nyg', 'New York Jets': 'nyj',
                    'Philadelphia Eagles': 'phi',
                    'Pittsburgh Steelers': 'pit', 'San Francisco 49ers': 'sfo', 'Seattle Seahawks': 'sea',
                    'Tampa Bay Buccaneers': 'tam',
                    'Tennessee Titans': 'oti', 'Washington Football Team': 'was'}


def main(season):
    # createCombos(0, 2021, 1, '09132021BALLV')
    # box_score_retrieval(2021)
    # cleanAndSortSeasonPositions(2021)
    createAnalysisTables()
    countLineups()



##### CONTEST PERMUTATION CREATION #####
def createCombos(min_points_for_players_in_lineup, season, week, dateteams):
    array = pd.read_csv(file).to_numpy()

    # sorts by predicted FPPG
    sorted(array, key=lambda x: x[5], reverse=True)
    pd.DataFrame(array).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/Week' + str(
            week) + '/' + dateteams + '_BEFORE_GAME_reduced_players.csv', index=False)

    # creates all permutations of first player, with all combinations of the next four
    newcombos = []
    players = []
    for player in array:
        players.append(list(player))

    for player in range(0, len(players)):
        p1 = players[player]
        temp_players = players.copy()
        temp_players.pop(player)
        combos = list(combinations(temp_players, 4))

        for i in range(0, len(combos)):
            temp = []
            temp.append(p1[3])
            temp.append(combos[i][0][3])
            temp.append(combos[i][1][3])
            temp.append(combos[i][2][3])
            temp.append(combos[i][3][3])
            newcombos.append(temp)
    print(len(newcombos))
    def salaryLookup(name):
        for i in range(0, len(players)):
            if players[i][3] == name:
                return int(players[i][7])

    def fppg_lookup(name):
        for i in range(0, len(players)):
            if players[i][3] == name:
                return float(players[i][5])

    def team_lookup(name):
        for i in range(0, len(players)):
            if players[i][3] == name:
                return players[i][9]

    def all_player_team_check(p_teams):
        if len(p_teams) == p_teams.count(p_teams[0]):
            return False
        return True

    def position_lookup(name):
        for i in range(0, len(players)):
            if players[i][3] == name:
                return players[i][1]

    permutationsarr = []

    for combination in range(0, len(newcombos)):
        currentlineup = []
        lineupscore = 0
        salary = 0
        salaryMax = 60000
        p_teams = []
        p_positions = []
        for player in range(0, len(newcombos[combination])):
            p_salary = salaryLookup(newcombos[combination][player])
            p_fppg = fppg_lookup(newcombos[combination][player])
            p_name = newcombos[combination][player]
            p_positions.append(position_lookup(newcombos[combination][player]))
            if (salary + p_salary) <= salaryMax:
                currentlineup.append(p_name)  # add player to current
                salary += p_salary  # add salary
                p_teams.append(team_lookup(newcombos[combination][player]))
                if player == 0:
                    lineupscore += float(p_fppg) * 2  # MVP
                else:
                    lineupscore += float(p_fppg)  # NORMAL
            else:
                break

        if len(currentlineup) == 5 and all_player_team_check(p_teams) == True:
            currentlineup = currentlineup+p_teams+p_positions
            currentlineup.append(salary)
            currentlineup.append(lineupscore)
            permutationsarr.append(currentlineup)
    print(len(permutationsarr))
    permutationsarr.sort(key=lambda x: x[-1], reverse=True)
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5','Name1Team', 'Name2Team', 'Name3Team', 'Name4Team', 'Name5Team','Name1Position', 'Name2Position', 'Name3Position', 'Name4Position', 'Name5Position','Salary', 'FPPG']
    pd.DataFrame(permutationsarr).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/Week' + str(
            week) + '/' + dateteams + '_BEFORE_GAME_permutations.csv', index=False, header=headers)
########################################



##### DATA PIPELINE #####
def box_score_retrieval(season):
    get_Season_Schedule(season)
    schedule = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SCHEDULES/'+str(season)+'NFLScheduleAndResults.csv').to_numpy()
    game_count = 0
    for game in range(0, len(schedule)):
        if game_count <= 255 and 1 <= int(schedule[game][0]) <= 17: ############CHANGE BACK TO 17
            game_count += 1

            index = list(team_abbrev_dict_2021.keys()).index(defineHomeTeam(schedule[game][4],schedule[game][6],schedule[game][5]))
            teamcode = list(team_abbrev_dict_2021.values())[index]

            #make game links and get stats with them
            date = str(schedule[game][2])

            link = 'https://www.pro-football-reference.com/boxscores/'+date[0:4]+date[5:7]+date[8:]+'0'+str(teamcode)+'.htm'
            game = schedule[game]

            file_found = False
            for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/'):
                checkfile = (str(game[0])+str(defineAwayTeam(game[4], game[6], game[5]))[0:3]+str(defineHomeTeam(game[4], game[6], game[5]))[0:3]+'.csv')
                if file == checkfile:
                    file_found = True
                    break

            if file_found == False:
                try:
                    game_stats = get_Game_Stats(link)
                    #uses tables of one game to write all player stats, includes total fantasy points
                    get_Player_Stats(game_stats[0], game_stats[1], game_stats[2], game_stats[3], game, season)
                except:
                    game_stats = get_Game_Stats(link)
                    get_Player_Stats(game_stats[0], game_stats[1], game_stats[2], game_stats[3], game, season)

def get_Season_Schedule(season):
    try:
        # get season schedule
        chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver.maximize_window()
        driver.get('https://www.pro-football-reference.com/years/' + str(season) + '/games.htm')
        time.sleep(2)
        e1 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/span')
        e2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[2]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
        time.sleep(2)
        action = ActionChains(driver)
        action.move_to_element(e1).perform()
        action.move_to_element(e2).click().perform()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        crude = pd.DataFrame([soup.find('pre', id='csv_games')]).to_numpy()
        arr = crude[0][2].split('\n')
        arr.remove('')
        newarr = []
        for i in range(0, len(arr)):
            if arr[i][0] != '':
                newarr.append(arr[i].split(','))
        header = newarr[0]
        pd.DataFrame(newarr[1:]).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SCHEDULES/'+str(season)+'NFLScheduleAndResults.csv', index=False, header=header)
        return newarr[1:]
    except:
        get_Season_Schedule(season)

def get_Game_Stats(link):
    try:
        chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)

        def clean_Scrape(crude):
            arr = crude[0][2].split('\n')
            arr.remove('')
            newarr = []
            for i in range(0, len(arr)):
                if arr[i][0] != '':
                    newarr.append(arr[i].split(','))
            header = newarr[0]
            return newarr[1:]

        def getPRR():
            driver.maximize_window()
            driver.get(link)
            action = ActionChains(driver)
            # pass,rush,rec table
            prr_t_span = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[12]/div[1]/div/ul/li[1]/span')
            driver.execute_script("arguments[0].scrollIntoView();", prr_t_span)
            prr_t_button = driver.find_element_by_xpath(
                '/html/body/div[2]/div[4]/div[12]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
            time.sleep(2)
            action.move_to_element(prr_t_span).perform()
            action.move_to_element(prr_t_button).click().perform()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            Pass_Rush_Rec = clean_Scrape(pd.DataFrame([soup.find('pre', id='csv_player_offense')]).to_numpy())
            return Pass_Rush_Rec

        def getKRPR():
            driver.maximize_window()
            driver.get(link)
            action = ActionChains(driver)
            # KR/PR retrieval
            krpr_t_span = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[14]/div[1]/div/ul/li[1]/span')
            driver.execute_script("arguments[0].scrollIntoView();", krpr_t_span)
            krpr_t_button = driver.find_element_by_xpath(
                '/html/body/div[2]/div[4]/div[14]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
            time.sleep(2)
            action.move_to_element(krpr_t_span).perform()
            action.move_to_element(krpr_t_button).click().perform()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            KR_PR = clean_Scrape(pd.DataFrame([soup.find('pre', id='csv_returns')]).to_numpy())
            return KR_PR

        def getK():
            driver.maximize_window()
            driver.get(link)
            action = ActionChains(driver)
            # K retrieval
            k_t_span = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[16]/div[1]/div/ul/li[1]/span')
            driver.execute_script("arguments[0].scrollIntoView();", k_t_span)
            k_t_button = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[16]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
            time.sleep(2)
            action.move_to_element(k_t_span).perform()
            action.move_to_element(k_t_button).click().perform()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            K = clean_Scrape(pd.DataFrame([soup.find('pre', id='csv_kicking')]).to_numpy())
            return K

        def getTWOPC_FG():
            time.sleep(2)
            elements = driver.find_elements_by_xpath('//tr')
            begin, end = None, None
            TWOPC_FG = []
            for i in range(0, len(elements)):
                if end != None:
                    break
                t = elements[i].text
                if 'Quarter Time Tm Detail' in elements[i].text:
                    begin = i + 1
                elif 'Game Info' in elements[i].text:
                    end = i
                elif begin != None and end == None:
                    if elements[i].text[1]==' ':
                        TWOPC_FG.append((elements[i].text)[2:]) #split?
                    else:
                        TWOPC_FG.append(elements[i].text)
            driver.close()
            return TWOPC_FG

        return getPRR(),getKRPR(),getK(),getTWOPC_FG()

    except:
        get_Game_Stats(link)

def get_Player_Stats(PRR, PR_KR, K, TWOPC_FG, game, season):
    #calculate number of unqiue players for iteration
    names = []
    stats = []
    codes = []
    PRR_stats = []
    KR_PR_stats = []
    K_stats = []
    for player in range(1,len(PRR)):
        this_name = str(str(PRR[player][0]).split('\\')[0].replace('+', ''))
        this_name = str(this_name.replace('*', ''))
        code = str(str(PRR[player][0]).split('\\')[1])
        PRR_stats.append(PRR[player])
        if this_name not in names:
            names.append(this_name)
            stats.append(PRR[player])
            codes.append(code)

    for player in range(1, len(PR_KR)):
        name = PR_KR[player][0][:-9]
        KR_PR_stats.append(PR_KR[player])
        if name not in names:
            names.append(name)
            stats.append(PR_KR[player])
            code = str(str(PR_KR[player][0]).split('\\')[1])
            codes.append(code)

    for player in range(1, len(K)):
        name = K[player][0][:-9]
        stats.append(K[player])
        if name not in names and (K[player][6] == '0' or K[player][7] == '0'):
            names.append(name)
            stats.append(K[player])
            code = str(str(K[player][0]).split('\\')[1])
            codes.append(code)


    col = ['Season', 'Week', 'Game', 'Team', 'Name','Code', 'Position', 'PassTD', 'PassYD', 'RushTD', 'RushYD','Receptions', 'RecTD',
               'RecYD', 'INT', 'FUM/L', 'KRTD', 'PRTD', 'XP', 'FG0-19', 'FG20-29', 'FG30-39', 'FG40-49', 'FG50+', '2PC',
               'Fantasy Points']

    def get_team(stats,name):
        for i in range(0,len(stats)):
            this_name = str(str(stats[i][0]).split('\\')[0].replace('+', ''))
            this_name = str(this_name.replace('*', ''))
            if this_name == name:
                return stats[i][1]

    def getPRRStats(stats,name):
        arr = []
        for i in range(0,len(stats)):
            if stats[i][0][:-9] == name:

                arr.append(int(stats[i][5]))
                arr.append(int(stats[i][4]))
                arr.append(int(stats[i][13]))
                arr.append(int(stats[i][12]))
                arr.append(int(stats[i][16]))
                arr.append(int(stats[i][18]))
                arr.append(int(stats[i][17]))
                arr.append(int(stats[i][6]))
                arr.append(int(stats[i][21]))
        if arr == []:
            arr.append(0)
            arr.append(0)
            arr.append(0)
            arr.append(0)
            arr.append(0)
            arr.append(0)
            arr.append(0)
            arr.append(0)
            arr.append(0)
        return arr

    def getPRKRStats(stats,name):
        arr = [0,0]
        for i in range(0, len(stats)):
            if str(stats[i][0][:-9]) == str(name):
                arr[0] += int(stats[i][5])
                arr[1] += int(stats[i][10])
        return arr

    def getKStats(K,TWOPC_FG,name):
        #get kicker names
        arr = [0,0,0,0,0,0,0]

        #get kicker names
        kicker_names = []
        for player in range(1, len(K)):
            this_name = K[player][0][:-9]
            if this_name not in kicker_names and (K[player][6] == '0' or K[player][7] == '0'):
                kicker_names.append(this_name)

        #score field goals ONLY for kickers
        for scoring_play in range(0, len(TWOPC_FG)):
            if name not in kicker_names:
                break
            array = TWOPC_FG[scoring_play].split(' ')
            if 'field goal' in TWOPC_FG[scoring_play] and str(name) == str(str(array[2])+' '+ str(array[3])):
                i1 = array.index('yard')
                FG_Yards = int(array[i1-1])
                if FG_Yards <= 19:
                    arr[1] += 1
                elif 20<=FG_Yards<=29:
                    arr[2] += 1
                elif 30<=FG_Yards<=39:
                    arr[3] += 1
                elif 40<=FG_Yards<=49:
                    arr[4] += 1
                elif 50<=FG_Yards:
                    arr[5] += 1

        #record XP
        for kicker in range(1,len(K)):
            this_name = K[kicker][0][:-9]
            if this_name == str(name) and K[kicker][2]!='':
                arr[0] += int(K[kicker][2])

        #record 2PC
        for scoring_play in range(0, len(TWOPC_FG)):
            if '(' in TWOPC_FG[scoring_play]:
                i1 = TWOPC_FG[scoring_play].index('(')
                i2 = TWOPC_FG[scoring_play].index(')')
                after_TD = str(TWOPC_FG[scoring_play][i1 + 1:i2])
                if name in after_TD and 'pass from' in after_TD:
                    arr[6] += 1
                elif name in after_TD and 'run' in after_TD and 'run failed' not in after_TD:
                    arr[6] += 1
        return arr

    def lineup_scoring(entry):
        score = (entry[7] * 4) + (entry[8] * .04) + (entry[9] * 6) + (entry[10] * .1) + (entry[11] * .5)+ (entry[12] * 6) + (entry[13] * .1) + (entry[14] * -1) + (entry[15] * -2) + (entry[16] * 6) + (entry[17] * 6) + (entry[18] * 1) + (entry[19] * 3) + (entry[20] * 3) + (entry[21] * 3) + (entry[22] * 4) + (entry[23] * 5) + (entry[24] * 2)
        score = round(score, 2)
        return score

    player_data = pd.DataFrame(columns=col).to_numpy()
    for player in range(0,len(names)):

        def getPlayerCode(name):
            for record in range(0, len(stats)):
                this_name = str(str(stats[record][0]).split('\\')[0].replace('+',''))
                this_name = str(this_name.replace('*',''))
                code = str(str(stats[record][0]).split('\\')[1])
                if name == this_name:
                    return code
        entry = []
        entry.append(season)
        entry.append(game[0])
        entry.append(str(defineAwayTeam(game[4], game[6], game[5]))+'V'+str(defineHomeTeam(game[4], game[6], game[5])))
        entry.append(get_team(stats,names[player]))
        entry.append(names[player])
        entry.append(codes[player])
        entry.append(checkPlayerPosition(season,getPlayerCode(names[player])))

        P = getPRRStats(PRR_stats,names[player])
        entry.append(P[0])
        entry.append(P[1])
        entry.append(P[2])
        entry.append(P[3])
        entry.append(P[4])
        entry.append(P[5])
        entry.append(P[6])
        entry.append(P[7])
        entry.append(P[8])

        KR = getPRKRStats(KR_PR_stats,names[player])
        entry.append(KR[0])
        entry.append(KR[1])

        FG = getKStats(K,TWOPC_FG,names[player])
        entry.append(FG[0])
        entry.append(FG[1])
        entry.append(FG[2])
        entry.append(FG[3])
        entry.append(FG[4])
        entry.append(FG[5])
        entry.append(FG[6])

        points = lineup_scoring(entry)
        entry.append(points)
        player_data = np.vstack([player_data, entry])
    pd.DataFrame(player_data).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/'+str(game[0])+str(defineAwayTeam(game[4], game[6], game[5]))[0:3]+str(defineHomeTeam(game[4], game[6], game[5]))[0:3]+'.csv', index=False, header=col)

def defineHomeTeam(winner, loser, value):  # value = @ of matchup, returns home team
    if str(value) == '@':
        return loser
    else:
        return winner

def defineAwayTeam(winner, loser, value):  # value = @ of matchup, returns away team
    if str(value) == '@':
        return winner
    else:
        return loser

def createPlayerDatabase(season):
    player_db = []
    for team in team_abbrev_list:
        keys = list(team_abbrev_dict_2021.keys())
        values = list(team_abbrev_dict_2021.values())
        link = 'https://www.pro-football-reference.com/teams/'+values[keys.index(team)]+'/'+str(season)+'_roster.htm'
        chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        try:
            driver = webdriver.Chrome(chromedriver)
            driver.maximize_window()
            driver.get(link)
            time.sleep(2)
            e1 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[2]/span')
            driver.execute_script("arguments[0].scrollIntoView();", e1)
            e2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[2]/div/ul/li[4]/button')
            action = ActionChains(driver)
            time.sleep(2)
            action.move_to_element(e1).perform()
            action.move_to_element(e2).click().perform()
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            crude = pd.DataFrame([soup.find('pre', id='csv_games_played_team')]).to_numpy()
            arr = crude[0][2].split('\n')
            arr.remove('')
            newarr = []
            for i in range(0, len(arr)-1):
                if arr[i][0] != '':
                    newarr.append(arr[i].split(','))
            newarr = newarr[1:]
            driver.close()


            for entry in range(0,len(newarr)):
                newestarr_entry = []
                this_name = str(str(newarr[entry][1]).split('\\')[0].replace('+', ''))
                this_name = str(this_name.replace('*', ''))
                code = str(str(newarr[entry][1]).split('\\')[1])
                newestarr_entry.append(this_name)
                newestarr_entry.append(code)
                newestarr_entry.append(newarr[entry][3])
                player_db.append(newestarr_entry)

            pd.DataFrame(player_db).to_csv(
                '/DFS/DFS_DATA/DFS_FILES/0_players_db.csv',
                index=False, header=['Name', 'Football-Ref-Code', 'Position'])

        except:
            driver = webdriver.Chrome(chromedriver)
            driver.maximize_window()
            driver.get(link)
            time.sleep(2)
            e1 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[2]/span')
            driver.execute_script("arguments[0].scrollIntoView();", e1)
            e2 = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[2]/div/ul/li[4]/button')
            action = ActionChains(driver)
            time.sleep(2)
            action.move_to_element(e1).perform()
            action.move_to_element(e2).click().perform()
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            crude = pd.DataFrame([soup.find('pre', id='csv_games_played_team')]).to_numpy()
            arr = crude[0][2].split('\n')
            arr.remove('')
            newarr = []
            for i in range(0, len(arr) - 1):
                if arr[i][0] != '':
                    newarr.append(arr[i].split(','))
            newarr = newarr[1:]
            driver.close()

            for entry in range(0, len(newarr)):
                newestarr_entry = []
                this_name = str(str(newarr[entry][1]).split('\\')[0].replace('+', ''))
                this_name = str(this_name.replace('*', ''))
                code = str(str(newarr[entry][1]).split('\\')[1])
                newestarr_entry.append(this_name)
                newestarr_entry.append(code)
                newestarr_entry.append(newarr[entry][3])
                player_db.append(newestarr_entry)

            pd.DataFrame(player_db).to_csv(
                'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/0_players_db.csv',
                index=False, header=['Name', 'Football-Ref-Code', 'Position'])

def checkPlayerPosition(season,name_code):
    exists = False
    for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/'):
        checkfile = '0_players_db.csv'
        if file == checkfile:
            exists = True

    if exists == False:
        createPlayerDatabase(season) #just one overall no season so this check doesnt work

    file = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/0_players_db.csv'
    df = pd.read_csv(file)
    arr = df.to_numpy()
    for entry in range(0, len(arr)):
        if str(arr[entry][2]) == 'nan' and str(name_code) == str(arr[entry][1]):
            link = 'https://www.pro-football-reference.com/players/' + str(arr[entry][1])[0] + '/' + str(arr[entry][1]) + '.htm'
            chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            driver.get(link)
            not_found = False
            e = None
            try:
                e = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/p[2]')
            except:
                not_found=True
            if not_found == True:
                 e = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/p[2]')

            error = False
            index = ''
            position = 'error'
            try:
                index = (e.text).index(':')
                position = (e.text[index + 1:]).replace(' ', '')
            except:
                pass
            arr[entry][2] = position
            driver.close()
            pd.DataFrame(arr).to_csv(file, index=False, header=['Name', 'Football-Ref-Code', 'Position'])
            return str(position)

        elif str(arr[entry][2]) != 'nan' and str(name_code) == str(arr[entry][1]):
            return str(arr[entry][2])
##############################


##### DATA ANALYSIS #####
def cleanAndSortSeasonPositions(season):
    counter = 0
    for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/'):
        counter += 1
        df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/' + file)
        col = df.columns
        df.sort_values(by=['Fantasy Points'], inplace=True, ascending=False)
        arr = df.to_numpy()
        for entry in range(0, len(arr)):
            if 'QB' in str(arr[entry][5]) or 'RB' in str(arr[entry][5]) or 'TE' in str(arr[entry][5]) or 'WR' in str(
                    arr[entry][5]):
                arr[entry][5] = str(arr[entry][5])[0:2]
            elif 'K' in str(arr[entry][5]):
                pass
            else:
                arr[entry][5] = 'error'
        pd.DataFrame(arr).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/' + file, index=False, header=col)

    print("Total files:" + str(counter))

def updatePlayerPositionFromDB(season):
    def getPlayerfromDB(code):
        None

    counter = 0
    for directory in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'):
        for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + directory + '/'):
            counter += 1
            df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/' + file)
            col = df.columns
            arr = df.to_numpy()
            for entry in range(0, len(arr)):
                if 'QB' in str(arr[entry][5]) or 'RB' in str(arr[entry][5]) or 'TE' in str(arr[entry][5]) or 'WR' in str(
                        arr[entry][5]):
                    arr[entry][5] = str(arr[entry][5])[0:2]
                elif 'K' in str(arr[entry][5]):
                    pass
                else:
                    arr[entry][5] = 'error'
            pd.DataFrame(arr).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+str(season)+'/' + file, index=False, header=col)

    print("Total files:" + str(counter))

def createAnalysisTables():
    # Season Totals for Top 5 Contest Outcomes
    distinct_positional_combinations = []
    qb_position_counter = [0, 0, 0, 0, 0]
    rb_position_counter = [0, 0, 0, 0, 0]
    wr_position_counter = [0, 0, 0, 0, 0]
    te_position_counter = [0, 0, 0, 0, 0]
    k_position_counter = [0, 0, 0, 0, 0]
    other_position_counter = [0, 0, 0, 0, 0]

    for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/2020/'):
        lineup = ['','','','','']
        df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/2020/' + file)
        col = df.columns
        arr = df.to_numpy()
        for entry in range(0, 5):
            lineup[entry] = arr[entry][5].upper()
            # distinct_lineup[entry] = arr[entry][5].upper()
            if str(arr[entry][5]).upper() == 'QB':
                qb_position_counter[entry] += 1
            elif str(arr[entry][5]).upper() == 'RB':
                rb_position_counter[entry] += 1
            elif str(arr[entry][5]).upper() == 'WR':
                wr_position_counter[entry] += 1
            elif str(arr[entry][5]).upper() == 'TE':
                te_position_counter[entry] += 1
            elif str(arr[entry][5]).upper() == 'K':
                k_position_counter[entry] += 1
            else:
                other_position_counter[entry] += 1
        distinct_positional_combinations.append(lineup)

    # ###directory in Season
    # for directory in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'):
    #     for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+directory+'/'):
    #         lineup = ['','','','','']
    #         df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'+directory+'/' + file)
    #         col = df.columns
    #         arr = df.to_numpy()
    #
    #         for entry in range(0, 5):
    #             lineup[entry] = arr[entry][5].upper()
    #             # distinct_lineup[entry] = arr[entry][5].upper()
    #             if str(arr[entry][5]).upper() == 'QB':
    #                 qb_position_counter[entry] += 1
    #             elif str(arr[entry][5]).upper() == 'RB':
    #                 rb_position_counter[entry] += 1
    #             elif str(arr[entry][5]).upper() == 'WR':
    #                 wr_position_counter[entry] += 1
    #             elif str(arr[entry][5]).upper() == 'TE':
    #                 te_position_counter[entry] += 1
    #             elif str(arr[entry][5]).upper() == 'K':
    #                 k_position_counter[entry] += 1
    #             else:
    #                 other_position_counter[entry] += 1
    #         distinct_positional_combinations.append(lineup)
    #
    print("QBs: " + str(qb_position_counter), str(sum(qb_position_counter)/256))
    print("RBs: " + str(rb_position_counter), str(sum(rb_position_counter)/256))
    print("WRs: " + str(wr_position_counter), str(sum(wr_position_counter)/256))
    print("TEs: " + str(te_position_counter), str(sum(te_position_counter)/256))
    print("Ks: " + str(k_position_counter), str(sum(k_position_counter)/256))
    print("Other: " + str(other_position_counter), str(sum(other_position_counter)/256))
    sorted(distinct_positional_combinations, key=lambda x: x[-1])
    pd.DataFrame(distinct_positional_combinations).to_csv('top_5_positions_per_contest.csv',index=False,header=['1st','2nd','3rd','4th','5th']) #,'Count])







        #Contest Position Outcome vs. Player Position Array
        # for entry in range(0, 1):
        #     print(arr[entry][1],arr[entry][2],arr[entry][5])

def countLineups():
    df = pd.read_csv('file.csv')
    table = df.to_numpy()
    lineups = []
    for entry in range(0,len(table)): #
        this = []
        q = np.count_nonzero(table[entry] == 'QB')
        r = np.count_nonzero(table[entry] == 'RB')
        w = np.count_nonzero(table[entry] == 'WR')
        t = np.count_nonzero(table[entry] == 'TE')
        k = np.count_nonzero(table[entry] == 'K')
        o = 0
        if q+r+w+t+k != 5:
            o = 5 - (q+r+w+t+k)

        this.append(q)
        this.append(r)
        this.append(w)
        this.append(t)
        this.append(k)
        this.append(o)
        this.append(0)
        lineups.append(this)

    new_lineups = []
    logs = []
    for entry in range(0,len(lineups)):
        if lineups[entry][0:-1] in logs:
            pass
        else:
            logs.append(lineups[entry][0:-1])
            c = lineups.count(lineups[entry])
            lineups[entry][-1] = c
            new_lineups.append(lineups[entry])

    new_lineups = sorted(new_lineups, key=lambda x: x[-1])[::-1]

    # #total games check
    # count = 0
    # for i in range(0,len(new_lineups)):
    #     count += new_lineups[i][-1]
    # print(count)

    pd.DataFrame(new_lineups).to_csv('all_lineups_position_count.csv',index=False,header=['QB_count','RB_count','WR_count','TE_count','K_count','OTHER_count','count'])

def bigCountTable():
    table = pd.DataFrame(columns=['Position','0','1','2B','2S','3B','3S','4B','4S','5B','5S'])
    col = table.columns
    table.loc[len(table.index)] = ['QB', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    table.loc[len(table.index)] = ['RB', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    table.loc[len(table.index)] = ['WR', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    table.loc[len(table.index)] = ['TE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    table.loc[len(table.index)] = ['K', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    table.loc[len(table.index)] = ['Other', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    table = table.to_numpy()
    print(table)



    for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/2020'):
        lineup = []
        df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/2020/' + file)
        arr = df.to_numpy()
        for entry in range(0, 5):
            lineup.append(arr[entry][5]) #position
            lineup.append(arr[entry][3]) #team

        #team 1
        t1 = ''
        t1_qb_position_counter = 0
        t1_rb_position_counter = 0
        t1_wr_position_counter = 0
        t1_te_position_counter = 0
        t1_k_position_counter = 0
        t1_other_position_counter = 0

        # team 2
        t2 = ''
        t2_qb_position_counter = 0
        t2_rb_position_counter = 0
        t2_wr_position_counter = 0
        t2_te_position_counter = 0
        t2_k_position_counter = 0
        t2_other_position_counter = 0

        for entry in range(0,10,2):
            if entry == 0:
                t1 = str(lineup[entry][1])


            if str(arr[entry][5]).upper() == 'QB':
                t1_qb_position_counter += 1
            elif str(arr[entry][5]).upper() == 'RB':
                t1_rb_position_counter += 1
            elif str(arr[entry][5]).upper() == 'WR':
                t1_wr_position_counter += 1
            elif str(arr[entry][5]).upper() == 'TE':
                t1_te_position_counter += 1
            elif str(arr[entry][5]).upper() == 'K':
                t1_k_position_counter += 1
            else:
                t1_other_position_counter += 1





main(2020)