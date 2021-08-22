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
    array = pd.read_csv(file)
    column_names = getColumns(array)
    array = array.to_numpy()

    newarray = []
    for player in range(0, len(array)):
        if (str(array[player][11])=='nan') and (array[player][5]>3 or str(array[player][5])=='nan'): #removes injuries
            newarray.append(array[player])
    newarray.sort(key=lambda x: x[5], reverse=True)
    pd.DataFrame(newarray).to_csv(file[0:-4] + "_players_list.csv", index=False, header=column_names)


def createCombinationsFromCSV():
    array = pd.read_csv(file + "_players_list.csv").to_numpy()
    newarray = []

    combos = list(permutations(newarray, 5))
    permutationsarr = []
    currentlineup = []
    lineupscore = 0
    salary = 0
    salaryMax = 35000

    for combination in range(0, len(combos)):
        for player in range(0, len(combos[combination])):
            if (salary + combos[combination][player][7]) <= salaryMax:
                currentlineup.append(combos[combination][player][3])  # add player to current
                salary += combos[combination][player][7]  # add salary
                if player == 0:
                    lineupscore += float(combos[combination][player][5]) * 2  # MVP
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

    permutationsarr.sort(key=lambda x: x[6], reverse=True)

    newpermutationsarr = []  # removes every 24th entry, the 4
    for i in range(24, len(permutationsarr) + 24):
        if i % 24 == 0 and permutationsarr[i - 24][5] >= 32000:  # every sixth and lineup cost above 30000
            newpermutationsarr.append(permutationsarr[i - 24])

    # check for all players team same and remove them
    players = pd.read_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_reduced_players_list.csv").to_numpy()
    # print(len(newpermutationsarr))
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
        playerteam = []

    pop_counter_deduction = 0
    for i in range(0, len(poplist)):
        newpermutationsarr.pop(poplist[i]-pop_counter_deduction) #needed to remove the proper array index after previous removal of elements
        pop_counter_deduction += 1
    # print(len(newpermutationsarr))
    # print(len(poplist))

    #save to a csv
    headers = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Salary', 'LineupScore']
    pd.DataFrame(newpermutationsarr).to_csv("ContestsOutput/" + file[21:] + "_BEFORE_GAME_lineup_permutations.csv",index=False, header=headers)  # THIS IS FOR PERMUTATION TESTING


def getColumns(dataframe):
    col_arr = []
    for col in dataframe:
        print(col)
        col_arr.append(col)
    return col_arr

main()