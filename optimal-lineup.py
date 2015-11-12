

import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
from openpyxl import load_workbook
import itertools

week = raw_input("Which week?")
week = str(week)

data_set = 'finalscore-week' +week +'.csv'
excel_out = 'lineups-week' + week + '.xlsx'

book = load_workbook(excel_out)
writer = pd.ExcelWriter(excel_out)



writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#data_filtered.to_excel(writer, "Main", cols=['Diff1', 'Diff2'])
#writer.save()


#getting the data
df = pd.read_csv(data_set)

#start_time = datetime.now()

#fftoday_csv = 'fftoday-lineup-' + week + '.csv'
#nfl_csv = 'nfl-lineup-' + week + '.csv'
#cbs_csv = 'cbs-lineup-' + week + '.csv'
#fleaflicker_csv = 'fleaflicker-lineup-' + week + '.csv'
#espn_csv = 'espn-lineup-' + week + '.csv'
#fox_csv = 'fox-lineup-' + week + '.csv'
#fire_csv = 'fire-lineup-' + week + '.csv'
final_csv = 'final-lineup-' + week + '.csv'

#excel_out = 'lineups-week' + week + '-1.xlsx'
#writer = pd.ExcelWriter(excel_out)

df_final = FF_scoring.optimize_lineup('final',df,.90)
#df_fftoday.to_csv(fftoday_csv)
df_final.to_excel(writer,'optimal')
writer.save()

#---------------------

#df_final = FF_scoring.optimize_lineup('final',df)




#df_final.to_csv(final_csv)


#print datetime.now() - start_time

