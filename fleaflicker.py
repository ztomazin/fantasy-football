#This one works - 9/20

import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

week = raw_input("Which week?") # for fleaflicker, this is for the csv_output (auto-refreshes projections)
week = str(week)


dk_file = "DKweek" +week +"salaries.xlsx"

csv_output = "fleaflicker-week" + week + ".csv"
csv_output_2 = "fleaflicker-week" + week + "-2" + ".csv"

data = []
first_half ="http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=" 
last_half = "&tableOffset="

#position is 11 for RB/WR/TE, 4 for QB, 256 for DEF
#table_offset is for page # 
data_FL = [['player','pos','team','bye','opp','rush_att','rush_yards','rush_tds','rec','tar','rec_yards','rec_tds','fl','misc_yard','misc_td','punt_td','kick_td','fan_pts','own','2-pt','pass_yards','pass_tds','int']]

page_num = 1
for page_num in range(1,14):
	position = '11'
	csv_pos = 'FL.csv'
	page_mult = (page_num-1) * 20
	next = str(page_mult)
	url = first_half + position + last_half + next
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'table-group table table-striped table-bordered table-hover'})

	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    cols = [ele.encode('ascii','ignore') for ele in cols]
	    data_FL.append([ele for ele in cols if ele]) # Get rid of empty values
	b = open(csv_pos, 'w')
	a = csv.writer(b)
	a.writerows(data_FL)	
	b.close()
	page_num =page_num+1

df_FL = FF_scoring.scoring('fleaflicker',csv_pos)

# for QBs
data_QB = [['player','pos','team','bye','opp','comp','pass_att','comp-%','pass_yards','pass_tds','int','QB_rat','rush_att','rush_yards','rush_tds','fan_pts','own-%','fl','rec','rec_yards','rec_tds','punt_td','kick_td','2-pt']]
page_num = 1
for page_num in range(1,3):
	position = '4'
	csv_pos = 'QB.csv'
	page_mult = (page_num-1) * 20
	next = str(page_mult)
	url = first_half + position + last_half + next
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'table-group table table-striped table-bordered table-hover'})

	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')   
	    cols = [ele.text.strip() for ele in cols]
	    cols = [ele.encode('ascii','ignore') for ele in cols]
	    data_QB.append([ele for ele in cols if ele]) # Get rid of empty values
	b = open(csv_pos, 'w')
	a = csv.writer(b)
	a.writerows(data_QB)	
	b.close()
	page_num =page_num+1

df_QB = FF_scoring.scoring('fleaflicker',csv_pos)

# for DEF
page_num = 1
for page_num in range(1,3):
	position = '256'
	page_mult = (page_num-1) * 20
	next = str(page_mult)
	url = first_half + position + last_half + next
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'table-group table table-striped table-bordered table-hover'})
	#table_body = table.find('tbody') no tbody in table

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
	page_num =page_num+1



df = pd.concat([df_QB,df_FL,], axis=0, ignore_index=True)
print df


df_2 = df[(df['fleaflicker'] > 0)]  # How do I drop all zero scores?


df_2.to_csv(csv_output_2)
#dk_file = 'DKweek6salaries.xlsx'#change every week
df = FF_scoring.get_player(csv_output_2,dk_file,86)
df.to_csv(csv_output_2)

#this fucking works
# RB/WR/TE http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=11
#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=11&tableOffset=20
#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=11
#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=11&tableOffset=40

#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=4
#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=4&tableOffset=0
#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=4&tableOffset=20

#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=256
#http://www.fleaflicker.com/nfl/leaders?statType=7&sortMode=7&position=256&tableOffset=20