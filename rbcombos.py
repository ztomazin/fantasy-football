


import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
import sys
import itertools

score = 'average'

data_set = 'aggregate-week8.csv'
csv_output = 'lu.csv'

#getting the data
df = pd.read_csv(data_set)

#qbs
#df_qb = FF_scoring.optimal_players(df,score,['QB'],1)
#df_qb = df_qb[['Name','Salary',score]]
#qb_num = len(df_qb)
#qb = df_qb.values.tolist()

#rbs

df_rb = FF_scoring.segment_df(df,score,['RB'])
df_rb = FF_scoring.optimal_players(df_rb,score,2)
df_rb = df_rb[['Name','Salary',score]]


#not unique --doing the combos (use 2 as parameter)
rb_num = len(df_rb)
rb = df_rb.values.tolist() 
tup_rb =  itertools.combinations(rb, 2)
list_rb = map(list,tup_rb)
df_rb = pd.DataFrame(list_rb)

#unique to Rb/WR -- extending list
df_rb['RB'] = df_rb[0] + df_rb[1] 
df_rb = df_rb[['RB']]

#flatten list
rb = df_rb.values.tolist()
rb = list(itertools.chain(*rb))

#print rb
#adding salaries together

# adding salaries and points
r = len(rb)
x=0
for x in range(0,r):
	sal = [rb[x][1] +rb[x][4]]
	pts = [rb[x][2] +rb[x][5]]
	rb[x] = rb[x] +sal +pts
	x +=1

#shortening list
df_rb = pd.DataFrame(rb)
df_rb = df_rb[[0,3,6,7]]
df_rb.columns = ['RB1','RB2','Salary',score]

df = df_rb #modify for below script

#beginning optimal players
#def optimal_players(df,score,pos_list,mult):
#import pandas as pd
#import numpy as np
#df = df[df.Position.isin(pos_list)]
#df = df.reset_index(drop=True)
#df.replace('NaN',0, inplace=True)
#getting two columns
#df = df[['Name','Salary',score]]

print len(df)


df_rb = FF_scoring.optimal_players(df,score,1)


#		mult = 1
#		rows = len(df)
#		print rows
#		row = 0 #starting string
#		df['max_pts'] = 0.000
#
#		for col in range(0,rows):
#			salary_temp = df['Salary'][row]
#			df_temp = df[df.Salary <= salary_temp] #take all players with salaries less than current player's salary
#			df_temp.sort_index(by=score, ascending=False, inplace=True) # sorting scores so we can take nth (mult-1)
#			df_temp = df_temp.reset_index(drop=True) #resetting index so they are appropriately sorted
#			max_pts = df_temp[score][mult-1] # taking the nth score as max points -- generally a buffer for the number of available slots inc FLEX, RB=3, WR=4, TE=2
#			df['max_pts'][row] = max_pts  #finding the highest points at or below that salary --
#			row +=1
#		#print df
#		df['max_score'] = np.where((df[score] >= df['max_pts']) , 1, 0)  #giving a binary "1" to folks who are at least as "efficient" as those with lower salaries
#		#	df['max_score'] = np.where((df[score] >= mult*df['max_pts']) , 1, 0)
#
#		df = df[df.max_score == 1]
#		#return df

#end optimal players

print len(df_rb)

df.to_csv('combo2.csv')

#print rb


