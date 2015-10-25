file_name = 'espn-week4.csv' #str(file_name)
#print projection
#print file_name
import pandas as pd


df = pd.read_csv(file_name)
#df.head()

num_col = ['pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','punt_td','kick_td','fl','2-pt']


print df
col = 0
for col in range(0,14):
	df[num_col[col]] = df[num_col[col]].convert_objects(convert_numeric=True)
	col +=1
df.replace('NaN',0, inplace=True)

print df