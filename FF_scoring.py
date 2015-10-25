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
