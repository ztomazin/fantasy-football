
import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
from openpyxl import load_workbook
import itertools

week = raw_input("Which week?")
week = str(week)

data_set = 'aggregate-week' +week +'.csv'
#getting the data
df = pd.read_csv(data_set)

start_time = datetime.now()

#fftoday_csv = 'fftoday-lineup-' + week + '.csv'
#nfl_csv = 'nfl-lineup-' + week + '.csv'
#cbs_csv = 'cbs-lineup-' + week + '.csv'
#fleaflicker_csv = 'fleaflicker-lineup-' + week + '.csv'
#espn_csv = 'espn-lineup-' + week + '.csv'
#fox_csv = 'fox-lineup-' + week + '.csv'
#fire_csv = 'fire-lineup-' + week + '.csv'
#average_csv = 'avg-lineup-' + week + '.csv'

excel_out = 'lineups-week' + week + '.xlsx'
writer = pd.ExcelWriter(excel_out)

df_fftoday = FF_scoring.optimize_lineup('fftoday',df)
#df_fftoday.to_csv(fftoday_csv)
df_fftoday.to_excel(writer,'fftoday')
writer.save()

df_nfl = FF_scoring.optimize_lineup('nfl',df)
#df_nfl.to_csv(nfl_csv)
df_nfl.to_excel(writer,'nfl')
writer.save()


df_cbs = FF_scoring.optimize_lineup('cbs',df)
#df_cbs.to_csv(cbs_csv)
df_cbs.to_excel(writer,'cbs')
writer.save()


df_fleaflicker = FF_scoring.optimize_lineup('fleaflicker',df)
#df_fleaflicker.to_csv(fleaflicker_csv)
df_fleaflicker.to_excel(writer,'fleaflicker')
writer.save()


df_espn = FF_scoring.optimize_lineup('espn',df)
#df_espn.to_csv(espn_csv)
df_espn.to_excel(writer,'espn')
writer.save()


df_fox = FF_scoring.optimize_lineup('fox',df)
#df_fox.to_csv(fox_csv)
df_fox.to_excel(writer,'fox')
writer.save()

df_fire = FF_scoring.optimize_lineup('fire',df)
#df_fire.to_csv(fire_csv)
df_fire.to_excel(writer,'fire')
writer.save()

df_avg = FF_scoring.optimize_lineup('average',df)
#df_avg.to_csv(average_csv)
df_avg.to_excel(writer,'average')
writer.save()

df_avg = FF_scoring.optimize_lineup('max',df)
#df_avg.to_csv(average_csv)
df_avg.to_excel(writer,'max')
writer.save()




print datetime.now() - start_time