#http://games.espn.go.com/ffl/leaders?&startIndex=0&scoringPeriodId=9&seasonId=2015

import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np


week = raw_input("Which week?") # for ESPN, this is for the csv_output (auto-refreshes projections)
week = str(week)

excel_doc = 'Week ' + week +'.xlsx' 
csv_output = "finalscore-week" + week + ".csv"
#csv_output_2 = "finalscore-week" + week + "-2.csv"
dk_file = 'DKweek'+week+'salaries.xlsx' #change every week
agg = "aggregate-week" + week + ".csv"

url_format = "http://games.espn.go.com/ffl/leaders?&startIndex={index}&scoringPeriodId={week}&seasonId=2015"
page_num = 1

data = [['player','opp','status','comp/att','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds','rec','rec_yards','rec_tds','targets','2-pt','fl','def_td','fan_pts','punt_td','kick_td']]


for page_num in range(1,20):
	page_mult = (page_num-1) * 50
	next = str(page_mult)
	url = url_format.format(index=page_mult,week=week)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'playerTableTable tableBody'})
	table_body = table.find('tbody')

	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    cols = [ele.encode('ascii','ignore') for ele in cols]
	    data.append([ele for ele in cols if ele]) # Get rid of empty values
	b = open(csv_output, 'w')
	a = csv.writer(b)
	a.writerows(data)
	b.close()
	page_num = page_num+1
#print data


final = FF_scoring.scoring('final',csv_output)
df_fin = pd.DataFrame(final)

# cleaning the names for easier fuzzy logic
i = 0
row_num = len(df_fin)

for i in range(0,row_num):
	f1 = df_fin['player'][i].split(',') # split() only once
	new_player = f1[0]
	df_fin['player'][i] = new_player
	i = i+ 1


df_fin_2 = df_fin[(df_fin['final'] > 0)]  # cleaning low scores
df_fin_2.to_csv(csv_output)

df = FF_scoring.get_player(csv_output,dk_file,86)


#accumulating with aggregate scores
df_agg = pd.read_csv(agg)
df = pd.merge(df_agg, df, how='left', left_on='Name', right_on = 'dk_name')

df = df[['Name','Position','Salary','GameInfo','AvgPointsPerGame','teamAbbrev','fftoday','nfl','cbs','fleaflicker','espn','fox','fire','average','max','min','range','rel_range','final']]


#df = df.drop('Unnamed: 0_x', 1)
#df = df.drop('Unnamed: 0_y', 1)
#df = df.drop('player', 1)
#df = df.drop('dk_name', 1)
#df = s1.drop(s1.columns[['Unnamed: 0_y','player','dk_name']], axis=1, inplace=True)

df.to_csv(csv_output)
#this fucking works
