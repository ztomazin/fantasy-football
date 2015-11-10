
import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
import sys
import itertools

start_time = datetime.now()

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

df_rb = FF_scoring.optimal_players(df,score,['RB'],2)
df_rb = df_rb[['Name','Salary',score]]
rb_num = len(df_rb)
rb = df_rb.values.tolist() 
tup_rb =  itertools.combinations(rb, 2)
list_rb = map(list,tup_rb)
df_rb = pd.DataFrame(list_rb)
df_rb['RB'] = df_rb[0] + df_rb[1] 
df_rb = df_rb[['RB']]

rb = df_rb.values.tolist()
rb = list(itertools.chain(*rb))
r = len(rb)
#print rb
#adding salaries together
x=0
for x in range(0,r):
	sal = [rb[x][1] +rb[x][4]]
	pts = [rb[x][2] +rb[x][5]]
	rb[x] = rb[x] +sal +pts
	x +=1

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
mult = 1
rows = len(df)
print rows
row = 0 #starting string
df['max_pts'] = 0.000

for col in range(0,rows):
	salary_temp = df['Salary'][row]
	df_temp = df[df.Salary <= salary_temp] #take all players with salaries less than current player's salary
	df_temp.sort_index(by=score, ascending=False, inplace=True) # sorting scores so we can take nth (mult-1)
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

df.to_csv('combo2.csv')

#print rb





cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
cont = str(cont)
if cont == 'n':
	sys.exit(0)


#wrs
#df_wr = FF_scoring.optimal_players(df,score,['WR'],3)
#df_wr = df_wr[['Name','Salary',score]]
#wr_num = len(df_wr)
#wr = df_wr.values.tolist()
#tup_wr =  itertools.combinations(wr, 3)
#list_wr = map(list,tup_wr)
#df_wr = pd.DataFrame(list_wr)
#df_wr['WR'] = df_wr[0] + df_wr[1] + df_wr[2]
#df_wr = df_wr[['WR']]
#wr = df_wr.values.tolist()
#wr = list(itertools.chain(*wr))




#df_te = FF_scoring.optimal_players(df,score,['TE'],1)
#df_flex = FF_scoring.optimal_players(df,score,['RB','WR','TE'],6)


#getting three columns
#df_te = df_te[['Name','Salary',score]]
#df_flex = df_flex[['Name','Salary',score]]

#getting length of file
#te_num = len(df_te)
#flex_num = len(df_flex)

#dst_num = len(df_dst)
#print qb_num
print rb_num
#print wr_num
#print te_num
#print flex_num


#turning df into list of lists
#te = df_te.values.tolist()
#flex = df_flex.values.tolist()


tup_fin = itertools.product(rb,wr,qb)
list_fin = map(list,tup_fin)

df = pd.DataFrame(list_fin)
print len(df)
df = df.head(10)
df['XX'] = df[0] + df[1] +df[2] #+df[3] #+df[4]
df.to_csv('combo1.csv')

df = df[['XX']]

xx = df.values.tolist()
xx = list(itertools.chain(*xx))
df = pd.DataFrame(xx)
df[18] = 0
df[19] = 0


xx = df.values.tolist()
y = len(xx)
x=0
for x in range(0,y):
	sal = xx[x][1] +xx[x][4]+xx[x][7]+xx[x][10]+xx[x][13]+xx[x][16]
	pts = xx[x][2] +xx[x][5]+xx[x][8]+xx[x][11]+xx[x][14]+xx[x][17]
	xx[x][18] = sal
	xx[x][19] = pts
	x +=1
df = pd.DataFrame(xx)
df.columns = ['a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']
#print df#list(df.columns.values)
print len(df)
df = df[df.s < 43000]
print len(df)


#df.to_csv('combo2.csv')

#print xx[0][0]
#print xx[0][1]
#print xx[0][2]
print datetime.now() - start_time



