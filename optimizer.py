

import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
from openpyxl import load_workbook
import itertools
import easygui as eg



#week = '11'
week = raw_input("Which week?")
week = str(week)

#fd = '1'
fd = raw_input("If Fanduel type 1:")
fd = str(fd)


#spec = 'testtesttest'
spec = raw_input("Enter special string for name of output:   ")
spec = str(spec)



if fd =='1':
	#kick_sal = 5000
	kick_sal = raw_input("Enter kicker salary:   ")
	kick_sal = int(kick_sal)
	salary = 60000-kick_sal
	data_set = "weeks/week-" +week + "/aggregate-week" +week +'fd.csv'
	excel_out = "weeks/week-" +week + "/lineups-week" + week + spec +'fd.xlsx'
else:
	data_set = "weeks/week-" +week + "/aggregate-week" +week +'dk.csv'  
	excel_out = "weeks/week-" +week + "/lineups-week" + week + spec + 'dk.xlsx'
	
#getting the data
df = pd.read_csv(data_set)
df = FF_scoring.exclude_teams(df)
df = FF_scoring.exclude_players(df)

#need a list here

#score_list = ['average'] 
score_list = FF_scoring.which_scores(df)

#print score_list


#---------
#cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
#cont = str(cont)
#if cont == 'n':
#	sys.exit(0)
#---------

start_time = datetime.now()
writer = pd.ExcelWriter(excel_out)

s_n = len(score_list)
x=0

if fd =='1':
	for x in range(0,s_n):
		score = score_list[x]

		df_out = FF_scoring.optimize_lineup_fd(score,df,.95,salary)
		#csv_out = 'lineups-week' + week + score + spec + 'fd.csv'		
		#df_out.to_csv(csv_out)

		df_out.to_excel(writer,score)
		writer.save()
		print datetime.now() - start_time
else:
	for x in range(0,s_n):
		score = score_list[x]
		
		df_out = FF_scoring.optimize_lineup(score,df,.95)
#		csv_out = 'lineups-week' + week + score + spec + '.csv'		
#		df_out.to_csv(csv_out)

		df_out.to_excel(writer,score)
		writer.save()
		print datetime.now() - start_time
		x +=1



print datetime.now() - start_time