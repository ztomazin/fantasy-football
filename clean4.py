import pandas as pd
import numpy as np
import csv
from datetime import datetime

start_time = datetime.now()

score = 'fftoday'

data_set = 'aggregate-week6.csv'
csv_output = 'line-up-test.csv'
df = pd.read_csv(data_set)
#getting the data
def optimal_players(df,score,pos,mult):
	
	df = df[df.Position == pos]
	df = df.reset_index(drop=True)
	df.replace('NaN',0, inplace=True)
	#getting two columns
	df = df[['Name','Salary',score]]
	rows = len(df)
	row = 0 #starting string
	df['max_pts'] = 0.000

	for col in range(0,rows):
		salary_temp = df['Salary'][row]
		df_temp = df[df.Salary <= salary_temp]
		df_temp.sort_index(by=score, ascending=False, inplace=True) # sorting scores so we can take nth (mult-1)
		df_temp = df_temp.reset_index(drop=True) #resetting index so they are appropriately sorted
		max_pts = df_temp[score][mult-1] # taking the nth score as max points -- generally a buffer for the number of available slots inc FLEX, RB=3, WR=4, TE=2

		#max_pts = df_temp[score].max()  Using buffer rather than mult
		df['max_pts'][row] = max_pts
		row +=1
	#print df
	df['max_score'] = np.where((df[score] >= df['max_pts']) , 1, 0)
#	df['max_score'] = np.where((df[score] >= mult*df['max_pts']) , 1, 0)

	df = df[df.max_score == 1]
	return df

df_qb = optimal_players(df,score,'QB',1)
print df_qb

df_rb = optimal_players(df,score,'RB',4)
print df_rb