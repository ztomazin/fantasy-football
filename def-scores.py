
import FF_scoring 
import pandas as pd
import numpy as np

week = raw_input("Which week?") # for ESPN, this is for the csv_output (auto-refreshes projections)
week = str(week)

dk_file = "DKweek" +week +"salaries.xlsx"

csv_output = 'def-week' +week + ".csv"
csv_output_2 = 'def-week' +week + "-2.csv"
data_set = 'espn-week' +week +".csv"

#data_set = 'espn-week' +week +'.csv'
#getting the data

#df_dk.to_excel(dk_file)

df = pd.read_csv(data_set)

df_1 = df[['player','fan_pts']]

pos = "D/STD/ST"
df_1['pos']=0
row_num = len(df_1)
i=0
for i in range(0,row_num):
	#cleaning favorite from "At" and "(London)"
	f1 = df_1['player'][i].split(' ')
	f = len(f1)-1
	f2 = f1[f]
	f3 = f1[0]
	df_1['pos'][i] = f2
	df_1['player'][i] = f3
	i +=1

df_1['Def'] = np.where(df_1['pos']==pos,1,0)
df_1 = df_1[df_1.Def == 1]
df = df_1[['player','fan_pts']]

df.to_csv(csv_output)
df = FF_scoring.get_player(csv_output,dk_file,50)
df['fftoday']=df['fan_pts']
df['nfl']=df['fan_pts']
df['cbs']=df['fan_pts']
df['fleaflicker']=df['fan_pts']
df['espn']=df['fan_pts']
df['fox']=df['fan_pts']
df['fire'] =df['fan_pts']

df['Name'] =df['dk_name']


df.to_csv(csv_output_2)




