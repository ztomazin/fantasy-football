
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


team_list_1 = ['Atl','Buf','Car','Chi','Cin']
team_list_2 = ['Atl','Buf']

print len(df)
df_in = df[df.teamAbbrev.isin(team_list_1)]
print len(df_in)

df_out = df_in[~df_in.teamAbbrev.isin(team_list_2)]
print len(df_out)


#excel_out = 'lineups-week' + week + '.xlsx'
#writer = pd.ExcelWriter(excel_out)

#df_fftoday = FF_scoring.optimize_lineup('fftoday',df)
#df_fftoday.to_excel(writer,'fftoday')
#writer.save()

#df_nfl = FF_scoring.optimize_lineup('nfl',df)
#df_nfl.to_excel(writer,'nfl')
#writer.save()


#df_cbs = FF_scoring.optimize_lineup('cbs',df)
#df_cbs.to_excel(writer,'cbs')
#writer.save()


#df_fleaflicker = FF_scoring.optimize_lineup('fleaflicker',df)
#df_fleaflicker.to_excel(writer,'fleaflicker')
#writer.save()


#df_espn = FF_scoring.optimize_lineup('espn',df)
#df_espn.to_excel(writer,'espn')
#writer.save()


#df_fox = FF_scoring.optimize_lineup('fox',df)
#df_fox.to_excel(writer,'fox')
#writer.save()

#df_fire = FF_scoring.optimize_lineup('fire',df)
#df_fire.to_excel(writer,'fire')
#writer.save()

#df_avg = FF_scoring.optimize_lineup('average',df)
#df_avg.to_excel(writer,'average')
#writer.save()

#df_avg = FF_scoring.optimize_lineup('max',df)
#df_avg.to_excel(writer,'max')
#writer.save()




print datetime.now() - start_time