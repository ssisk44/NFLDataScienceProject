import math
import random
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

directory = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/'
game = '09262021GBSF'
file = directory + game + '_reduced_players.csv'

team_abbrev_list = ['Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills', 'Carolina Panthers',
                    'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns', 'Dallas Cowboys', 'Denver Broncos',
                    'Detroit Lions', 'Green Bay Packers', 'Houston Texans', 'Indianapolis Colts',
                    'Jacksonville Jaguars', 'Kansas City Chiefs', 'Las Vegas Raiders', 'Los Angeles Chargers',
                    'Los Angeles Rams', 'Miami Dolphins', 'Minnesota Vikings', 'New England Patriots',
                    'New Orleans Saints', 'New York Giants', 'New York Jets', 'Philadelphia Eagles',
                    'Pittsburgh Steelers', 'San Francisco 49ers', 'Seattle Seahawks', 'Tampa Bay Buccaneers',
                    'Tennessee Titans', 'Washington Football Team', 'Oakland Raiders', 'Washington Redskins']

bbref_team_abbrev_dict_2016_to_2017 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
                                       'Buffalo Bills': 'buf', 'Carolina Panthers': 'car',
                                       'Chicago Bears': 'chi', 'Cincinnati Bengals': 'cin', 'Cleveland Browns': 'cle',
                                       'Dallas Cowboys': 'dal', 'Denver Broncos': 'den',
                                       'Detroit Lions': 'det', 'Green Bay Packers': 'gnb', 'Houston Texans': 'htx',
                                       'Indianapolis Colts': 'clt',
                                       'Jacksonville Jaguars': 'jax', 'Kansas City Chiefs': 'kan',
                                       'San Diego Chargers': 'sdg',
                                       'Los Angeles Rams': 'ram', 'Miami Dolphins': 'mia', 'Minnesota Vikings': 'min',
                                       'New England Patriots': 'nwe',
                                       'New Orleans Saints': 'nor', 'New York Giants': 'nyg', 'New York Jets': 'nyj',
                                       'Philadelphia Eagles': 'phi',
                                       'Pittsburgh Steelers': 'pit', 'San Francisco 49ers': 'sfo',
                                       'Seattle Seahawks': 'sea',
                                       'Tampa Bay Buccaneers': 'tam',
                                       'Tennessee Titans': 'oti', 'Oakland Raiders': 'rai',
                                       'Washington Redskins': 'was'}

bbref_team_abbrev_dict_2017_to_2019 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
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
                                       'Pittsburgh Steelers': 'pit', 'San Francisco 49ers': 'sfo',
                                       'Seattle Seahawks': 'sea',
                                       'Tampa Bay Buccaneers': 'tam',
                                       'Tennessee Titans': 'oti', 'Oakland Raiders': 'rai',
                                       'Washington Redskins': 'was'}

bbref_team_abbrev_dict_2020_to_2021 = {'Arizona Cardinals': 'crd', 'Atlanta Falcons': 'atl', 'Baltimore Ravens': 'rav',
                                       'Buffalo Bills': 'buf', 'Carolina Panthers': 'car',
                                       'Chicago Bears': 'chi', 'Cincinnati Bengals': 'cin', 'Cleveland Browns': 'cle',
                                       'Dallas Cowboys': 'dal', 'Denver Broncos': 'den',
                                       'Detroit Lions': 'det', 'Green Bay Packers': 'gnb', 'Houston Texans': 'htx',
                                       'Indianapolis Colts': 'clt',
                                       'Jacksonville Jaguars': 'jax', 'Kansas City Chiefs': 'kan',
                                       'Las Vegas Raiders': 'rai',
                                       'Los Angeles Chargers': 'sdg',
                                       'Los Angeles Rams': 'ram', 'Miami Dolphins': 'mia', 'Minnesota Vikings': 'min',
                                       'New England Patriots': 'nwe',
                                       'New Orleans Saints': 'nor', 'New York Giants': 'nyg', 'New York Jets': 'nyj',
                                       'Philadelphia Eagles': 'phi',
                                       'Pittsburgh Steelers': 'pit', 'San Francisco 49ers': 'sfo',
                                       'Seattle Seahawks': 'sea',
                                       'Tampa Bay Buccaneers': 'tam',
                                       'Tennessee Titans': 'oti', 'Washington Football Team': 'was'}


def main():
    ###CONTESTS###
    create_Combos(0, 2021, 3, game)
    filter_Combos_Combos(2021, 3, game)
    count_CSV_Permutations([])
    return_CSV_Entries()

    ###DATA PIPELINE###
    # get_Box_Scores(2021)
    # getSimplePositions(2016) ###ERASES MANUALLY INPUT PLAYERS IN CASE OF NAN
    # updateGameHistoryWithSimplePlayerPositions(2016)
    # getDepthChartPositions(2016) ###ERASES MANUALLY INPUT PLAYERS IN CASE OF NAN

    ###DATA ANALYSIS###
    # create_Analysis_Table()
    # print_Analysis_Table()
    # top_5_pattern_counter()
    None


##### CONTEST PERMUTATION CREATION #####
def create_Combos(min_points_for_players_in_lineup, season, week, dateteams):
    array = pd.read_csv(file).to_numpy()
    sorted(array, key=lambda x: x[5], reverse=True)
    found = False
    # for files in os.listdir(directory + str(season) + '/Week' + str(
    #         week) + '/'):
    #     if str(file[-32:-19]) in files:
    #         found = True
    #         break
    # if found == False:

    pd.DataFrame(array).to_csv(
        directory + str(season) + '/Week' + str(
            week) + '/' + dateteams + '_BEFORE_GAME_reduced_players.csv', index=False)

    # sorts by predicted FPPG

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
            currentlineup = currentlineup + p_teams + p_positions
            currentlineup.append(salary)
            currentlineup.append(lineupscore)
            currentlineup = currentlineup + p_id
            permutationsarr.append(currentlineup)
    print(len(permutationsarr))
    permutationsarr.sort(key=lambda x: x[-1], reverse=True)
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Name1Team', 'Name2Team', 'Name3Team', 'Name4Team',
               'Name5Team', 'Name1Position', 'Name2Position', 'Name3Position', 'Name4Position', 'Name5Position',
               'Salary', 'FPPG', 'p_id1', 'p_id2', 'p_id3', 'p_id4', 'p_id5']
    pd.DataFrame(permutationsarr).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/' + str(season) + '/Week' + str(
            week) + '/' + dateteams + '_BEFORE_GAME_permutations.csv', index=False, header=headers)


def filter_Combos_Combos(season, week, dateteams):
    array = pd.read_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DFS_FILES/' + str(season) + '/Week' + str(
            week) + '/' + dateteams + '_BEFORE_GAME_permutations.csv')
    col = array.columns
    array = array.to_numpy()

    print("Initial Length: " + str(len(array)))
    list = []
    for i in range(0, len(array)):
        lineup_names = []
        lineup_teams = []

        team1 = ''
        team2 = ''
        team1_mvp = ''
        team2_mvp = ''
        all_positions = []
        team1_positions = []
        team2_positions = []
        team1_players = []
        team2_players = []

        def countPlayerTeamPositions(team, position):
            this_team = ''
            if team == team1:
                this_team = team1_players
            if team == team2:
                this_team = team2_players
            count = 0
            for player in range(0, len(this_team)):
                if position in this_team[player]:
                    count += 1
            return count

        qb_counter = 0
        rb_counter = 0
        rb1_counter = 0
        rb2_counter = 0
        rb3_counter = 0
        wr_counter = 0
        wr1_counter = 0
        wr2_counter = 0
        wr3_counter = 0
        wr4_counter = 0
        te_counter = 0
        te1_counter = 0
        te2_counter = 0
        te3_counter = 0
        kicker_counter = 0
        add_to = True
        for j in range(10, 15):
            if j == 10:
                team1 = str(array[i][j - 5])
            if j > 10 and str(array[i][j - 5]) != team1 and team2 == '':
                team2 = str(array[i][j - 5])

            all_positions.append(str(array[i][j]))
            if str(array[i][j - 5]) == team1:
                team1_players.append(str(array[i][j]))
                if j == 10:
                    team1_mvp = str(array[i][j])
                team1_positions.append(str(array[i][j]))

            if str(array[i][j - 5]) == team2:
                team2_players.append(str(array[i][j]))
                if j == 10:
                    team2_mvp = str(array[i][j])
                team2_positions.append(str(array[i][j]))

            lineup_teams.append(str(array[i][j - 5]))
            lineup_names.append(str(array[i][j - 10]))

            # COUNTS QBS
            if 'QB' in str(array[i][j]):
                qb_counter += 1
            # COUNTS RBS
            elif 'RB' in str(array[i][j]):
                rb_counter += 1
                if 'RB1' in str(array[i][j]):
                    rb1_counter += 1
                if 'RB2' in str(array[i][j]):
                    rb2_counter += 1
                if 'RB3' in str(array[i][j]):
                    rb3_counter += 1
            # COUNTS WRS
            elif 'WR' in str(array[i][j]):
                wr_counter += 1
                if 'WR1' in str(array[i][j]):
                    wr1_counter += 1
                if 'WR2' in str(array[i][j]):
                    wr2_counter += 1
                if 'WR3' in str(array[i][j]):
                    wr3_counter += 1
                if 'WR4' in str(array[i][j]):
                    wr4_counter += 1
            # COUNTS TES
            elif 'TE' in str(array[i][j]):
                te_counter += 1
                if 'TE1' in str(array[i][j]):
                    te1_counter += 1
                if 'TE2' in str(array[i][j]):
                    te2_counter += 1
                if 'TE3' in str(array[i][j]):
                    te3_counter += 1
            # COUNTS KICKERS
            elif 'K' in str(array[i][j]):
                kicker_counter += 1

            # REMOVES MVP K
            if j == 10 and str(array[i][j]) == 'K':
                add_to = False

        # GAME SPECIFIC FILTERS


        # #ATL has 3 or less in top 5
        # if (team1 == 'ATL' and len(team1_positions) >=4) or (team1 == 'ATL' and len(team2_positions) >=4):
        #     add_to = False

        if 'Randall Cobb' in lineup_names and 'Aaron Rodgers' not in lineup_names:
            add_to = False

        if ('Mohamed Sanu' in lineup_names or 'Trent Sherfield' in lineup_names) and 'Jimmy Garoppolo' not in lineup_names:
            add_to = False

        if (team1 == 'SF' and team1_positions.count('WR2') == 1 and team1_positions.count('WR3') == 1) or (
                team1 == 'SF' and team2_positions.count('WR2') == 1 and team2_positions.count('WR3') == 1):
            add_to = False

        if (team1 == 'SF' and team1_positions.count('WR4') == 1 and team1_positions.count('WR3') == 1) or (
                team1 == 'SF' and team2_positions.count('WR4') == 1 and team2_positions.count('WR3') == 1):
            add_to = False

        if (team1 == 'SF' and team1_positions.count('WR2') == 1 and team1_positions.count('WR4') == 1) or (
                team1 == 'SF' and team2_positions.count('WR2') == 1 and team2_positions.count('WR4') == 1):
            add_to = False

        # REMOVE NON MVP CHOICES
        if lineup_names[0] not in ('Aaron Rodgers', 'Aaron Jones','Davante Adams','Jimmy Garappolo','Deebo Samuel','George Kittle'):
            add_to=False

        # ALL GAME FILTERS
        #**********************************************************
        if (team1_positions.count('RB1') == 1 and team1_positions.count('RB2') == 1) or (team2_positions.count('RB1') == 1 and team2_positions.count('RB2') == 1):
            add_to = False

        if (team1_positions.count('WR3') == 1 and team1_positions.count('RB2') == 1) or (team2_positions.count('WR3') == 1 and team2_positions.count('RB2') == 1):
            add_to = False

        if ('RB' in team1_mvp and 'WR' in team1_positions and 'QB' not in team1_positions) or ('RB' in team2_mvp and 'WR' in team2_positions and 'QB' not in team2_positions):
            add_to = False

        # No K and RB2
        if rb2_counter>=1 and 'K' in all_positions:
            add_to = False

        # No K and TE2
        if 'TE2' in all_positions and 'K' in all_positions:
            add_to = False

        # No TE2 and RB2
        if 'TE2' in all_positions and rb2_counter>=1:
            add_to = False

        #***********************************************************
        # must be at least one QB
        if countPlayerTeamPositions(team1, 'QB') == 0 and countPlayerTeamPositions(team2, 'QB') == 0:
            add_to = False

        # no two RBs from same team
        if countPlayerTeamPositions(team1, 'RB') >= 2 or countPlayerTeamPositions(team2, 'QB') >= 2:
            add_to = False

        # no three WRs from same team
        if countPlayerTeamPositions(team1, 'WR') >= 3 or countPlayerTeamPositions(team2, 'WR') >= 3:
            add_to = False

        # no two TEs from same team
        if countPlayerTeamPositions(team1, 'TE') >= 2 or countPlayerTeamPositions(team2, 'TE') >= 2:
            add_to = False

        # less than one TE and WR4 combined in a lineup (each team)
        if (countPlayerTeamPositions(team1, 'TE') >= 2 and countPlayerTeamPositions(team1, 'WR4') >= 2) or (
                countPlayerTeamPositions(team2, 'TE') >= 2 and countPlayerTeamPositions(team2, 'WR4') >= 2):
            add_to = False

        # WR3 WR4 TE2 (each team)  <= 1
        if (countPlayerTeamPositions(team1, 'WR3') + countPlayerTeamPositions(team1, 'WR4') + countPlayerTeamPositions(
                team1, 'TE2') >= 2) or (countPlayerTeamPositions(team2, 'WR3') + countPlayerTeamPositions(team2,
                                                                                                          'WR4') + countPlayerTeamPositions(
                team2, 'TE2') >= 2):
            add_to = False

        # RB3 WR4 TE2 (each team)  <= 1
        if (countPlayerTeamPositions(team1, 'RB3') + countPlayerTeamPositions(team1, 'TE2') + countPlayerTeamPositions(
                team1, 'WR4') >= 2) or (countPlayerTeamPositions(team2, 'RB3') + countPlayerTeamPositions(team2,
                                                                                                          'TE2') + countPlayerTeamPositions(
                team2, 'WR4') >= 2):
            add_to = False

        # 0 QB and 2 WR (same team) == 0
        if (countPlayerTeamPositions(team1, 'QB') == 0 and countPlayerTeamPositions(team1, 'WR') >= 2) or (
                countPlayerTeamPositions(team2, 'QB') == 0 and countPlayerTeamPositions(team2, 'WR') >= 2):
            add_to = False

        # 0 QB and 1 WR and 1 TE (same team) == 0
        if (countPlayerTeamPositions(team1, 'QB') == 0 and countPlayerTeamPositions(team1,
                                                                                    'WR') >= 1 and countPlayerTeamPositions(
                team1, 'TE') >= 1) or (countPlayerTeamPositions(team2, 'QB') == 0 and countPlayerTeamPositions(team2,
                                                                                                               'WR') >= 1 and countPlayerTeamPositions(
                team2, 'TE') >= 1):
            add_to = False

        # *****Research Paper Based******
        # If QB,TE,WR MVP and other team cant have 4 players
        if (('WR' in team1_mvp or 'TE' in team1_mvp or 'QB' in team1_mvp) and len(team2_positions) >= 4) or (
                ('WR' in team2_mvp or 'TE' in team2_mvp or 'QB' in team2_mvp) and len(team1_positions) >= 4):
            add_to = False

        # if wr is mvp there are no TEs on same team
        if ('WR' in team1_mvp and 'TE' in team1_positions) or ('WR' in team2_mvp and 'TE' in team2_positions):
            add_to = False

        # if WR MVP must be WR on other team
        if ('WR' in team1_mvp and sum('WR' in s for s in team2_positions) == 0) or (
                'WR' in team2_mvp and sum('WR' in s for s in team1_positions) == 0):
            add_to = False

        # If QB MVP there must be a WR on same team
        if ('QB' in team1_mvp and sum('WR' in s for s in team1_positions) == 0) or (
                'QB' in team2_mvp and sum('WR' in s for s in team2_positions) == 0):
            add_to = False

        # if QB MVP no kickers
        if ('QB' in team1_mvp and kicker_counter != 0) or ('QB' in team2_mvp and kicker_counter != 0):
            add_to = False

        # if RB MVP no kicker on other team
        if ('RB' in team1_mvp and sum('K' in s for s in team2_positions) != 0) or (
                'RB' in team2_mvp and sum('K' in s for s in team1_positions) != 0):
            add_to = False

        # if RB MVP no same team TE
        if ('RB' in team1_mvp and sum('TE' in s for s in team1_positions) > 0) or (
                'RB' in team2_mvp and sum('TE' in s for s in team2_positions) != 0):
            add_to = False

        # if there is a kicker you cant have (3wrs or more that two on either team, 1qb, 1TE, 2-3RBs)
        if kicker_counter == 1 and (
                wr_counter >= 3 or countPlayerTeamPositions(team1, 'WR') >= 2 or countPlayerTeamPositions(team2,
                                                                                                          'WR') >= 2 or qb_counter >= 2 or te_counter >= 2 or 1 < rb_counter >= 3):
            add_to = False

        # GENERAL SINGLE GAME DFS FILTERS
        # depth chart position basic filters
        if rb2_counter >= 2 or rb3_counter >= 2 or wr3_counter >= 2 or wr4_counter >= 2 or te1_counter >= 2 or te2_counter >= 2 or te3_counter >= 2:
            add_to = False

        # simple position basic filters
        if qb_counter >= 3 or rb_counter >= 3 or wr_counter >= 4 or te_counter >= 3 or kicker_counter >= 2:
            add_to = False

        if add_to == True:
            list.append(array[i])

    print("Length after removal: " + str(len(list)))
    this_list = sorted(list, key=lambda x: (x[0], -x[-6], x[1], [2], x[3], x[4]))
    pd.DataFrame(this_list).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/remaining_output.csv', index=False,
                                   header=col)  # ,'Count])
    return list


def count_CSV_Permutations(list):
    array = pd.read_csv(file).to_numpy()
    perms = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/remaining_output.csv').to_numpy()
    if len(list) != 0:
        perms = list

    list_mvp = []
    list_util = []

    names = []

    # get names of reduced players
    # for every entry in perms count mvps by player
    # for every entry in perms count utils by player

    for i in range(0, len(array)):
        names.append([array[i][3]])

    for i in range(0, len(perms)):
        for j in range(0, 5):
            if j == 0:
                list_mvp.append(perms[i][0])
            else:
                list_util.append(perms[i][j])

    for i in range(0, len(names)):
        name = names[i][0]
        names[i].append(list_mvp.count(name))
        names[i].append(list_util.count(name))
        names[i].append(str(round(float(list_mvp.count(name) / len(list_mvp) * 100), 2)) + '%')
        names[i].append(str(round(float(list_util.count(name) / len(list_mvp) * 100), 2)) + '%')
        names[i].append(str(round(float(float(names[i][3][:-1]) + float(names[i][4][:-1])), 2)) + '%')

    x = pd.DataFrame(names, columns=['Name', 'MVPs', 'UTILs', 'MVP Exposure', 'UTIL Exposure', 'Total Exposure'])
    x.to_csv('Exposure.csv', index=False)
    pd.set_option('display.max_columns', None)
    # print(x)


def return_CSV_Entries():
    this_list = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/remaining_output.csv').to_numpy()
    ret_list = []
    name_list = []
    for i in range(0, len(this_list)):
        ret_list.append(this_list[i][-5:])
        n = []
        for j in range(0, 5):
            n.append(this_list[i][j])
        name_list.append(n)

    rand_list = []
    rand_numbers = []
    names = []
    for i in range(0, 450):
        num = random.randint(0, len(ret_list))
        choice = ret_list[num]
        if num not in rand_numbers:
            rand_numbers.append(num)
            rand_list.append(choice)
            names.append(name_list[num])
    rand_list = rand_list + names

    pd.DataFrame(ret_list).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/output_contest_file.csv', index=False)
    pd.DataFrame(rand_list).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/random_selection_of_output_contest_file.csv', index=False)


########################################


##### DATA PIPELINE #####
def get_Box_Scores(season):
    schedule = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SCHEDULES/' + str(
        season) + 'NFLScheduleAndResults.csv').to_numpy()
    game_count = 0

    # sets team dictionairy to the right years values
    def get_Teams_Dictionairy_For_Year(season):
        if season == 2016:
            this_dict = bbref_team_abbrev_dict_2016_to_2017
        elif 2017 <= season <= 2019:
            this_dict = bbref_team_abbrev_dict_2017_to_2019
        elif 2020 <= season <= 2021:
            this_dict = bbref_team_abbrev_dict_2020_to_2021
        return this_dict

    this_dict = get_Teams_Dictionairy_For_Year(season)

    for game in range(0, len(schedule)):
        if game_count <= 255 and 1 <= int(schedule[game][0]) <= 18:
            game_count += 1

            # gets index of game for link
            index = list(this_dict.keys()).index(
                define_Home_Team(schedule[game][4], schedule[game][6], schedule[game][5]))
            teamcode = list(this_dict.values())[index]

            # make game links and get stats with them
            date = str(schedule[game][2])

            link = 'https://www.pro-football-reference.com/boxscores/' + date[0:4] + date[5:7] + date[8:] + '0' + str(
                teamcode) + '.htm'
            game = schedule[game]

            file_found = False
            for file in os.listdir(
                    'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/'):
                checkfile = (str(game[0]) + str(define_Away_Team(game[4], game[6], game[5]))[0:3] + str(
                    define_Home_Team(game[4], game[6], game[5]))[0:3] + '.csv')
                if file == checkfile:
                    file_found = True
                    break

            if file_found == False:
                get_Game_Stats(link, game, season)


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
        pd.DataFrame(newarr[1:]).to_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SCHEDULES/' + str(
            season) + 'NFLScheduleAndResults.csv', index=False, header=header)
        return newarr[1:]
    except:
        get_Season_Schedule(season)


def get_Game_Stats(link, game, season):
    chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get(link)
    df = pd.read_html(driver.page_source)
    driver.close()

    def cleanReturnDF(df):
        col = df.columns
        arr = df.to_numpy()
        index = 0
        for entry in range(0, len(arr)):
            if type(arr[entry][0]) == float:
                index = entry
        new_arr = []
        for entry in range(0, index):
            new_arr.append(arr[entry])
        for entry in range(index + 2, len(arr)):
            new_arr.append(arr[entry])
        return pd.DataFrame(new_arr, columns=col)

    # print(cleanReturnDF(df[-20]))  # k
    # print(cleanReturnDF(df[-15]))  # prr
    # print(cleanReturnDF(df[-13]))  # krpr
    # print(cleanReturnDF(df[-12]))  # kp
    def get_start_index():
        for i in range(0, len(df)):
            c = len(df[i].columns)
            if c != 3:
                return i + 1

    PRR = cleanReturnDF(df[get_start_index() - len(df) + 5]).to_numpy()  # prr
    PR_KR = cleanReturnDF(df[get_start_index() - len(df) + 7]).to_numpy()  # krpr
    K = cleanReturnDF(df[get_start_index() - len(df) + 8]).to_numpy()  # kp
    TWOPC_FG = cleanReturnDF(df[get_start_index() - len(df)]).to_numpy()

    # GET ALL THE NAMES
    names = []
    stats = []
    for player in range(0, len(PRR)):
        this_name = str(PRR[player][0])
        if this_name not in names:
            names.append(this_name)
            stats.append(PRR[player])

    for player in range(0, len(PR_KR)):
        this_name = str(PR_KR[player][0])
        if this_name not in names:
            names.append(this_name)
            stats.append(PR_KR[player])

    for player in range(0, len(K)):
        this_name = str(K[player][0])
        if this_name not in names:
            names.append(this_name)
            stats.append(K[player])

    def getPRRStats(name):
        for i in range(0, len(PRR)):
            if str(PRR[i][0]) == name:
                return PRR[i]
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getPRKRStats(name):
        for i in range(0, len(PR_KR)):
            if str(PRR[i][0]) == name:
                return [int(PR_KR[i][5]), int(PR_KR[i][10])]
        return [0, 0]

    def getKStats(K, TWOPC_FG, name):
        # get kicker names
        arr = [0, 0, 0, 0, 0, 0, 0]

        # get kicker names
        kicker_names = []
        for player in range(0, len(K)):
            this_name = K[player][0]
            if this_name not in kicker_names and (K[player][6] == '0' or K[player][7] == '0'):
                kicker_names.append(this_name)

        # score field goals ONLY for kickers
        for scoring_play in range(0, len(TWOPC_FG)):
            if name not in kicker_names:
                break
            array = TWOPC_FG[scoring_play][3].split(' ')

            if 'field goal' in str(TWOPC_FG[scoring_play][3]) and str(name) == str(str(array[0]) + ' ' + str(array[1])):
                i1 = array.index('yard')
                FG_Yards = int(array[i1 - 1])
                if FG_Yards <= 19:
                    arr[1] += 1
                elif 20 <= FG_Yards <= 29:
                    arr[2] += 1
                elif 30 <= FG_Yards <= 39:
                    arr[3] += 1
                elif 40 <= FG_Yards <= 49:
                    arr[4] += 1
                elif 50 <= FG_Yards:
                    arr[5] += 1

        # record XP
        for kicker in range(0, len(K)):
            this_name = K[kicker][0]
            if math.isnan(float(K[kicker][2])):
                continue
            elif this_name == str(name):
                arr[0] = int(K[kicker][2])

        # record 2PC
        for scoring_play in range(0, len(TWOPC_FG)):
            if '(' in str(TWOPC_FG[scoring_play][3]):
                i1 = str(TWOPC_FG[scoring_play][3]).index('(')
                i2 = str(TWOPC_FG[scoring_play][3]).index(')')
                after_TD = str(TWOPC_FG[scoring_play][3][i1 + 1:i2])
                if name in after_TD and 'pass from' in after_TD:
                    arr[6] += 1
                elif name in after_TD and 'run' in after_TD and 'run failed' not in after_TD:
                    arr[6] += 1
        return arr

    def get_team(name):
        for i in range(0, len(names)):
            if str(names[i]) == str(name):
                return str(stats[i][1])

    def lineup_scoring(entry):
        score = (int(entry[6]) * 4) + (int(entry[7]) * .04) + (int(entry[8]) * 6) + (int(entry[9]) * .1) + (
                int(entry[10]) * .5) + (
                        int(entry[11]) * 6) + (int(entry[12]) * .1) + (int(entry[13]) * -1) + (int(entry[14]) * -2) + (
                        int(entry[15]) * 6) + (
                        int(entry[16]) * 6) + (int(entry[17]) * 1) + (int(entry[18]) * 3) + (int(entry[19]) * 3) + (
                        int(entry[20]) * 3) + (
                        int(entry[21]) * 4) + (int(entry[22]) * 5) + (int(entry[23]) * 2)
        score = round(score, 2)
        return score

    def define_Home_Team(winner, loser, value):  # value = @ of matchup, returns home team
        if str(value) == '@':
            return loser
        else:
            return winner

    def define_Away_Team(winner, loser, value):  # value = @ of matchup, returns away team
        if str(value) == '@':
            return winner
        else:
            return loser

    col = ['Season', 'Week', 'Game', 'Team', 'Name', 'Position', 'PassTD', 'PassYD', 'RushTD', 'RushYD',
           'Receptions', 'RecTD',
           'RecYD', 'INT', 'FUM/L', 'KRTD', 'PRTD', 'XP', 'FG0-19', 'FG20-29', 'FG30-39', 'FG40-49', 'FG50+', '2PC',
           'Fantasy Points']
    player_data = pd.DataFrame(columns=col).to_numpy()
    for player in range(0, len(names)):
        entry = []
        entry.append(season)
        entry.append(game[0])
        entry.append(
            str(define_Away_Team(game[4], game[6], game[5])) + 'V' + str(define_Home_Team(game[4], game[6], game[5])))
        entry.append(get_team(names[player]))
        entry.append(names[player])
        entry.append('')

        P = getPRRStats(names[player])
        entry.append(P[5])
        entry.append(P[4])
        entry.append(P[13])
        entry.append(P[12])
        entry.append(P[16])
        entry.append(P[18])
        entry.append(P[17])
        entry.append(P[6])
        entry.append(P[21])

        KR = getPRKRStats(names[player])
        entry.append(KR[0])
        entry.append(KR[1])

        FG = getKStats(K, TWOPC_FG, names[player])
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
    player_data = sorted(player_data, key=lambda x: float(x[-1]), reverse=True)
    pd.DataFrame(player_data).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/' + str(game[0]) + str(
            define_Away_Team(game[4], game[6], game[5]))[0:3] + str(define_Home_Team(game[4], game[6], game[5]))[
                                                                0:3] + '.csv', index=False, header=col)


def define_Home_Team(winner, loser, value):  # value = @ of matchup, returns home team
    if str(value) == '@':
        return loser
    else:
        return winner


def define_Away_Team(winner, loser, value):  # value = @ of matchup, returns away team
    if str(value) == '@':
        return winner
    else:
        return loser


def getSimplePositions(season):
    directory = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SIMPLEPOSITIONROSTERS/' + str(season) + '/'

    def cleanReturnDF(df):
        col = df.columns
        arr = df.to_numpy()
        index = 0
        for entry in range(0, len(arr)):
            if type(arr[entry][0]) == float:
                index = entry
        new_arr = []
        for entry in range(0, index):
            new_arr.append(arr[entry])
        for entry in range(index + 2, len(arr)):
            new_arr.append(arr[entry])
        return pd.DataFrame(new_arr, columns=col)

    def get_Teams_Dictionairy_For_Year(season):
        if season == 2016:
            return bbref_team_abbrev_dict_2016_to_2017
        elif 2017 <= season <= 2019:
            return bbref_team_abbrev_dict_2017_to_2019
        elif 2020 <= season <= 2021:
            return bbref_team_abbrev_dict_2020_to_2021

    this_dict = get_Teams_Dictionairy_For_Year(season)

    for team in range(0, 32):
        chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        teamname = list(this_dict.keys())[team]
        teamcode = list(this_dict.values())[team]
        found = False
        for files in os.listdir(directory):
            if str(teamname) in files:
                found = True
                break

        if found == False:
            url = 'https://www.pro-football-reference.com/teams/' + str(teamcode) + '/' + str(season) + '_roster.htm'
            driver.get(url)
            df = pd.read_html(driver.page_source)
            driver.close()
            df = cleanReturnDF(df[0])  #### if current season this is 0, else 1
            col = df.columns
            arr = df.to_numpy()
            new_arr = []
            for entry in range(0, len(arr)):
                if arr[entry][3] in ('QB', 'RB', 'WR', 'TE', 'K'):
                    new_arr.append(arr[entry])
            pd.DataFrame(new_arr, columns=col).to_csv(str(directory) + str(teamname) + str(season) + 'Roster.csv',
                                                      index=False)
            print(teamcode)


def getSimplePositionsFilesForALLSeasons():
    None


def updateGameHistoryWithSimplePlayerPositions(season):
    # puts all files into one giant player database per season
    directory = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SIMPLEPOSITIONROSTERS/' + str(season) + '/'
    roster_array = []
    col = []
    for files in os.listdir(directory):
        if 'ALL_PLAYERS' in files:
            continue
        team = str(files[0:files.index('2')])
        df = pd.read_csv(directory + files)
        df["Team"] = team
        col = df.columns
        arr = df.to_numpy()
        for entry in range(0, len(arr)):
            roster_array.append(arr[entry])
    pd.DataFrame(roster_array, columns=col).to_csv(str(directory) + '0' + str(season) + '_ALL_PLAYERS_ROSTER.csv',
                                                   index=False)

    def getPositionFromName(name, team):
        for entry in range(0, len(roster_array)):
            if str(roster_array[entry][1]) == str(name) and str(roster_array[entry][-1]) == str(team):
                return str(roster_array[entry][3])

    def getTeam(teamnames, teamabbrev):
        teams_dict = {'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL',
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
                      'Tennessee Titans': 'TEN', 'Washington Football Team': 'WAS', 'San Diego Chargers': 'SDG',
                      'Oakland Raiders': 'OAK', 'Washington Redskins': 'WAS'}
        t_keys = list(teams_dict.keys())
        t_values = list(teams_dict.values())
        index = str(teamnames).index('V')
        if str(teamnames)[index + 1] == 'e' or str(teamnames)[index + 1] == 'i':
            index2 = str(teamnames)[index + 1:].index('V')
            index = index + index2 + 1
        team1 = str(teamnames)[index + 1:]
        if t_values[t_keys.index(team1)] == teamabbrev:
            return team1
        else:
            team2 = str(teamnames)[:index]
            return team2

    # edits all games from the season with positions
    games_directory = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/'
    for files in os.listdir(games_directory):
        df = pd.read_csv(games_directory + files)
        col = df.columns
        arr = df.to_numpy()
        for entry in range(0, len(arr)):
            teamnames = arr[entry][2]
            teamabbrev = arr[entry][3]
            this_team = getTeam(teamnames, teamabbrev)
            name = arr[entry][4]
            position = getPositionFromName(name, this_team)
            arr[entry][5] = position
        pd.DataFrame(arr, columns=col).to_csv(games_directory + files, index=False)
        print(files)


def getDepthChartPositions(season):
    directory = 'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/'
    week_counter = 0
    weekly_depth_chart_arr = []

    for file in os.listdir(directory):
        week = re.sub(r"[A-Z]|[a-z]|[.]", '', file)
        game = pd.read_csv(directory + file)
        col = game.columns
        game_arr = game.to_numpy()

        # prevent reacquiring weekly depth chart for each game
        if week != week_counter:
            week_counter = week
            df_list = []
            chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            driver.get('https://www.spotrac.com/nfl/depth-charts/' + str(season) + '/week-' + week + '/')
            df = pd.read_html(driver.page_source)
            driver.close()

            for i in range(0, len(df)):
                if df[i].columns[1] == 'Pos.':
                    df_list.append(df[i][:-1])
            weekly_depth_chart = pd.concat(df_list)
            weekly_depth_chart_arr = weekly_depth_chart.to_numpy()

        for player in range(0, len(game_arr)):
            for entry in range(0, len(weekly_depth_chart_arr)):
                name = str(weekly_depth_chart_arr[entry][0])
                if name[-2:] == 'IR':
                    name = name[:-3]
                if name.split(" ")[0] in str(game_arr[player][4]) and name.split(" ")[1] in str(game_arr[player][4]):
                    game_arr[player][-1] = weekly_depth_chart_arr[entry][1]
                    break
                else:
                    game_arr[player][-1] = ''
        print(file)
        pd.DataFrame(game_arr).to_csv(
            'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/DEPTHCHARTROSTERS' + str(season) + '/' + file,
            header=col, index=False)


##############################


##### DATA ANALYSIS #####
def create_Analysis_Table():
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
                            'Tennessee Titans': 'TEN', 'Washington Football Team': 'WAS', 'San Diego Chargers': 'SDG',
                            'Oakland Raiders': 'OAK', 'Washington Redskins': 'WAS'}
    t_keys = game_teams_dict_2020.keys()
    t_values = game_teams_dict_2020.values()

    # ASSIGN WINNER AND LOSER
    all_contest_results_array = []
    col = ['Season', 'Week', 'Game', 'Team', 'Name', 'Position', 'PassTD',
           'PassYD', 'RushTD', 'RushYD', 'Receptions', 'RecTD', 'RecYD', 'INT',
           'FUM/L', 'KRTD', 'PRTD', 'XP', 'FG0-19', 'FG20-29', 'FG30-39',
           'FG40-49', 'FG50+', '2PC', 'Fantasy Points', 'Rank', 'Winner', 'Depth_Chart_Position']
    for season in os.listdir('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/'):
        for game_file in os.listdir(
                'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(season) + '/'):
            arr = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SEASON/' + str(
                season) + '/' + game_file).to_numpy()

            def getWinner():
                index = str(arr[0][2]).index('V')
                if str(arr[0][2])[index + 1] == 'e' or str(arr[0][2])[index + 1] == 'i':
                    index2 = str(arr[0][2])[index + 1:].index('V')
                    index = index + index2 + 1

                year = str(arr[0][0])
                week = str(arr[0][1])
                team1 = str(arr[0][2])[index + 1:]
                team2 = str(arr[0][2])[:index]
                schedule = pd.read_csv('C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/SCHEDULES/' + str(
                    year) + 'NFLScheduleAndResults.csv').to_numpy()
                for entry in range(0, len(schedule)):
                    if schedule[entry][0] == week and (schedule[entry][4] == team1 or schedule[entry][4] == team2):
                        return list(t_values)[list(t_keys).index(schedule[entry][4])]

            def getDCPosition(position_dc):
                if position_dc == 'nan':
                    return ''
                position = re.sub(r"[0-9]", '', position_dc)
                return position

            winner = getWinner()
            game_list = []
            for entry in range(0, len(arr)):
                player_list = list(arr[entry])
                player_list.append(entry + 1)
                if str(arr[entry][3]) == winner:
                    player_list.append(True)
                else:
                    player_list.append(False)
                player_list.append(str(arr[entry][5]))
                game_list.append(player_list)

            for player in game_list:
                all_contest_results_array.append(player)
    pd.DataFrame(all_contest_results_array).to_csv('all_contests_array.csv', index=False, header=col)


def print_Analysis_Table():
    def print_Analysis(array, title):
        total_num_entries = 0
        for entry in range(0, len(array)):
            total_num_entries += array[entry][0]
        print(title)
        array = sorted(array, key=lambda x: x[1], reverse=True)
        for entry in range(0, len(array)):
            print(str(array[entry][1]) + '\t' + str(array[entry][0]) + '\t' + str(
                (array[entry][0] / total_num_entries) * 100) + '%')
        print('TOTAL' + '\t' + str(total_num_entries))
        print('\n')

    all_contest_results_array = pd.read_csv('all_contests_array.csv').to_numpy()

    # PRINTS MVP PER CONTEST BY SIMPLE POSITION
    MVP_Position_DC_Counter = []
    retlist = []
    for i in range(0, len(all_contest_results_array)):
        rank = all_contest_results_array[i][-3]
        position_dc = str(all_contest_results_array[i][5])
        if rank == 1:
            MVP_Position_DC_Counter.append(position_dc)
    myset = set(MVP_Position_DC_Counter)
    for i in myset:
        retlist.append([MVP_Position_DC_Counter.count(i), i])
    count = 0
    for i in range(0, len(retlist)):
        count += retlist[i][0]
    print_Analysis(retlist, "Positional MVPs")

    # PRINTS TOP 5 PER CONTEST BY SIMPLE POSITION
    UTIL_Position_DC_Counter = []
    retlist = []
    for i in range(0, len(all_contest_results_array)):
        rank = all_contest_results_array[i][-3]
        position_dc = str(all_contest_results_array[i][5])
        if rank in (1, 2, 3, 4, 5):
            # if 'K' in position_dc:
            #     print(rank, all_contest_results_array[i])
            UTIL_Position_DC_Counter.append(position_dc)
    myset = set(UTIL_Position_DC_Counter)
    for i in myset:
        retlist.append([UTIL_Position_DC_Counter.count(i), i])
    count = 0
    for i in range(0, len(retlist)):
        count += retlist[i][0]
    print_Analysis(retlist, "Positional Top 5")

    def print_simple_position_count(position):
        # counts positions per lineup
        count = [0, 0, 0, 0, 0, 0]
        top_5_list = []
        for entry in range(0, len(all_contest_results_array)):
            if all_contest_results_array[entry][-3] in (1, 2, 3, 4, 5):
                top_5_list.append(str(all_contest_results_array[entry][-1]))
                if all_contest_results_array[entry][-3] == 5:
                    this_count = top_5_list.count(str(position))
                    count[this_count] = count[this_count] + 1
                    top_5_list = []

        print(str(position) + ' Count List: ', count)

    print_simple_position_count('QB')
    print_simple_position_count('RB')
    print_simple_position_count('WR')
    print_simple_position_count('TE')
    print_simple_position_count('K')
    print('\n')

    def print_dc_position_count(position):
        # counts positions per lineup
        count = [0, 0, 0, 0, 0, 0]
        top_5_list = []
        for entry in range(0, len(all_contest_results_array)):
            if all_contest_results_array[entry][-3] in (1, 2, 3, 4, 5):
                top_5_list.append(str(all_contest_results_array[entry][5]))
                if all_contest_results_array[entry][-3] == 5:
                    this_count = top_5_list.count(str(position))
                    count[this_count] = count[this_count] + 1
                    top_5_list = []
        print(str(position) + ' Count List: ', count)

    print_dc_position_count('QB')
    print_dc_position_count('RB1')
    print_dc_position_count('RB2')
    print_dc_position_count('RB3')
    print_dc_position_count('RB4')
    print_dc_position_count('WR1')
    print_dc_position_count('WR2')
    print_dc_position_count('WR3')
    print_dc_position_count('WR4')
    print_dc_position_count('WR5')
    print_dc_position_count('TE1')
    print_dc_position_count('TE2')
    print_dc_position_count('TE3')
    print_dc_position_count('K')

    # all_list = []
    # contest_list = []
    # for entry in range(0,len(all_contest_results_array)):
    #     if all_contest_results_array[entry][-3] in (1,2,3,4,5):
    #         contest_list.append(all_contest_results_array[entry][5])
    #         if all_contest_results_array[entry][-3] == 5:
    #             all_list.append(contest_list)
    #             contest_list = []
    #
    # myset = [set(ele) for ele in all_list]
    # for i in myset:
    #     print(i)
    # for i in myset:
    #     print(list(i))
    #
    # count_list = []
    # for i in range(0,len(myset)):
    #     count_list.append(all_list.count(mylist[i]))
    #
    # retlist = []
    # for i in range(0,len(mylist)):
    #     retlist.append([mylist[i],count_list[i]])
    # retlist = sorted(retlist, key=lambda x: x[1], reverse=True)
    # pd.DataFrame(retlist).to_csv('contest_output.csv',index=False)


def top_5_pattern_counter():
    all_contest_results_array = pd.read_csv('all_contests_array.csv').to_numpy()
    # PRINTS TOP 5 PER CONTEST BY SIMPLE POSITION
    positions = []
    all = []
    for i in range(0, len(all_contest_results_array)):
        rank = all_contest_results_array[i][-3]
        position = str(all_contest_results_array[i][5])
        if rank in (1, 2, 3, 4, 5):
            positions.append(position)
            if rank == 5:
                positions.append(0)
                all.append(positions)
                positions = []

    count_all = []
    previously_used = []
    for entry in range(0, len(all)):
        if all[entry] in previously_used:
            continue
        else:
            previously_used.append(all[entry])
            e = all[entry].copy()
            count = all.count(e)
            e[-1] += count
            e.append(e.count('QB'))
            e.append(e.count('RB'))
            e.append(e.count('WR'))
            e.append(e.count('TE'))
            e.append(e.count('K'))
            e.append(e.count('nan'))
            count_all.append(e)
    count_all = sorted(count_all, key=lambda x: (x[5], x[1], x[2], x[3], x[4]), reverse=True)
    pd.DataFrame(count_all,
                 columns=['MVP', 'UTIL1', 'UTIL2', 'UTIL3', 'UTIL4', 'Lineup Frequency Count', 'QB Count', 'RB Count',
                          'WR Count', 'TE Count', 'K Count', 'nan Count']).to_csv(
        'C:/Users/samue/PycharmProjects/NFL_FanDuel_DFS/DFS/DFS_DATA/ANALYSIS/Historical_Position_Combinations_Count.csv',
        index=False)


main()
