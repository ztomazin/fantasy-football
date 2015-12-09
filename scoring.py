


import urllib2
import csv
from bs4 import BeautifulSoup # latest version bs4
import FF_scoring 
import pandas as pd
import numpy as np

week = raw_input("Which week?") # for ESPN, this is for the csv_output (auto-refreshes projections)
week = str(week)

dk_file = "weeks/week-" +week + "/DKweek" +week +"salaries.xlsx"  #weekly salary file
fd_file = "weeks/week-" +week + "/FDweek" +week +"salaries.csv"  #weekly salary file
df = pd.read_csv(fd_file)
df['Name'] = df['First Name'] + " " + df['Last Name']
fd_file = "weeks/week-" +week + "/FDweek" +week +"salaries.xlsx"  #weekly salary file
writer = pd.ExcelWriter(fd_file)
df.to_excel(writer)
writer.save()

#---------------------

#score_list = ['fox'] #['fire','fftoday','fox','fleaflicker','espn','cbs','nfl']
score_list = ['fire','fftoday','fleaflicker','espn','cbs','nfl'] #removed fox, they suck

#-----------------------------

s_n = len(score_list)

x=0
for x in range(0,s_n):
	score = score_list[x]
	csv_output = "weeks/week-" +week + "/" + score + "-week" + week + ".csv"
	csv_output_dk = "weeks/week-" +week + "/" + score + "-week" + week + "-dk.csv"
	csv_output_fd = "weeks/week-" +week + "/" + score + "-week" + week + "-fd.csv"

	df_dk = FF_scoring.scoring(score,csv_output)
	df_fd = FF_scoring.fd_scoring(score,csv_output)

	df_dk_2 = df_dk[(df_dk[score] > 1)]  # cleaning low scores
	df_fd_2 = df_fd[(df_fd[score] > 1)]  # cleaning low scores

	df_dk_2.to_csv(csv_output_dk)
	df_fd_2.to_csv(csv_output_fd)

	df_dk = FF_scoring.get_player(csv_output_dk,dk_file,86)
	df_fd = FF_scoring.get_player(csv_output_fd,fd_file,86)

	df_dk.to_csv(csv_output_dk)
	df_fd.to_csv(csv_output_fd)


#-----------------------------
