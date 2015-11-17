

import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
from openpyxl import load_workbook
import itertools
import easygui as eg

week = raw_input("Which week?")
week = str(week)

data_set = 'aggregate-week' +week +'.csv'
#getting the data
df = pd.read_csv(data_set)

df = FF_scoring.exclude_teams(df)
df = FF_scoring.exclude_players(df)


start_time = datetime.now()

excel_out = 'lineups-avg-range-week' + week + '.xlsx'
writer = pd.ExcelWriter(excel_out)


df_avg = FF_scoring.optimize_lineup('average',df,.95)
#df_avg.to_csv(average_csv)
df_avg.to_excel(writer,'average')
writer.save()

df_max = FF_scoring.optimize_lineup('max',df,.95)
#df_avg.to_csv(average_csv)
df_max.to_excel(writer,'max')
writer.save()

df_range = FF_scoring.optimize_lineup('range',df,.90)
#df_avg.to_csv(average_csv)
df_range.to_excel(writer,'range')
writer.save()



print datetime.now() - start_time