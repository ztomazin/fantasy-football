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

#getting three columns
#df_qb = df_qb[['Name']]
df_rb = df_rb[['Name']]
df_wr = df_wr[['Name']]

#getting length of file
rb_num = len(df_rb)
wr_num = len(df_wr)

#dst_num = len(df_dst)
print rb_num
print wr_num
cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
cont = str(cont)
if cont == 'n':
	sys.exit(0)


#turning df into list of lists
rb = df_rb.values.tolist() 
wr = df_wr.values.tolist()

list_rb =  list(itertools.permutations(rb, 2))
list_wr =  list(itertools.permutations(wr, 3))


list_rbwr = list(itertools.permutations([list_rb,list_wr], 2))





#list_rbwr = list_rb.append(list_wr)




print list_rbwr
#print list_wr

df_rbwr = pd.DataFrame(list_rbwr)
#df_wr = pd.DataFrame(list_wr)

df_rbwr.to_csv('wrrb.csv')
#df_wr.to_csv('wr1.csv')


#[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]


