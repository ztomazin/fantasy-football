
#pass the score, the data_set or df
#def optimize_lineup(score,df):
import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 
import sys


score = 'average'

data_set = 'aggregate-week8.csv'
csv_output = score + 'fin-line-up-8-steve.csv'

#getting the data
df = pd.read_csv(data_set)

df_qb = FF_scoring.optimal_players(df,score,['QB'],1)
df_rb = FF_scoring.optimal_players(df,score,['RB'],2)
df_wr = FF_scoring.optimal_players(df,score,['WR'],3)
df_te = FF_scoring.optimal_players(df,score,['TE'],1)
df_dst = FF_scoring.optimal_players(df,score,['DST'],1)
df_flex = FF_scoring.optimal_players(df,score,['RB','WR','TE'],6)


#getting three columns
df_qb = df_qb[['Name','Salary',score]]
df_rb = df_rb[['Name','Salary',score]]
df_wr = df_wr[['Name','Salary',score]]
df_te = df_te[['Name','Salary',score]]
df_dst = df_dst[['Name','Salary',score]]
df_flex = df_flex[['Name','Salary',score]]

#getting length of file
qb_num = len(df_qb)
rb_num = len(df_rb)
wr_num = len(df_wr)
te_num = len(df_te)
dst_num = len(df_dst)
flex_num = len(df_flex)

print qb_num
print rb_num
print wr_num
print te_num
print dst_num
perms = qb_num*rb_num*(rb_num-1)/2*wr_num*(wr_num-1)*(wr_num-2)/6*te_num*flex_num*dst_num
print "Runs = " + str(perms)


cont = raw_input("Continue (y/n)?") # for ESPN, this is for the csv_output (auto-refreshes projections)
cont = str(cont)
if cont == 'n':
	sys.exit(0)


#turning df into list of lists
qb = df_qb.values.tolist() 
rb = df_rb.values.tolist()
wr = df_wr.values.tolist()
te = df_te.values.tolist()
dst = df_dst.values.tolist()
flex = df_flex.values.tolist()



#these are the column headings
lu = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
lu_headings = [['QB','QB_sal','QB_score','RB1','RB1_sal','RB1_score','RB2','RB2_sal','RB2_score','WR1','WR1_sal','WR1_score','WR2','WR2_sal','WR2_score','WR3','WR3_sal','WR3_score','TE','TE_sal','TE_score','DST','DST_sal','DST_score','FLEX','FLEX_sal','FLEX_score','salary','score']]
#lu = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
#lu_headings = [['QB','QB_sal','QB_score','RB1','RB1_sal','RB1_score','RB2','RB2_sal','RB2_score','WR1','WR1_sal','WR1_score','WR2','WR2_sal','WR2_score','WR3','WR3_sal','WR3_score','TE','TE_sal','TE_score','FLEX','FLEX_sal','FLEX_score','salary','score']]


q = 0 #for row numbers
r1 = 0 #first rb
w1 = 0 #first wr
t = 0
d = 0
l = 0
f = 0
max_score = 0
start_time = datetime.now()
for q in range(0,qb_num):
	for r1 in range(0,rb_num):
		r2 = r1 + 1 #second rb
		for r2 in range(r2,rb_num):
			for w1 in range(0,wr_num):
				w2 = w1 +1 
				for w2 in range(w2,wr_num):
					w3 = w2 +1
					for w3 in range(w3,wr_num):
						for t in range(0,te_num):
							for d in range(0,dst_num):
								for f in range(0,flex_num):
									data = [qb[q][0],qb[q][1],qb[q][2],rb[r1][0],rb[r1][1],rb[r1][2],rb[r2][0],rb[r2][1],rb[r2][2],wr[w1][0],wr[w1][1],wr[w1][2],wr[w2][0],wr[w2][1],wr[w2][2],wr[w3][0],wr[w3][1],wr[w3][2],te[t][0],te[t][1],te[t][2],dst[d][0],dst[d][1],dst[d][2],flex[f][0],flex[f][1],flex[f][2],0,0]
									total_salary = data[1] + data[4] + data[7] + data[10] + data[13] + data[16] + data[19] + data[22] + data[25]
									total_score = data[2] + data[5] + data[8] + data[11] + data[14] + data[17] + data[20] + data[23]+ data[26]
									data[27]=total_salary
									data[28]=total_score
									if total_score >= max_score and total_salary <=50000:# and total_salary > 45500:				
										lu.append(data)
										max_score = total_score
									f +=1
									l +=1
								d +=1
							t +=1
						w3 += 1
					print l
					print datetime.now() - start_time
					w2 +=1
				w1 +=1
			r2+=1
		r1 +=1
	q +=1

df = pd.DataFrame(lu, columns=lu_headings[0])
df['Unique_flex'] = np.where((df['FLEX']==df['RB1']) |(df['FLEX']==df['RB2']) |(df['FLEX']==df['WR1']) | (df['FLEX']==df['WR2']) | (df['FLEX']==df['WR3']) | (df['FLEX']==df['TE']), 0, 1)
df = df[df.Unique_flex == 1]

df.to_csv(csv_output)


print len(lu)
print l
print datetime.now() - start_time



