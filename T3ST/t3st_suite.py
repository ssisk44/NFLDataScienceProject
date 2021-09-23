import math
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

chromedriver = "C:/Users/samue/OneDrive/Documents/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('https://www.pro-football-reference.com/boxscores/201911030sea.htm')
df = pd.read_html(driver.page_source)
driver.close()





