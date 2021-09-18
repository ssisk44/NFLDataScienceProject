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

file = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/09192021KCBAL_reduced_players.csv'

team_abbrev_list = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers',
                    'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
                    'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts',
                    'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers',
                    'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots',
                    'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles',
                    'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers',
                    'Tennessee Titans', 'Washington Football Team', 'Oakland Raiders', 'Washington Redskins']

bbref_team_abbrev_dict_2019 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
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

bbref_team_abbrev_dict_2021 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
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
    createCombos(0, 2021, 2, '09192021KCBAL')
    filterCombosContests()
    countCSVPermutations(filterCombosCombos(2021, 2, '09192021KCBAL'))
    returnCSVEntries()
    createAnalysisTables()




##### CONTEST PERMUTATION CREATION #####
def createCombos(min_points_for_players_in_lineup, season, week, dateteams):
    array = pd.read_csv(file).to_numpy()

    # sorts by predicted FPPG
    sorted(array, key=lambda x: x[5], reverse=True)
    pd.DataFrame(array).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/' + str(season) + '/Week' + str(
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

    def id_lookup(name):
        for i in range(0, len(players)):
            if players[i][3] == name:
                return players[i][0]

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
        p_id = []
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
                p_id.append(id_lookup(newcombos[combination][player]))
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
            currentlineup = currentlineup + p_id
            permutationsarr.append(currentlineup)
    print(len(permutationsarr))
    permutationsarr.sort(key=lambda x: x[-1], reverse=True)
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5','Name1Team', 'Name2Team', 'Name3Team', 'Name4Team', 'Name5Team','Name1Position', 'Name2Position', 'Name3Position', 'Name4Position', 'Name5Position','Salary', 'FPPG','p_id1','p_id2','p_id3','p_id4','p_id5']
    pd.DataFrame(permutationsarr).to_csv(
         'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/' + str(season) + '/Week' + str(
            week) + '/' + dateteams + '_BEFORE_GAME_permutations.csv', index=False, header=headers)
def filterCombosContests():
    array = pd.read_csv(
        'top_5_positions_per_contest.csv').to_numpy()
    print("Initial Length: " + str(len(array)))
    list = []
    for i in range(0, len(array)):
        qb_counter = 0
        rb_counter = 0
        wr_counter = 0
        te_counter = 0
        kicker_counter = 0
        add_to = True
        for j in range(0,5):
            # COUNTS QBS
            if str(array[i][j]) == 'QB':
                qb_counter += 1
            # COUNTS RBS
            if str(array[i][j]) == 'RB':
                rb_counter += 1
            # COUNTS RBS
            if str(array[i][j]) == 'WR':
                wr_counter += 1
            # COUNTS RBS
            if str(array[i][j]) == 'TE':
                te_counter += 1
            # COUNTS KICKERS
            if str(array[i][j]) == 'K':
                kicker_counter+=1

            # REMOVES MVP TE
            if j == 10 and str(array[i][j]) == 'TE':
                add_to = False

            # REMOVES MVP K
            if j == 10 and str(array[i][j]) == 'K':
                add_to = False

        if rb_counter == 0 and wr_counter < 2:
            add_to = False

        if qb_counter == 0 or kicker_counter > 1 or te_counter > 1:
            add_to = False

        if add_to == True:
            list.append(array[i])
    print("Length after removal: " + str(len(list)))
def filterCombosCombos(season, week, dateteams):
    array = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/' + str(season) + '/Week' + str(
        week) + '/' + dateteams + '_BEFORE_GAME_permutations.csv')
    col = array.columns
    array = array.to_numpy()

    print("Initial Length: " + str(len(array)))
    list = []
    for i in range(0,len(array)):
        lineup_names = []
        lineup_teams = []
        qb_counter = 0
        rb_counter = 0
        wr_counter = 0
        te_counter = 0
        kicker_counter = 0
        add_to = True
        for j in range(10,15):
            lineup_names.append(str(array[i][j-10]))
            lineup_teams.append(str(array[i][j-5]))
            # COUNTS QBS
            if str(array[i][j]) == 'QB':
                qb_counter += 1
            # COUNTS RBS
            if str(array[i][j]) == 'RB':
                rb_counter += 1
            # COUNTS WRS
            if str(array[i][j]) == 'WR':
                wr_counter += 1
            # COUNTS TES
            if str(array[i][j]) == 'TE':
                te_counter += 1
            # COUNTS KICKERS
            if str(array[i][j]) == 'K':
                kicker_counter+=1

            # # REMOVES MVP TE
            # if j == 10 and str(array[i][j]) == 'TE':
            #     add_to = False

            # REMOVES MVP K
            if j == 10 and str(array[i][j]) == 'K':
                add_to = False

        #REQUIREMENTS
        if 'Patrick Mahomes' not in lineup_names:
            add_to = False

        if lineup_names[0] == 'Patrick Mahomes' and ():
            pass

        #removes all non selected MVPs from lineups
        if lineup_names[0] not in ('Patrick Mahomes','Travis Kelce','Tyreek Hill','Clyde Edwards-Helaire','Lamar Jackson','Sammy Watkins','Mark Andrews','Marquise Brown',"Ty'Son Williams"):
            add_to = False

        #removes two RBs from same team in

        # #when there are no running backs, there must be at least one WR
        # if rb_counter==0 and wr_counter<2:
        #     add_to = False

        if qb_counter==0 or kicker_counter>=2 or te_counter>2:
            add_to = False

        if add_to == True :
            list.append(array[i])

    print("Length after removal: " + str(len(list)))
    list = sorted(list, key=lambda x: (x[0], -x[-6], x[1], [2], x[3], x[4]))
    pd.DataFrame(list).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/remaining_output.csv', index=False,
                                                          header=col)  # ,'Count])
    return list
def countCSVPermutations(list):
    array = pd.read_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/09192021KCBAL_reduced_players.csv').to_numpy()
    names = []

    def nameIndex(name):
        for i in range(0, len(names)):
            if str(names[i][0]) == str(name):
                return i

    for i in range(0, len(array)):
        names.append([array[i][3]] + [0, 0])

    for i in range(0, len(list)):
        for j in range(0, 5):
            if j == 0:
                names[nameIndex(list[i][j])][1] += 1
            else:
                names[nameIndex(list[i][j])][2] += 1

    print(pd.DataFrame(names))
    print('\n')
def returnCSVEntries():
    this_list = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/remaining_output.csv').to_numpy()
    ret_list = []
    for i in range(0,len(this_list)):
        ret_list.append(this_list[i][-5:])
    pd.DataFrame(ret_list).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/output_contest_file.csv', index=False)
########################################


##### DATA PIPELINE #####
def box_score_retrieval(season):
    get_Season_Schedule(season)
    schedule = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SCHEDULES/'+str(season)+'NFLScheduleAndResults.csv').to_numpy()
    game_count = 0
    for game in range(0, len(schedule)):
        if game_count <= 255 and 1 <= int(schedule[game][0]) <= 17: ############CHANGE BACK TO 17
            game_count += 1

            index = list(bbref_team_abbrev_dict_2021.keys()).index(defineHomeTeam(schedule[game][4], schedule[game][6], schedule[game][5]))
            teamcode = list(bbref_team_abbrev_dict_2021.values())[index]

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
        keys = list(bbref_team_abbrev_dict_2021.keys())
        values = list(bbref_team_abbrev_dict_2021.values())
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
def updatePlayerPositionsInContestsFromDB(season):
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
    game_teams_dict_2020 = {'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL',
                    'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR',
                    'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE',
                    'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN',
                    'Detroit Lions': 'DET', 'Green Bay Packers': 'GNB', 'Houston Texans': 'HOU',
                    'Indianapolis Colts': 'IND',
                    'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KAN', 'Las Vegas Raiders': 'LVR',
                    'Los Angeles Chargers': 'LAC',
                    'Los Angeles Rams': 'LAR', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN',
                    'New England Patriots': 'NWE',
                    'New Orleans Saints': 'NOR', 'New York Giants': 'NYG', 'New York Jets': 'NYJ',
                               'Philadelphia Eagles': 'PHI',
                               'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SFO', 'Seattle Seahawks': 'SEA',
                               'Tampa Bay Buccaneers': 'TAM',
                               'Tennessee Titans': 'TEN', 'Washington Football Team': 'WAS'}
    t_keys = game_teams_dict_2020.keys()
    t_values = game_teams_dict_2020.values()
    # Season Totals for Top 5 Contest Outcomes
    distinct_positional_combinations = []

    qb_position_counter = [0, 0, 0, 0, 0]
    rb_position_counter = [0, 0, 0, 0, 0]
    wr_position_counter = [0, 0, 0, 0, 0]
    te_position_counter = [0, 0, 0, 0, 0]
    k_position_counter = [0, 0, 0, 0, 0]
    other_position_counter = [0, 0, 0, 0, 0]

    winner_qb_position_counter = [0, 0, 0, 0, 0]
    winner_rb_position_counter = [0, 0, 0, 0, 0]
    winner_wr_position_counter = [0, 0, 0, 0, 0]
    winner_te_position_counter = [0, 0, 0, 0, 0]
    winner_k_position_counter = [0, 0, 0, 0, 0]
    winner_other_position_counter = [0, 0, 0, 0, 0]

    loser_qb_position_counter = [0, 0, 0, 0, 0]
    loser_rb_position_counter = [0, 0, 0, 0, 0]
    loser_wr_position_counter = [0, 0, 0, 0, 0]
    loser_te_position_counter = [0, 0, 0, 0, 0]
    loser_k_position_counter = [0, 0, 0, 0, 0]
    loser_other_position_counter = [0, 0, 0, 0, 0]


    for file in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/2020/'):


        lineup = ['','','','','']
        df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/2020/' + file)
        col = df.columns
        arr = df.to_numpy()

        #ASSIGN WINNER AND LOSER
        index = str(arr[0][2]).index('V')
        if str(arr[0][2])[index+1] == 'e' or str(arr[0][2])[index+1] == 'i':
            index2 = str(arr[0][2])[index+1:].index('V')
            index = index+index2+1
        w = list(t_keys).index(str(arr[0][2])[:index])
        loser = list(t_values)[w]
        l = list(t_keys).index(str(arr[0][2])[index+1:])
        winner = list(t_values)[l]

        for entry in range(0, 5):
            is_winner = True
            if str(arr[entry][3]) != winner:
                is_winner = False

            lineup[entry] = arr[entry][5].upper()
            if str(arr[entry][5]).upper() == 'QB':
                qb_position_counter[entry] += 1
                if is_winner == True:
                    winner_qb_position_counter[entry]+=1
                else:
                    loser_qb_position_counter[entry]+=1
            elif str(arr[entry][5]).upper() == 'RB':
                rb_position_counter[entry] += 1
                if is_winner == True:
                    winner_rb_position_counter[entry]+=1
                else:
                    loser_rb_position_counter[entry]+=1
            elif str(arr[entry][5]).upper() == 'WR':
                wr_position_counter[entry] += 1
                if is_winner == True:
                    winner_wr_position_counter[entry]+=1
                else:
                    loser_wr_position_counter[entry]+=1
            elif str(arr[entry][5]).upper() == 'TE':
                te_position_counter[entry] += 1
                if is_winner == True:
                    winner_te_position_counter[entry]+=1
                else:
                    loser_te_position_counter[entry]+=1
            elif str(arr[entry][5]).upper() == 'K':
                k_position_counter[entry] += 1
                if is_winner == True:
                    winner_k_position_counter[entry]+=1
                else:
                    loser_k_position_counter[entry]+=1
            else:
                other_position_counter[entry] += 1
                if is_winner == True:
                    winner_other_position_counter[entry]+=1
                else:
                    loser_other_position_counter[entry]+=1
        distinct_positional_combinations.append(lineup)

    print("All 2020 Lineups DFS Contests Breakdown")
    print("QBs: " + '\t' + str(qb_position_counter) + '\t' + str(sum(qb_position_counter)/256) + ' per lineup')
    print("RBs: " + '\t' + str(rb_position_counter) + '\t' + str(sum(rb_position_counter)/256) + ' per lineup')
    print("WRs: " + '\t' + str(wr_position_counter) + '\t' + str(sum(wr_position_counter)/256) + ' per lineup')
    print("TEs: " + '\t' + str(te_position_counter) + '\t' + str(sum(te_position_counter)/256) + ' per lineup')
    print("Ks: " + '\t' + str(k_position_counter) + '\t' + str(sum(k_position_counter)/256) + ' per lineup')
    print("Other: " + '\t' + str(other_position_counter) + '\t' + str(sum(other_position_counter)/256) + ' per lineup')
    total_players = sum(qb_position_counter) + sum(rb_position_counter) + sum(wr_position_counter) + sum(te_position_counter) + sum(
        k_position_counter) + sum(other_position_counter)
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players/256))
    print('\n')

    print("Place: ALL 2020 MVP")
    print("QBs: " + '\t' + str(qb_position_counter[0]) + '\t' + str((qb_position_counter[0] / 256) * 100) + '%')
    print("RBs: " + '\t' + str(rb_position_counter[0]) + '\t' + str((rb_position_counter[0] / 256) * 100) + '%')
    print("WRs: " + '\t' + str(wr_position_counter[0]) + '\t' + str((wr_position_counter[0] / 256) * 100) + '%')
    print("TEs: " + '\t' + str(te_position_counter[0]) + '\t' + str((te_position_counter[0] / 256) * 100) + '%')
    print("Ks: " + '\t' + str(k_position_counter[0]) + '\t' + str((k_position_counter[0] / 256) * 100) + '%')
    print("Other: " + '\t' + str(other_position_counter[0]) + '\t' + str((other_position_counter[0] / 256) * 100) + '%')
    total_players = qb_position_counter[0] + rb_position_counter[0] + wr_position_counter[0] + te_position_counter[0] + k_position_counter[0] + other_position_counter[0]
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n')

    print("Place: ALL 2020 UTIL")
    qb_position_counter = qb_position_counter[1] + qb_position_counter[2] + qb_position_counter[3] + qb_position_counter[4]
    rb_position_counter = rb_position_counter[1] + rb_position_counter[2] + rb_position_counter[3] + rb_position_counter[4]
    wr_position_counter = wr_position_counter[1] + wr_position_counter[2] + wr_position_counter[3] + wr_position_counter[4]
    te_position_counter = te_position_counter[1] + te_position_counter[2] + te_position_counter[3] + te_position_counter[4]
    k_position_counter = k_position_counter[1] + k_position_counter[2] + k_position_counter[3] + k_position_counter[4]
    other_position_counter = other_position_counter[1] + other_position_counter[2] + other_position_counter[3] + other_position_counter[4]
    print("QBs: " + '\t' + str(qb_position_counter) + '\t' + str((qb_position_counter / 256) * 100/4) + '%')
    print("RBs: " + '\t' + str(rb_position_counter) + '\t' + str((rb_position_counter / 256) * 100/4) + '%')
    print("WRs: " + '\t' + str(wr_position_counter) + '\t' + str((wr_position_counter / 256) * 100/4) + '%')
    print("TEs: " + '\t' + str(te_position_counter) + '\t' + str((te_position_counter / 256) * 100/4) + '%')
    print("Ks: " + '\t' + str(k_position_counter) + '\t' + str((k_position_counter / 256) * 100/4) + '%')
    print("Other: " + '\t' + str(other_position_counter) + '\t' + str((other_position_counter / 256) * 100/4) + '%')
    total_players = qb_position_counter + rb_position_counter + wr_position_counter + te_position_counter + \
                    k_position_counter + other_position_counter
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n\n\n')



    print("WINNING TEAMS DFS Contests Breakdown")
    print("QBs: " + '\t' + str(winner_qb_position_counter) + '\t' + str(sum(winner_qb_position_counter) / 256) + ' per lineup')
    print("RBs: " + '\t' + str(winner_rb_position_counter) + '\t' + str(sum(winner_rb_position_counter) / 256) + ' per lineup')
    print("WRs: " + '\t' + str(winner_wr_position_counter) + '\t' + str(sum(winner_wr_position_counter) / 256) + ' per lineup')
    print("TEs: " + '\t' + str(winner_te_position_counter) + '\t' + str(sum(winner_te_position_counter) / 256) + ' per lineup')
    print("Ks: " + '\t' + str(winner_k_position_counter) + '\t' + str(sum(winner_k_position_counter) / 256) + ' per lineup')
    print(
        "Other: " + '\t' + str(winner_other_position_counter) + '\t' + str(sum(winner_other_position_counter) / 256) + ' per lineup')
    total_players = sum(winner_qb_position_counter) + sum(winner_rb_position_counter) + sum(winner_wr_position_counter) + sum(
        winner_te_position_counter) + sum(
        winner_k_position_counter) + sum(winner_other_position_counter)
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n')

    print("Place: WINNING TEAMS 2020 MVP")
    print("QBs: " + '\t' + str(winner_qb_position_counter[0]) + '\t' + str((winner_qb_position_counter[0] / 256) * 100) + '%')
    print("RBs: " + '\t' + str(winner_rb_position_counter[0]) + '\t' + str((winner_rb_position_counter[0] / 256) * 100) + '%')
    print("WRs: " + '\t' + str(winner_wr_position_counter[0]) + '\t' + str((winner_wr_position_counter[0] / 256) * 100) + '%')
    print("TEs: " + '\t' + str(winner_te_position_counter[0]) + '\t' + str((winner_te_position_counter[0] / 256) * 100) + '%')
    print("Ks: " + '\t' + str(winner_k_position_counter[0]) + '\t' + str((winner_k_position_counter[0] / 256) * 100) + '%')
    print("Other: " + '\t' + str(winner_other_position_counter[0]) + '\t' + str((winner_other_position_counter[0] / 256) * 100) + '%')
    total_players = winner_qb_position_counter[0] + winner_rb_position_counter[0] + winner_wr_position_counter[0] + winner_te_position_counter[0] + \
                    winner_k_position_counter[0] + winner_other_position_counter[0]
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n')


    print("Place: WINNING TEAMS 2020 UTIL")
    winner_qb_position_counter = winner_qb_position_counter[1] + winner_qb_position_counter[2] + winner_qb_position_counter[3] + \
                          winner_qb_position_counter[4]
    winner_rb_position_counter = winner_rb_position_counter[1] + winner_rb_position_counter[2] + winner_rb_position_counter[3] + \
                          winner_rb_position_counter[4]
    winner_wr_position_counter = winner_wr_position_counter[1] + winner_wr_position_counter[2] + winner_wr_position_counter[3] + \
                          winner_wr_position_counter[4]
    winner_te_position_counter = winner_te_position_counter[1] + winner_te_position_counter[2] + winner_te_position_counter[3] + \
                          winner_te_position_counter[4]
    winner_k_position_counter = winner_k_position_counter[1] + winner_k_position_counter[2] + winner_k_position_counter[3] + winner_k_position_counter[4]
    winner_other_position_counter = winner_other_position_counter[1] + winner_other_position_counter[2] + winner_other_position_counter[3] + \
                             winner_other_position_counter[4]
    print("QBs: " + '\t' + str(winner_qb_position_counter) + '\t' + str((winner_qb_position_counter / 256) * 100 / 4) + '%')
    print("RBs: " + '\t' + str(winner_rb_position_counter) + '\t' + str((winner_rb_position_counter / 256) * 100 / 4) + '%')
    print("WRs: " + '\t' + str(winner_wr_position_counter) + '\t' + str((winner_wr_position_counter / 256) * 100 / 4) + '%')
    print("TEs: " + '\t' + str(winner_te_position_counter) + '\t' + str((winner_te_position_counter / 256) * 100 / 4) + '%')
    print("Ks: " + '\t' + str(winner_k_position_counter) + '\t' + str((winner_k_position_counter / 256) * 100 / 4) + '%')
    print("Other: " + '\t' + str(winner_other_position_counter) + '\t' + str((winner_other_position_counter / 256) * 100 / 4) + '%')
    total_players = winner_qb_position_counter + winner_rb_position_counter + winner_wr_position_counter + winner_te_position_counter + \
                    winner_k_position_counter + winner_other_position_counter
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n\n\n')




    print("LOSING TEAMS DFS Contests Breakdown")
    print("QBs: " + '\t' + str(loser_qb_position_counter) + '\t' + str(sum(loser_qb_position_counter) / 256) + ' per lineup')
    print("RBs: " + '\t' + str(loser_rb_position_counter) + '\t' + str(sum(loser_rb_position_counter) / 256) + ' per lineup')
    print("WRs: " + '\t' + str(loser_wr_position_counter) + '\t' + str(sum(loser_wr_position_counter) / 256) + ' per lineup')
    print("TEs: " + '\t' + str(loser_te_position_counter) + '\t' + str(sum(loser_te_position_counter) / 256) + ' per lineup')
    print("Ks: " + '\t' + str(loser_k_position_counter) + '\t' + str(sum(loser_k_position_counter) / 256) + ' per lineup')
    print(
        "Other: " + '\t' + str(loser_other_position_counter) + '\t' + str(sum(loser_other_position_counter) / 256) + ' per lineup')
    total_players = sum(loser_qb_position_counter) + sum(loser_rb_position_counter) + sum(loser_wr_position_counter) + sum(
        loser_te_position_counter) + sum(
        loser_k_position_counter) + sum(loser_other_position_counter)
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n')

    print("Place: LOSING TEAMS 2020 MVP")
    print("QBs: " + '\t' + str(loser_qb_position_counter[0]) + '\t' + str((loser_qb_position_counter[0] / 256) * 100) + '%')
    print("RBs: " + '\t' + str(loser_rb_position_counter[0]) + '\t' + str((loser_rb_position_counter[0] / 256) * 100) + '%')
    print("WRs: " + '\t' + str(loser_wr_position_counter[0]) + '\t' + str((loser_wr_position_counter[0] / 256) * 100) + '%')
    print("TEs: " + '\t' + str(loser_te_position_counter[0]) + '\t' + str((loser_te_position_counter[0] / 256) * 100) + '%')
    print("Ks: " + '\t' + str(loser_k_position_counter[0]) + '\t' + str((loser_k_position_counter[0] / 256) * 100) + '%')
    print("Other: " + '\t' + str(loser_other_position_counter[0]) + '\t' + str((loser_other_position_counter[0] / 256) * 100) + '%')
    total_players = loser_qb_position_counter[0] + loser_rb_position_counter[0] + loser_wr_position_counter[0] + loser_te_position_counter[0] + \
                    loser_k_position_counter[0] + loser_other_position_counter[0]
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n')

    print("Place: LOSING TEAMS 2020 UTIL")
    loser_qb_position_counter = loser_qb_position_counter[1] + loser_qb_position_counter[2] + loser_qb_position_counter[3] + \
                          loser_qb_position_counter[4]
    loser_rb_position_counter = loser_rb_position_counter[1] + loser_rb_position_counter[2] + loser_rb_position_counter[3] + \
                          loser_rb_position_counter[4]
    loser_wr_position_counter = loser_wr_position_counter[1] + loser_wr_position_counter[2] + loser_wr_position_counter[3] + \
                          loser_wr_position_counter[4]
    loser_te_position_counter = loser_te_position_counter[1] + loser_te_position_counter[2] + loser_te_position_counter[3] + \
                          loser_te_position_counter[4]
    loser_k_position_counter = loser_k_position_counter[1] + loser_k_position_counter[2] + loser_k_position_counter[3] + loser_k_position_counter[4]
    loser_other_position_counter = loser_other_position_counter[1] + loser_other_position_counter[2] + loser_other_position_counter[3] + \
                             loser_other_position_counter[4]
    print("QBs: " + '\t' + str(loser_qb_position_counter) + '\t' + str((loser_qb_position_counter / 256) * 100 / 4) + '%')
    print("RBs: " + '\t' + str(loser_rb_position_counter) + '\t' + str((loser_rb_position_counter / 256) * 100 / 4) + '%')
    print("WRs: " + '\t' + str(loser_wr_position_counter) + '\t' + str((loser_wr_position_counter / 256) * 100 / 4) + '%')
    print("TEs: " + '\t' + str(loser_te_position_counter) + '\t' + str((loser_te_position_counter / 256) * 100 / 4) + '%')
    print("Ks: " + '\t' + str(loser_k_position_counter) + '\t' + str((loser_k_position_counter / 256) * 100 / 4) + '%')
    print("Other: " + '\t' + str(loser_other_position_counter) + '\t' + str((loser_other_position_counter / 256) * 100 / 4) + '%')
    total_players = loser_qb_position_counter + loser_rb_position_counter + loser_wr_position_counter + loser_te_position_counter + \
                    loser_k_position_counter + loser_other_position_counter
    print("Total Players: " + str(total_players) + '\t' + "Total Players per Contest: " + str(total_players / 256))
    print('\n\n\n')



    sorted(distinct_positional_combinations, key=lambda x: x[-1])
    pd.DataFrame(distinct_positional_combinations).to_csv('top_5_positions_per_contest.csv',index=False,header=['1st','2nd','3rd','4th','5th']) #,'Count])
def countLineups():
    df = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/top_5_positions_per_contest.csv')
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
    pd.DataFrame(new_lineups).to_csv('all_lineups_position_count.csv',index=False,header=['QB_count','RB_count','WR_count','TE_count','K_count','OTHER_count','count'])



main(2020)