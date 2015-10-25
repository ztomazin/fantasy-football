# cleaning finalscores
import csv
import pandas as pd
import numpy as np


df = pd.read_csv('finalscore-week5-2.csv')
df = df.drop('Unnamed: 0', 1)
df = df.drop('Unnamed: 0_x', 1)
df = df.drop('Unnamed: 0_y', 1)
df = df.drop('player', 1)
df = df.drop('dk_name', 1)
#df = s1.drop(s1.columns[['Unnamed: 0_y','player','dk_name']], axis=1, inplace=True)

df.to_csv('finalscores.csv')