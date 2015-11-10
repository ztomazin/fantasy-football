#sal here means what I want to max after defense
import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
import itertools
start_time = datetime.now()
#def optimize_lineup(score,df,sal):
score = 'range'

data_set = 'aggregate-week9.csv'
#data_set = 'aggregate-week' +week +'.csv'
df = pd.read_csv(data_set)
#sal = 47000

df_qb = FF_scoring.segment_df(df,score,['QB'])
df_rb = FF_scoring.segment_df(df,score,['RB'])
df_wr = FF_scoring.segment_df(df,score,['WR'])
df_te = FF_scoring.segment_df(df,score,['TE'])
df_dst = FF_scoring.segment_df(df,score,['DST'])
df_flex = FF_scoring.segment_df(df,score,['RB','WR','TE'])


df_qb = FF_scoring.optimal_players(df_qb,score,1)
df_rb = FF_scoring.optimal_players(df_rb,score,2)
df_wr = FF_scoring.optimal_players(df_wr,score,3)
df_te = FF_scoring.optimal_players(df_te,score,1)
df_dst = FF_scoring.optimal_players(df_dst,score,1)
df_flex = FF_scoring.optimal_players(df_flex,score,7)


#getting three columns
df_qb = df_qb[['Name','Salary',score]]
df_rb = df_rb[['Name','Salary',score]]
df_wr = df_wr[['Name','Salary',score]]
df_te = df_te[['Name','Salary',score]]
df_dst = df_dst[['Name','Salary',score]]
df_flex = df_flex[['Name','Salary',score]]

#flattening RBs
print datetime.now() - start_time

#doing the combos (use 2 as parameter)
rb_num = len(df_rb)  #i can probably get rid of this
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

df_rb = FF_scoring.optimal_players(df_rb,score,1)

print datetime.now() - start_time

#-----------------------------------------------
#flattening WRs

#doing the combos (use 2 as parameter)
wr_num = len(df_wr)  #i can probably get rid of this
wr = df_wr.values.tolist() 
tup_wr =  itertools.combinations(wr, 3)
list_wr = map(list,tup_wr)
df_wr = pd.DataFrame(list_wr)
#unique to Rb/WR -- extending list
df_wr['WR'] = df_wr[0] + df_wr[1] + df_wr[2] 
df_wr = df_wr[['WR']]
#flatten list
wr = df_wr.values.tolist()
wr = list(itertools.chain(*wr))

# adding salaries and points
r = len(wr)
x=0
for x in range(0,r):
	sal = [wr[x][1] +wr[x][4]+wr[x][7]]
	pts = [wr[x][2] +wr[x][5]+wr[x][8]]
	wr[x] = wr[x] +sal +pts
	x +=1

#shortening list
df_wr = pd.DataFrame(wr)
df_wr = df_wr[[0,3,6,9,10]]
df_wr.columns = ['WR1','WR2','WR3','Salary',score]

df_wr = FF_scoring.optimal_players(df_wr,score,1)

print datetime.now() - start_time
#--------------------------------------------------

#getting length of file
qb_num = len(df_qb)
rb_num = len(df_rb)
wr_num = len(df_wr)
te_num = len(df_te)
dst_num = len(df_dst)
flex_num = len(df_flex)

#df_qb.to_csv('comboqb.csv')
#df_rb.to_csv('comborb.csv')
#df_wr.to_csv('combowr.csv')
#df_te.to_csv('combote.csv')

#turning df into list of lists
qb = df_qb.values.tolist() 
rb = df_rb.values.tolist()
wr = df_wr.values.tolist()
te = df_te.values.tolist()
dst = df_dst.values.tolist()
flex = df_flex.values.tolist()

#these are the column headings
lu = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
lu_headings = [['QB','QB_sal','QB_score','RB1','RB2','RB_sal','RB_score','WR1','WR2','WR3','WR_sal','WR_score','TE','TE_sal','TE_score','DST','DST_sal','DST_score','FLEX','FLEX_sal','FLEX_score','salary','score']]

q = 0 #for row numbers
r1 = 0 #first rb
w1 = 0 #first wr
t = 0
d = 0
l = 0
f = 0
max_score = 0
max_sal = 50000 # an input for the function

for q in range(0,qb_num):
	for r1 in range(0,rb_num):
#		r2 = r1 + 1 #second rb
#		for r2 in range(r2,rb_num):
		for w1 in range(0,wr_num):
#			w2 = w1 +1 
#		for w2 in range(w2,wr_num):
#			w3 = w2 +1
#		for w3 in range(w3,wr_num):
			for t in range(0,te_num):
				for d in range(0,dst_num):
					for f in range(0,flex_num):
						data = [qb[q][0],qb[q][1],qb[q][2],rb[r1][0],rb[r1][1],rb[r1][2],rb[r1][3],wr[w1][0],wr[w1][1],wr[w1][2],wr[w1][3],wr[w1][4],te[t][0],te[t][1],te[t][2],dst[d][0],dst[d][1],dst[d][2],flex[f][0],flex[f][1],flex[f][2],0,0]
						total_salary = data[1] + data[5] + data[10] + data[13] + data[16] + data[19]
						total_score = data[2] + data[6] + data[11] + data[14] + data[17] + data[20]
						data[21]=total_salary
						data[22]=total_score
						if total_score >= .97* max_score and total_salary <= max_sal:			
							lu.append(data)
							if total_score > max_score:
								max_score = total_score
						f +=1
						l +=1
					d +=1
				t +=1
#			w3 += 1
			print l
			print datetime.now() - start_time
#			w2 +=1
			w1 +=1
#			r2+=1
		r1 +=1
	q +=1

df = pd.DataFrame(lu, columns=lu_headings[0])
df['Unique_flex'] = np.where((df['FLEX']==df['RB1']) |(df['FLEX']==df['RB2']) |(df['FLEX']==df['WR1']) | (df['FLEX']==df['WR2']) | (df['FLEX']==df['WR3']) | (df['FLEX']==df['TE']), 0, 1)
df = df[df.Unique_flex == 1]

print datetime.now() - start_time
df.to_csv('combo-range.csv')

#return df
