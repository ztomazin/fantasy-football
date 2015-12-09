
import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

data = []

week = raw_input("Which week?")
week = str(week)

#dk_file = "DKweek" +week +"salaries.xlsx"
csv_output = "weeks/week-" +week + "/fftoday-week" + week + ".csv"
csv_output_2 = "weeks/week-" +week + "/fftoday-week" + week + "-2" + ".csv"
#first_half = "http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek="
#second_section = "&PosID="
#last_half = "&LeagueID=1"

url_format = "http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek={week}&PosID={position}&LeagueID=1"

#----------------------- QB and TE use this format

#position is 10 for QB, 20 for RB, 30 for WR, 40 for TE
data_QB = [['player','team','opp','comp','pass_att','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds','fan_pts','fl','rec','rec_yards','rec_tds','punt_td','kick_td','2-pt']]
position = '10'
#csv_pos = 'QB.csv'
url = url_format.format(week=week,position=position)
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
b = open(csv_output, 'w')
a = csv.writer(b)
a.writerows(data_QB)
b.close()
#page_num =page_num+1
df_qb = pd.read_csv(csv_output)
df_qb['fl']=0
df_qb['rec_yards']=0
df_qb['rec_tds']=0
df_qb['2-pt']=0
df_qb['rec']=0
df_qb['punt_td']=0
df_qb['kick_td']=0

#-------------------------------------
#TEs
data_TE = [['player','team','opp','rec','rec_yards','rec_tds','fan_pts','fl','punt_td','kick_td','2-pt','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds']]
position = '40'
#csv_pos = 'TE.csv'
url = url_format.format(week=week,position=position)
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
b = open(csv_output, 'w')
a = csv.writer(b)
a.writerows(data_TE)
b.close()

df_te = pd.read_csv(csv_output)
df_te['rush_att']=0 
df_te['rush_yards']=0 
df_te['rush_tds']=0
df_te['fl']=0
df_te['pass_yards']=0
df_te['pass_tds']=0
df_te['2-pt']=0
df_te['int']=0
df_te['punt_td']=0
df_te['kick_td']=0

#-------------------RB & WR use this format
# RBs
url_format = "http://www.fftoday.com/rankings/playerwkproj.php?Season=2015&GameWeek={week}&PosID={position}&order_by=FFPts&sort_order=DESC&cur_page={next}"
data_RB = [['player','team','opp','rush_att','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','fl','punt_td','kick_td','2-pt','pass_yards','pass_tds','int']]

page_num = 1
for page_num in range(1,3):
	position = '20'
#	csv_pos = 'RB.csv'
	page_mult = (page_num-1)
	next = str(page_mult)
	url = url_format.format(week=week,position=position,next=next)
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
	b = open(csv_output, 'w')
	a = csv.writer(b)
	a.writerows(data_RB)
	b.close()
	page_num =page_num+1

df_rb = pd.read_csv(csv_output)
df_rb['fl']=0
df_rb['pass_yards']=0
df_rb['pass_tds']=0
df_rb['2-pt']=0
df_rb['int']=0
df_rb['punt_td']=0
df_rb['kick_td']=0

#----------------------------------------------
# WRs
data_WR = [['player','team','opp','rec','rec_yards','rec_tds','fan_pts','fl','punt_td','kick_td','2-pt','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds']]

page_num = 1
for page_num in range(1,3):
	position = '30'
#	csv_pos = 'WR.csv'
	page_mult = (page_num-1)
	next = str(page_mult)
	url = url_format.format(week=week,position=position,next=next)
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
	b = open(csv_output, 'w')
	a = csv.writer(b)
	a.writerows(data_WR)
	b.close()
	page_num =page_num+1

df_wr = pd.read_csv(csv_output)
df_wr['rush_att']=0 
df_wr['rush_yards']=0 
df_wr['rush_tds']=0
df_wr['fl']=0
df_wr['pass_yards']=0
df_wr['pass_tds']=0
df_wr['2-pt']=0
df_wr['int']=0
df_wr['punt_td']=0
df_wr['kick_td']=0

#df.to_csv(csv_pos)
#df_wr = FF_scoring.scoring('fftoday',csv_pos)

#-------------------------


df = pd.concat([df_qb,df_rb,df_wr,df_te], axis=0, ignore_index=True)
#print df
df.to_csv(csv_output)



#--------------------leaving this here

#df = FF_scoring.scoring('fftoday',csv_output)
#df_2 = df[(df['fftoday'] > 1)]  # How do I drop all zero scores?
#df_2.to_csv(csv_output_2)
#df = FF_scoring.get_player(csv_output_2,dk_file,86)
#df.to_csv(csv_output_2)

