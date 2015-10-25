

import urllib2
import urllib
import csv
from bs4 import BeautifulSoup  # latest version bs4
import json
import pandas as pd
import numpy as np
import FF_scoring 

week = raw_input("Which week?")
week = str(week)

dk_file = "DKweek" +week +"salaries.xlsx"
csv_output = "nfl-week" + week + ".csv"
csv_output_2 = "nfl-week" + week + "-2" + ".csv"
url_format = "http://fantasy.nfl.com/research/projections?offset={offset}&position=O&sort=projectedPts&statCategory=projectedStats&statSeason=2015&statType=weekProjectedStats&statWeek={week}"
data = [['player','opp','pass_yards','pass_tds','int','rush_yards','rush_tds','rec_yards','rec_tds','fum_td','2-pt','fl','fan_pts']]

#page_num = 1
for page_num in range(1,20):
	
	page_mult = (page_num - 1) * 25 + 1
	next = str(page_mult)
	url = url_format.format(week=week, offset=page_mult)
	request = urllib2.Request(url, headers={'Ajax-Request': 'researchProjections'})
	raw_json = urllib2.urlopen(request).read()
	parsed_json = json.loads(raw_json)
	html = parsed_json['content']

	soup = BeautifulSoup(html, "html.parser")
	table = soup.find('table', attrs={'class': 'tableType-player hasGroups'})
	table_body = table.find('tbody')

	rows = table_body.find_all('tr')
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele])  # Get rid of empty values
	b = open(csv_output, 'w')
	a = csv.writer(b)
	a.writerows(data),
	b.close()
	page_num =page_num+1
#print data    
df = pd.read_csv(csv_output)
df['rec']=0
df['punt_td']=0
df['kick_td']=0
#print df
df.to_csv(csv_output)
df = FF_scoring.clean(csv_output)

df.replace('-',0, inplace=True)
#print df


df['rec']=df['rec_yards']/10

df.to_csv(csv_output)
#print df 
df = FF_scoring.scoring('nfl',csv_output)


i = 0
row_num = len(df)

for i in range(0,row_num):
	f1 = df['player'][i].split(' ') # split() only once
	first_name = f1[0]
	last_name = f1[1]
	new_player = first_name + " " + last_name
	df['player'][i] = new_player
	i = i+ 1


df_2 = df[(df['nfl'] > 0)]  # How do I drop all zero scores?


df_2.to_csv(csv_output_2)
#dk_file = 'DKweek6salaries.xlsx'#change every week
df = FF_scoring.get_player(csv_output_2,dk_file,86)
df.to_csv(csv_output_2)

