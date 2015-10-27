import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
import sys
import itertools


score = 'fftoday'

data_set = 'aggregate-week6.csv'
csv_output = 'lu.csv'

#getting the data
df = pd.read_csv(data_set)

#df_qb = FF_scoring.optimal_players(df,score,['QB'],1)
df_rb = FF_scoring.optimal_players(df,score,['RB'],2)
df_wr = FF_scoring.optimal_players(df,score,['WR'],3)
#df_te = FF_scoring.optimal_players(df,score,['TE'],1)
#df_flex = FF_scoring.optimal_players(df,score,['RB','WR','TE'],6)


#getting three columns
#df_qb = df_qb[['Name','Salary']]
df_rb = df_rb[['Name','Salary',score]]
df_wr = df_wr[['Name','Salary',score]]
#df_te = df_te[['Name','Salary']]
#df_flex = df_flex[['Name','Salary']]

#getting length of file
#qb_num = len(df_qb)
rb_num = len(df_rb)
wr_num = len(df_wr)
#te_num = len(df_te)
#flex_num = len(df_flex)

#dst_num = len(df_dst)
#print qb_num
print rb_num
print wr_num
#print te_num
#print flex_num

cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
cont = str(cont)
if cont == 'n':
	sys.exit(0)
start_time = datetime.now()


#turning df into list of lists
#qb = df_qb.values.tolist()
rb = df_rb.values.tolist() 
wr = df_wr.values.tolist()
#te = df_te.values.tolist()
#flex = df_flex.values.tolist()


list_rb =  list(itertools.combinations(rb, 2))
list_wr =  list(itertools.combinations(wr, 3))

print list_rb
print list_rb[0][0][1] 
print list_rb[0][1][1]
z = len(list_rb[0][0])
y = len(list_rb)
x=0
for x in range(0,y):
	list_rb[x][2] = list_rb[x][0][1] + list_rb[x][1][1]
	x +=1
print list_rb



cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
cont = str(cont)
if cont == 'n':
	sys.exit(0)


list_fin = list(itertools.product(list_rb,list_wr))
#list_fin = list(itertools.product(qb,list_rb,list_wr,te,flex))

print list_fin[0][0][0]
df = pd.DataFrame(list_fin)

def clean_player(df,posx,posy,pos):
	df[pos] = 0
	n = len(df)
	x=0
	for x in range(0,n):
		df[pos][x] = df[posx][x][posy]
		x += 1
	return df


df = clean_player(df,0,0,'RB1')

#list_rbwr = list(itertools.permutations([list_rb,list_wr], 2))





#list_rbwr = list_rb.append(list_wr)




#print list_rb
#print list_wr

#df_rbwr = pd.DataFrame(list_rbwr)


#df_rbwr.to_csv('wrrb.csv')
df.to_csv('opp.csv')

print datetime.now() - start_time
#print qb_num*rb_num*(rb_num-1)/2*wr_num*(wr_num-1)*(wr_num-2)/6*te_num*flex_num
#print len(list_fin)
#[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]


