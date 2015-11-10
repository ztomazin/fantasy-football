
#def optimize_rb_wr(score,df,sal):

import pandas as pd
import numpy as np
import FF_scoring 
import itertools

score = 'average'

data_set = 'aggregate-week8.csv'
csv_output = 'lu.csv'

#getting the data
df = pd.read_csv(data_set)


df_wr = FF_scoring.segment_df(df,score,['WR'])

df_wr = FF_scoring.optimal_players(df_wr,score,3)
df_wr = df_wr[['Name','Salary',score]]


wr_num = len(df_wr)
wr = df_wr.values.tolist() 
tup_wr =  itertools.combinations(wr, 3)
list_wr = map(list,tup_wr)
df_wr = pd.DataFrame(list_wr)

df_wr['WR'] = df_wr[0] + df_wr[1] + df_wr[2] 
df_wr = df_wr[['WR']]

wr = df_wr.values.tolist()
wr = list(itertools.chain(*wr))


r = len(wr)
#print rb
#adding salaries together
x=0
for x in range(0,r):
	sal = [wr[x][1] +wr[x][4]+wr[x][7]]
	pts = [wr[x][2] +wr[x][5]+wr[x][8]]
	wr[x] = wr[x] +sal +pts
	x +=1

df_wr = pd.DataFrame(wr)
df_wr = df_wr[[0,3,6,9,10]]
df_wr.columns = ['WR1','WR2','WR3','Salary',score]

df = df_wr #modify for below script

#beginning optimal players
#def optimal_players(df,score,pos_list,mult):



#def optimal_players(df,score,pos_list,mult): use above DF

mult = 1
rows = len(df)
print rows
row = 0 #starting string
df['max_pts'] = 0.000

for col in range(0,rows):
	salary_temp = df['Salary'][row]
	df_temp = df[df.Salary <= salary_temp] #take all players with salaries less than current player's salary
	df_temp.sort_values(by=score, ascending=False, inplace=True) # sorting scores so we can take nth (mult-1)
	df_temp = df_temp.reset_index(drop=True) #resetting index so they are appropriately sorted
	max_pts = df_temp[score][mult-1] # taking the nth score as max points -- generally a buffer for the number of available slots inc FLEX, RB=3, WR=4, TE=2
	df['max_pts'][row] = max_pts  #finding the highest points at or below that salary --
	row +=1
#print df
df['max_score'] = np.where((df[score] >= df['max_pts']) , 1, 0)  #giving a binary "1" to folks who are at least as "efficient" as those with lower salaries
#	df['max_score'] = np.where((df[score] >= mult*df['max_pts']) , 1, 0)

df = df[df.max_score == 1]
#return df

#end optimal players

print len(df)

df.to_csv('combo3.csv')

#print rb
#wrcombos.py:66: FutureWarning: by argument to sort_index is deprecated, pls use .sort_values(by=...)

