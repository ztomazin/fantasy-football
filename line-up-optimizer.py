import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 

data_set = 'aggregate-week7.csv'
#getting the data
df = pd.read_csv(data_set)

start_time = datetime.now()


df_fftoday = FF_scoring.optimize_lineup('fftoday',df)
df_nfl = FF_scoring.optimize_lineup('nfl',df)
df_cbs = FF_scoring.optimize_lineup('cbs',df)
df_fleaflicker = FF_scoring.optimize_lineup('fleaflicker',df)
df_espn = FF_scoring.optimize_lineup('espn',df)
df_fox = FF_scoring.optimize_lineup('fox',df)
df_fire = FF_scoring.optimize_lineup('fire',df)




df_fftoday.to_csv('fftoday.csv')
df_nfl.to_csv('nfl.csv')
df_cbs.to_csv('cbs.csv')
df_fleaflicker.to_csv('fleaflicker.csv')
df_espn.to_csv('espn.csv')
df_fox.to_csv('fox.csv')
df_fire.to_csv('fire.csv')

print datetime.now() - start_time