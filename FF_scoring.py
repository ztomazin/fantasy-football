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

	


def scoring(site,file_name):
	#projection = raw_input("Which site?")
	#projection = str(projection)
	#file_name = raw_input("Which file?") # for ESPN, this is for the csv_output (auto-refreshes projections)
	#file_name = str(file_name)
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
def def_scoring(site,file_name):
	#projection = raw_input("Which site?")
	#projection = str(projection)
	#file_name = raw_input("Which file?") # for ESPN, this is for the csv_output (auto-refreshes projections)
	#file_name = str(file_name)
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



def optimal_players(df,score,pos_list,mult):
	import pandas as pd
	import numpy as np
	df = df[df.Position.isin(pos_list)]
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

def optimize_lineup(score,df):
	import pandas as pd
	import numpy as np
	import csv
	from datetime import datetime
	import FF_scoring 


	#score = 'fftoday'

	#data_set = 'aggregate-week7.csv'
	#csv_output = score + 'line-up.csv'

	#getting the data
	#df = pd.read_csv(data_set)

	df_qb = FF_scoring.optimal_players(df,score,['QB'],1)
	df_rb = FF_scoring.optimal_players(df,score,['RB'],2)
	df_wr = FF_scoring.optimal_players(df,score,['WR'],3)
	df_te = FF_scoring.optimal_players(df,score,['TE'],1)
	#df_dst = FF_scoring.optimal_players(df,score,['DST'],1)
	df_flex = FF_scoring.optimal_players(df,score,['RB','WR','TE'],6)


	#getting three columns
	df_qb = df_qb[['Name','Salary',score]]
	df_rb = df_rb[['Name','Salary',score]]
	df_wr = df_wr[['Name','Salary',score]]
	df_te = df_te[['Name','Salary',score]]
	#df_dst = df_dst[['Name','Salary',score]]
	df_flex = df_flex[['Name','Salary',score]]

	#getting length of file
	qb_num = len(df_qb)
	rb_num = len(df_rb)
	wr_num = len(df_wr)
	te_num = len(df_te)
	#dst_num = len(df_dst)
	flex_num = len(df_flex)

	#turning df into list of lists
	qb = df_qb.values.tolist() 
	rb = df_rb.values.tolist()
	wr = df_wr.values.tolist()
	te = df_te.values.tolist()
	#dst = df_dst.values.tolist()
	flex = df_flex.values.tolist()



	#these are the column headings
	#lu = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
	#lu_headings = [['QB','QB_sal','QB_score','RB1','RB1_sal','RB1_score','RB2','RB2_sal','RB2_score','WR1','WR1_sal','WR1_score','WR2','WR2_sal','WR2_score','WR3','WR3_sal','WR3_score','TE','TE_sal','TE_score','DST','DST_sal','DST_score','FLEX','FLEX_sal','FLEX_score','salary','score']]
	lu = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
	lu_headings = [['QB','QB_sal','QB_score','RB1','RB1_sal','RB1_score','RB2','RB2_sal','RB2_score','WR1','WR1_sal','WR1_score','WR2','WR2_sal','WR2_score','WR3','WR3_sal','WR3_score','TE','TE_sal','TE_score','FLEX','FLEX_sal','FLEX_score','salary','score']]


	q = 0 #for row numbers
	r1 = 0 #first rb
	w1 = 0 #first wr
	t = 0
	#d = 0
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
	#							for d in range(0,dst_num):
								for f in range(0,flex_num):
									data = [qb[q][0],qb[q][1],qb[q][2],rb[r1][0],rb[r1][1],rb[r1][2],rb[r2][0],rb[r2][1],rb[r2][2],wr[w1][0],wr[w1][1],wr[w1][2],wr[w2][0],wr[w2][1],wr[w2][2],wr[w3][0],wr[w3][1],wr[w3][2],te[t][0],te[t][1],te[t][2],flex[f][0],flex[f][1],flex[f][2],0,0]
									total_salary = data[1] + data[4] + data[7] + data[10] + data[13] + data[16] + data[19] + data[22]
									total_score = data[2] + data[5] + data[8] + data[11] + data[14] + data[17] + data[20] + data[23]
									data[24]=total_salary
									data[25]=total_score
									if total_score >= max_score and total_salary <=47500:# and total_salary > 45500:				
										lu.append(data)
										max_score = total_score
									f +=1
									l +=1
									#d +=1
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

	print datetime.now() - start_time
	return df



