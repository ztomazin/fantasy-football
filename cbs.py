#this work 10-8 needs to be cleaned up



import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

week = raw_input("Which week?")
week = str(week)

url_format = "http://fantasynews.cbssports.com/fantasyfootball/stats/weeklyprojections/{position}/{week}/avg/standard?&print_rows=9999"

dk_file = "DKweek" +week +"salaries.xlsx"
csv_output = "CBS-week" + week + ".csv"
csv_output_2 = "CBS-week" + week + "-2"+ ".csv"

data_QB = [['player','pass_att','comp','pass_yards','pass_tds','int','comp-%','pass_yards/att','rush_att','rush_yards','rush_avg','rush_tds','fl','fan_pts','rec','rec_yards','rec_tds','punt_td','kick_td','2-pt']]
data_RB = [['player','rush_att','rush_yards','rush_avg','rush_tds','rec','rec_yards','avg_yards/rec','rec_tds','fl','fan_pts','punt_td','kick_td','2-pt','pass_yards','pass_tds','int']]
data_WR = [['player','rec','rec_yards','avg_yards/rec','rec_tds','fl','fan_pts','rush_att','rush_yards','rush_avg','rush_tds','punt_td','kick_td','2-pt','pass_yards','pass_tds','int']]
data_TE = [['player','rec','rec_yards','avg_yards/rec','rec_tds','fl','fan_pts','rush_att','rush_yards','rush_avg','rush_tds','punt_td','kick_td','2-pt','pass_yards','pass_tds','int']]

position_list = ['QB','RB','WR','TE','DST']
pos_num = 0

for pos_num in range(0,1):
	position = position_list[pos_num]
	csv_pos = position + ".csv"
	url = url_format.format(position=position,week=week)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'data'})
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
	pos_num = pos_num+1

df_qb = FF_scoring.scoring('cbs',csv_pos)

# this is for RB

for pos_num in range(1,2):
	position = position_list[pos_num]
	csv_pos = position + ".csv"
	url = url_format.format(position=position,week=week)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'data'})
	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    cols = [ele.encode('ascii','ignore') for ele in cols]
	    data_RB.append([ele for ele in cols if ele]) # Get rid of empty values
	b = open(csv_pos, 'w')
	a = csv.writer(b)
	a.writerows(data_RB)
	b.close()
	pos_num = pos_num+1
	
df_rb = FF_scoring.scoring('cbs',csv_pos)

# this is for WR

for pos_num in range(2,3):
	position = position_list[pos_num]
	csv_pos = position + ".csv"
	url = url_format.format(position=position,week=week)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'data'})
	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    cols = [ele.encode('ascii','ignore') for ele in cols]
	    data_WR.append([ele for ele in cols if ele]) # Get rid of empty values
	b = open(csv_pos, 'w')
	a = csv.writer(b)
	a.writerows(data_WR)
	b.close()
	pos_num = pos_num+1

df_wr = FF_scoring.scoring('cbs',csv_pos)

# this is for TE

for pos_num in range(3,4):
	position = position_list[pos_num]
	csv_pos = position + ".csv"
	url = url_format.format(position=position,week=week)
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'class':'data'})
	rows = table.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    cols = [ele.encode('ascii','ignore') for ele in cols]
	    data_TE.append([ele for ele in cols if ele]) # Get rid of empty values
	b = open(csv_pos, 'w')
	a = csv.writer(b)
	a.writerows(data_TE)
	b.close()
	pos_num = pos_num+1

df_te = FF_scoring.scoring('cbs',csv_pos)

### bring it all together
df = pd.concat([df_qb,df_rb,df_wr,df_te], axis=0, ignore_index=True)

#cleaning up the names for matching
i = 0
row_num = len(df)
for i in range(0,row_num):
	f1 = df['player'][i].split(',') # split() only once
	new_player = f1[0]
	df['player'][i] = new_player
	i = i+ 1

df_2 = df[(df['cbs'] > 1)]  # How do I drop all the super low scores?
df_2.to_csv(csv_output_2)
df = FF_scoring.get_player(csv_output_2,dk_file,86)
df.to_csv(csv_output_2)
