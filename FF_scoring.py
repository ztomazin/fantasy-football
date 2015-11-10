#this is my module for fantasy football



def clean(file_name):
	#file_name = 'espn-week4.csv' #str(file_name)
	#print projection
	#print file_name
	import pandas as pd


	df = pd.read_csv(file_name)
	#df.head()

	num_col = ['pass_yards','pass_tds','int','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','punt_td','kick_td','fl','2-pt']


	print df
	col = 0
	for col in range(0,13):
		df[num_col[col]] = df[num_col[col]].convert_objects(convert_numeric=True)
		col +=1
	df.replace('NaN',0, inplace=True)
	return df

def def_clean(df):
	import pandas as pd
	import numpy as np

	#df = pd.read_csv(file_name)
	#df.head()
	num_col = ['line','total']
	print df
	col = 0
	for col in range(0,2):
		df[num_col[col]] = df[num_col[col]].convert_objects(convert_numeric=True)
		col +=1
	df.replace('NaN',0, inplace=True)
	return df


def scoring(site,file_name):
	import pandas as pd
	import numpy as np

	df = pd.read_csv(file_name)
	
	num_col = ['pass_yards','pass_tds','int','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','punt_td','kick_td','fl','2-pt']
	col = 0 #starting string
	for col in range(0,13):
		df[num_col[col]] = df[num_col[col]].convert_objects(convert_numeric=True)
		col +=1
	df.replace('NaN',0, inplace=True)
	
	
	df["bonus"] = np.where(df["pass_yards"]>=300,3,0)
	df["bonus"] = np.where(df["rush_yards"]>=100,3,0) +df["bonus"]
	df["bonus"] = np.where(df["rec_yards"]>=100,3,0) +df["bonus"]


	df[site] = df["bonus"] + df["pass_yards"]*.04 + df["pass_tds"]*4 - df["int"] + df["rush_yards"]*.1 + df["rush_tds"]*6 + df["rec"] + df["rec_yards"]*.1 + df["rec_tds"]*6 + df["punt_td"]*6 + df["kick_td"]*6 - df["fl"] + df["2-pt"]*2

	df_final = df[["player",site]]
	return df_final


#this is to score defense and not done, yet
def def_scoring(df):
	import pandas as pd
	import numpy as np
	
	df['bonus'] = np.where(df['pts_against']==0,10,0)
	df['bonus'] = np.where(df['pts_against']>0,7,df['bonus'])
	df['bonus'] = np.where(df['pts_against']>6,4,df['bonus'])
	df['bonus'] = np.where(df['pts_against']>13,1,df['bonus'])
	df['bonus'] = np.where(df['pts_against']>20,0,df['bonus'])
	df['bonus'] = np.where(df['pts_against']>27,-1,df['bonus'])
	df['bonus'] = np.where(df['pts_against']>34,-4,df['bonus'])
	#df["bonus"] = np.where(df["rec_yards"]>=100,3,0) +df["bonus"]


	df['def_pts'] = df['bonus']

#	df["bonus"] + df["pass_yards"]*.04 + df["pass_tds"]*4 - df["int"] + df["rush_yards"]*.1 + df["rush_tds"]*6 + df["rec"] + df["rec_yards"]*.1 + df["rec_tds"]*6 + df["punt_td"]*6 + df["kick_td"]*6 - df["fl"] + df["2-pt"]*2

	df_final = df[['player','pts_against','def_pts']]
	return df_final

	#df.head()

def get_player(file_name,dk_file,score_cutoff):
	import pandas as pd
	import numpy as np
	from fuzzywuzzy import fuzz
	from fuzzywuzzy import process
	dk = dk_file
	df = pd.read_csv(file_name)
	df_dk = pd.read_excel(dk)
	df['dk_name'] = 'NaN'
	df_choices = df_dk['Name']
	rows = len(df['player'])
	i =0
	for i in range(0,rows):
	  	f1 = df['player'][i]
	  	f1_out = process.extractOne(f1,choices=df_choices,score_cutoff=score_cutoff)
	  	print f1_out
	  	dk_name = 'NaN'
	  	if f1_out:
	  		dk_name = f1_out[0]
	  	df['dk_name'][i] = dk_name
	  	i += 1
	return df

def segment_df(df,score,pos_list):
	import pandas as pd
	import numpy as np
	df = df[df.Position.isin(pos_list)]
	df = df.reset_index(drop=True)
	df.replace('NaN',0, inplace=True)
	df = df[['Name','Salary',score]]
	return df 


def optimal_players(df,score,mult):
	import pandas as pd
	import numpy as np
	#df = df[df.Position.isin(pos_list)]
	#df = df.reset_index(drop=True)
	#df.replace('NaN',0, inplace=True)
	#getting two columns
	#df = df[['Name','Salary',score]]

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


def optimize_lineup(score,df): 
	import pandas as pd
	import numpy as np
	import csv
	from datetime import datetime
	import FF_scoring 
	import itertools
	start_time = datetime.now()

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

	return df
