import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

data = []

week = raw_input("Which week?")
week = str(week)

#dk_file = 'DKweek6salaries.xlsx'#change every week
dk_file = "DKweek" +week +"salaries.xlsx"
csv_output = "fftoday-week" + week + ".csv"
csv_output_2 = "fftoday-week" + week + "-2" + ".csv"
first_half = "http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek="
second_section = "&PosID="
last_half = "&LeagueID=1"

#position is 10 for QB, 20 for RB, 30 for WR, 40 for TE
data_QB = [['player','team','opp','comp','pass_att','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds','fan_pts','fl','rec','rec_yards','rec_tds','punt_td','kick_td','2-pt']]
position = '10'
csv_pos = 'QB.csv'
url = first_half + week + second_section +position + last_half
html = urllib2.urlopen(url).read()
#print html
soup = BeautifulSoup(html,"lxml")
table = soup.find('table', attrs={'cellpadding':'2'})
#print table
table_body = table.find('tbody')
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
#page_num =page_num+1
df = pd.read_csv(csv_pos)
df['fl']=0
df['rec_yards']=0
df['rec_tds']=0
df['2-pt']=0
df['rec']=0
df['punt_td']=0
df['kick_td']=0
df.to_csv(csv_pos)

df_qb = FF_scoring.scoring('fftoday',csv_pos)


# RBs
last_half = "&order_by=FFPts&sort_order=DESC&cur_page="
data_RB = [['player','team','opp','rush_att','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','fl','punt_td','kick_td','2-pt','pass_yards','pass_tds','int']]

page_num = 1
for page_num in range(1,3):
	position = '20'
	csv_pos = 'RB.csv'
	page_mult = (page_num-1)
	next = str(page_mult)
	url = first_half + week + second_section +position + last_half + next
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")
	table = soup.find('table', attrs={'cellpadding':'2'})
	table_body = table.find('tbody') #not used for FFToday
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
	page_num =page_num+1
df = pd.read_csv(csv_pos)

df['fl']=0
df['pass_yards']=0
df['pass_tds']=0
df['2-pt']=0
df['int']=0
df['punt_td']=0
df['kick_td']=0
df.to_csv(csv_pos)

df_rb = FF_scoring.scoring('fftoday',csv_pos)



# WRs
last_half = "&order_by=FFPts&sort_order=DESC&cur_page="
data_WR = [['player','team','opp','rec','rec_yards','rec_tds','fan_pts','fl','punt_td','kick_td','2-pt','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds']]

last_half = "&order_by=FFPts&sort_order=DESC&cur_page="
page_num = 1
for page_num in range(1,3):
	position = '30'
	csv_pos = 'WR.csv'
	page_mult = (page_num-1)
	next = str(page_mult)
	url = first_half + week + second_section +position + last_half + next
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html,"lxml")

	table = soup.find('table', attrs={'cellpadding':'2'})
	table_body = table.find('tbody') #not used for FFToday

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
	page_num =page_num+1

df = pd.read_csv(csv_pos)

df['rush_att']=0 
df['rush_yards']=0 
df['rush_tds']=0
df['fl']=0
df['pass_yards']=0
df['pass_tds']=0
df['2-pt']=0
df['int']=0
df['punt_td']=0
df['kick_td']=0
df.to_csv(csv_pos)

df_wr = FF_scoring.scoring('fftoday',csv_pos)

#TEs
last_half = "&LeagueID=1"
data_TE = [['player','team','opp','rec','rec_yards','rec_tds','fan_pts','fl','punt_td','kick_td','2-pt','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds']]
position = '40'
csv_pos = 'TE.csv'
url = first_half + week + second_section +position + last_half
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html,"lxml")

table = soup.find('table', attrs={'cellpadding':'2'})
table_body = table.find('tbody')

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

df = pd.read_csv(csv_pos)
df['rush_att']=0 
df['rush_yards']=0 
df['rush_tds']=0
df['fl']=0
df['pass_yards']=0
df['pass_tds']=0
df['2-pt']=0
df['int']=0
df['punt_td']=0
df['kick_td']=0
df.to_csv(csv_pos)

df_te = FF_scoring.scoring('fftoday',csv_pos)
df = pd.concat([df_qb,df_rb,df_wr,df_te], axis=0, ignore_index=True)
print df



df_2 = df[(df['fftoday'] > 1)]  # How do I drop all zero scores?

df_2.to_csv(csv_output_2)
df = FF_scoring.get_player(csv_output_2,dk_file,86)
df.to_csv(csv_output_2)


#http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek=2&PosID=20&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=1
#http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek=2&PosID=20&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=1
#http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek=2&PosID=20&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0
#http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek=2&PosID=30&LeagueID=1
#http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek=2&PosID=40&LeagueID=1



#this fucking works

