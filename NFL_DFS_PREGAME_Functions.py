import datetime
import fnmatch
import os

import pandas as pd
from itertools import permutations, combinations
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

file = 'DALTB.csv'

def main():
   # removeInjuries()
   createCombinations(50000)
   countPlayerAppearanceInCombinations(0,0)

def removeInjuries():
    df = pd.read_csv(file)
    column_names = getHeaders(df)
    array = df.to_numpy()

    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11]) == 'nan') and (
                array[player][5] > 3):  # removes injuries and only gets players with FPPG scores
            newarray.append(array[player])
    newarray.sort(key=lambda x: x[5], reverse=True)
    pd.DataFrame(newarray).to_csv(file[0:-4] + "_players_list.csv", index=False, header=column_names)

def createCombinations(salaryRestriction):
    array = pd.read_csv(file[0:-4] + "_players_list.csv").to_numpy()

    combos = list(permutations(array, 5))
    permutationsarr = []
    currentlineup = []
    lineupscore = 0
    salary = 0
    salaryMax = 60000

    for combination in range(0, len(combos)):
        for player in range(0, len(combos[combination])):
            if (salary + combos[combination][player][7]) <= salaryMax:
                currentlineup.append(combos[combination][player][3])  # add player to current
                salary += combos[combination][player][7]  # add salary
                if player == 0:
                    lineupscore += float(combos[combination][player][5]) * 1.5  # MVP
                else:
                    lineupscore += float(combos[combination][player][5])  # NORMAL
            else:
                break

        if len(currentlineup) == 5:
            currentlineup.append(salary)
            currentlineup.append(lineupscore)
            permutationsarr.append(currentlineup)
        currentlineup = []
        salary = 0
        lineupscore = 0




    newpermutationsarr = []  # removes every 24th entry, the number of possible ways to order the 4 UTIL players
    for i in range(0, len(permutationsarr), 24):
        if permutationsarr[i][5] >= salaryRestriction:
            newpermutationsarr.append(permutationsarr[i])
    newpermutationsarr.sort(key=lambda x: x[6], reverse=True)
    print("Total Permutations Created: " + str(len(newpermutationsarr)))

    # check for all players team same and remove them
    players = pd.read_csv(file[0:-4] + "_players_list.csv").to_numpy()

    poplist = []
    for i in range(0, len(newpermutationsarr)):
        playerteam = []
        for j in range(0, 5):
            for k in range(0, len(players)):
                if newpermutationsarr[i][j] == players[k][3]:
                    playerteam.append(players[k][9])
                    break
        if playerteam[0] == playerteam[1] == playerteam[2] == playerteam[3] == playerteam[4]:
            poplist.append(i)

    pop_counter_deduction = 0
    for i in range(0, len(poplist)):
        newpermutationsarr.pop(poplist[i]-pop_counter_deduction) #needed to remove the proper array index after previous removal of elements
        pop_counter_deduction += 1


    #save to a csv
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Salary', 'LineupScore']
    pd.DataFrame(newpermutationsarr).to_csv(file[0:-4] + "_permutations.csv", index=False, header=headers)

def countPlayerAppearanceInCombinations(player_list, combinations):
    players = pd.read_csv(file[0:-4] + "_players_list.csv").to_numpy()
    combinations = pd.read_csv(file[0:-4] + "_permutations.csv").to_numpy()
    player_counter_array = []
    headers = ['Player Name', "# of MVPs", "# of UTILs"]

    for name in range(0, len(players)):
        player_counter_array.append([players[name][3], 0, 0])

    for i in range(0, len(combinations)):
        for j in range(0, len(player_counter_array)):
            for k in range(0, 5):

                if combinations[i][k] == player_counter_array[j][0]:
                    if k == 0:
                        player_counter_array[j][1] += 1
                    else:
                        player_counter_array[j][2] += 1

    pd.DataFrame(player_counter_array).to_csv(file[0:-4] + "_distribution_player_count", index=False, header=headers)

def getHeaders(dataframe):
    col_arr = []
    for col in dataframe:
        col_arr.append(col)
    return col_arr

main()