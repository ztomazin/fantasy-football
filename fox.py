

import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

week = raw_input("Which week?") # for ESPN, this is for the csv_output (auto-refreshes projections)
week = str(week)

dk_file = "DKweek" +week +"salaries.xlsx"
csv_output = "fox-week" + week + ".csv"
excel_output = "fox-week" + week + ".xlsx"
csv_output_2 = "fox-week" + week + "-2" + ".csv"
data = [['player','status','pass_tds','pass_yards','pass_att','comp','int','rush_tds','rush_yards','rush_att','rec_tds','rec_yards','rec','2-pt','def_td','fl','fan_pts','punt_td','kick_td',]]

url_format = 'http://www.foxsports.com/fantasy/football/commissioner/Research/Projections.aspx?page={page_num}&position=-1&split=4'

page_num = 1


for page_num in range(1,14):
	next = str(page_num)		
	url = url_format.format(page_num=next)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'wis_standard playerTable'})
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


fox = FF_scoring.scoring('fox',csv_output)
df = pd.DataFrame(fox)

i = 0
row_num = len(df)

for i in range(0,row_num):
	f1 = df['player'][i].split('\n') # split() only once
	new_player = f1[0]
	df['player'][i] = new_player
	i = i+ 1

#print df

df_2 = df[(df['fox'] > 0)]  # cleaning low scores
df_2.to_csv(csv_output_2)

df = FF_scoring.get_player(csv_output_2,dk_file,86)
df.to_csv(csv_output_2)

