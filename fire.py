
#modifying to enable numberfire
#http://www.numberfire.com/nfl/fantasy/fantasy-football-ppr-projections

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

csv_output = "weeks/week-" +week + "/fire-week" + week + ".csv"
#excel_output = "fire-week" + week + ".xlsx"
csv_output_2 = "weeks/week-" +week + "/fire-week" + week + "-2" + ".csv"

data = [['player','opp','opp_rank','overall_rank','pos_rank','pass_yards','pass_tds','int','rush_att','rush_yards','rush_tds','rec','rec_yards','rec_tds','fan_pts','fanduel_pts','fanduel_cost','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','2-pt','fl','punt_td','kick_td',]]
url = 'http://www.numberfire.com/nfl/fantasy/fantasy-football-ppr-projections'
html = urllib2.urlopen(url).read()
soup = BeautifulSoup(html,"lxml")
table = soup.find('table', attrs={'class':'data-table xsmall'})
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


#fire = FF_scoring.scoring('fire',csv_output)
#df = pd.DataFrame(fire)

df = pd.read_csv(csv_output)

i = 0
row_num = len(df)

for i in range(0,row_num):
	f1 = df['player'][i].split('(') # split() only once
	new_player = f1[0]
	df['player'][i] = new_player
	i = i+ 1

df.to_csv(csv_output)

#--------------------------leave for now

#df = FF_scoring.scoring('fire',csv_output)
#df_2 = df[(df['fire'] > 1)]  # cleaning low scores
#df_2.to_csv(csv_output_2)
#df = FF_scoring.get_player(csv_output_2,dk_file,86)
#df.to_csv(csv_output_2)

