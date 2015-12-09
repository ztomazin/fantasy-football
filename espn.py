

import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

week = raw_input("Which week?") # for ESPN, this is for the csv_output (auto-refreshes projections)
week = str(week)

#dk_file = 'DKweek6salaries.xlsx' #change every week
#dk_file = "DKweek" +week +"salaries.xlsx"
csv_output = "weeks/week-" +week + "/espn-week" + week + ".csv"
#excel_output = "espn-week" + week + ".xlsx"
csv_output_2 = "weeks/week-" +week + "/espn-week" + week + "-2" + ".csv"
data = [['player','opp','status','comp/att','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','punt_td','kick_td','fl','2-pt']]
first_half = "http://games.espn.go.com/ffl/tools/projections?startIndex="
page_num = 1


for page_num in range(1,14):
	page_mult = (page_num-1) * 40
	next = str(page_mult)
	url = first_half + next
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


#espn = FF_scoring.scoring('espn',csv_output)
#df_espn = pd.DataFrame(espn)


df = pd.read_csv(csv_output)

i = 0
row_num = len(df)

for i in range(0,row_num):
	f1 = df['player'][i].split(',') # split() only once
	new_player = f1[0]
	df['player'][i] = new_player
	i = i+ 1

df.to_csv(csv_output)

#-----keepfornow-----this is in dk_scoring---


#df = FF_scoring.scoring('espn',csv_output)
#df_espn_2 = df[(df['espn'] > 1)]  # cleaning low scores

#df_espn_2.to_csv(csv_output_2)

#df = FF_scoring.get_player(csv_output_2,dk_file,86)
#df.to_csv(csv_output_2)


#this fucking works

#http://games.espn.go.com/ffl/tools/projections?startIndex=0