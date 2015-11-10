
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

df_qb = FF_scoring.optimal_players(df,score,['QB'],1)
df_rb = FF_scoring.optimal_players(df,score,['RB'],2)
df_wr = FF_scoring.optimal_players(df,score,['WR'],3)
df_te = FF_scoring.optimal_players(df,score,['TE'],1)
#df_flex = FF_scoring.optimal_players(df,score,['RB','WR','TE'],6)


#getting three columns
df_qb = df_qb[['Name','Salary',score]]
df_rb = df_rb[['Name','Salary',score]]
df_wr = df_wr[['Name','Salary',score]]
#df_te = df_te[['Name','Salary',score]]
#df_flex = df_flex[['Name','Salary',score]]

#getting length of file
qb_num = len(df_qb)
rb_num = len(df_rb)
wr_num = len(df_wr)
#te_num = len(df_te)
#flex_num = len(df_flex)

#dst_num = len(df_dst)
print qb_num
print rb_num
print wr_num
#print te_num
#print flex_num

#cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
#cont = str(cont)
#if cont == 'n':
#	sys.exit(0)



#turning df into list of lists
qb = df_qb.values.tolist()
rb = df_rb.values.tolist() 
wr = df_wr.values.tolist()
#te = df_te.values.tolist()
#flex = df_flex.values.tolist()
#print rb


tup_rb =  itertools.combinations(rb, 2)
tup_wr =  itertools.combinations(wr, 3)
#print tup_rb
#list_rb =  list(itertools.combinations(rb, 2))

list_rb = map(list,tup_rb)
list_wr = map(list,tup_wr)
#print list_rb

#print list_rb
#print list_rb[0][0]
#print list_rb[0][1]

df_rb = pd.DataFrame(list_rb)
df_wr = pd.DataFrame(list_wr)

df_rb['RB'] = df_rb[0] + df_rb[1]
df_wr['WR'] = df_wr[0] + df_wr[1] + df_wr[2]

#df_rb.to_csv('combo_rb.csv')
#df_wr.to_csv('combo_wr.csv')

df_rb = df_rb[['RB']]
df_wr = df_wr[['WR']]

rb = df_rb.values.tolist()
wr = df_wr.values.tolist()

rb = list(itertools.chain(*rb))
wr = list(itertools.chain(*wr))

tup_fin = itertools.product(rb,wr,qb)
list_fin = map(list,tup_fin)

df = pd.DataFrame(list_fin)
print len(df)

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
df = df.head(10)

#df.to_csv('combo2.csv')

#print xx[0][0]
#print xx[0][1]
#print xx[0][2]
print datetime.now() - start_time



