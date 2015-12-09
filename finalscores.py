#http://games.espn.go.com/ffl/leaders?&startIndex=0&scoringPeriodId=9&seasonId=2015

import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np


week = raw_input("Which week?") # for ESPN, this is for the csv_output (auto-refreshes projections)
week = str(week)

csv_output = "weeks/week-" +week + "/finalscore-week" + week + ".csv"
csv_output_dk = "weeks/week-" +week + "/finalscore-week" + week + "-dk.csv"
csv_output_fd = "weeks/week-" +week + "/finalscore-week" + week + "-fd.csv"
agg_dk = "weeks/week-" +week + "/aggregate-week" + week + "dk.csv"
agg_fd = "weeks/week-" +week + "/aggregate-week" + week + "fd.csv"
dk_file = "weeks/week-" +week + "/DKweek" +week +"salaries.xlsx"  #weekly salary file
fd_file = "weeks/week-" +week + "/FDweek" +week +"salaries.xlsx"  #weekly salary file


#excel_doc = 'Week ' + week +'.xlsx' 
#dk_file = 'DKweek'+week+'salaries.xlsx' #change every week
#agg = "aggregate-week" + week + ".csv"

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


#-------------------------------------------------


#final = FF_scoring.scoring('final',csv_output)
#df_fin = pd.DataFrame(final)

# cleaning the names for easier fuzzy logic
#----------------------------
df = pd.read_csv(csv_output)

i = 0
row_num = len(df)

for i in range(0,row_num):
	f1 = df['player'][i].split(',') # split() only once
	new_player = f1[0]
	df['player'][i] = new_player
	i = i+ 1

df.to_csv(csv_output)

#-------------------------------

df_dk = FF_scoring.scoring('final',csv_output)
df_fd = FF_scoring.fd_scoring('final',csv_output)

df_dk_2 = df_dk[(df_dk['final'] > 1)]  # cleaning low scores
df_fd_2 = df_fd[(df_fd['final'] > 1)]  # cleaning low scores

df_dk_2.to_csv(csv_output_dk)
df_fd_2.to_csv(csv_output_fd)

df_dk = FF_scoring.get_player(csv_output_dk,dk_file,86)
df_fd = FF_scoring.get_player(csv_output_fd,fd_file,86)

df_dk.to_csv(csv_output_dk)
df_fd.to_csv(csv_output_fd)


#-----------------------


#accumulating with aggregate scores
df_agg_dk = pd.read_csv(agg_dk)
df_agg_fd = pd.read_csv(agg_fd)

df_dk = pd.merge(df_agg_dk, df_dk, how='left', left_on='Name', right_on = 'dk_name')
df_fd = pd.merge(df_agg_fd, df_fd, how='left', left_on='Name', right_on = 'dk_name')

df_dk = df_dk[['Name','Position','Salary','GameInfo','AvgPointsPerGame','teamAbbrev','fftoday','nfl','cbs','fleaflicker','espn','fire','average','max','min','range','rel_range','upside','final']]
df_fd = df_fd[['Id','Name','Position','Salary','Game','FPPG','teamAbbrev','fftoday','nfl','cbs','fleaflicker','espn','fire','average','max','min','range','rel_range','upside','final']]

df_dk.to_csv(csv_output_dk)
df_fd.to_csv(csv_output_fd)

#df = df.drop('Unnamed: 0_x', 1)
#df = df.drop('Unnamed: 0_y', 1)
#df = df.drop('player', 1)
#df = df.drop('dk_name', 1)
#df = s1.drop(s1.columns[['Unnamed: 0_y','player','dk_name']], axis=1, inplace=True)

#df.to_csv(csv_output)
#this fucking works
