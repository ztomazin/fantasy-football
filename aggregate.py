import pandas as pd
import numpy as np

week = raw_input("Which week?")
week = str(week)
csv_output = "aggregate-week" + week + ".csv"



#dk_file = 'DKweek6salaries.xlsx' #change every week
dk_file = "DKweek" +week +"salaries.xlsx"

#each site
ff_csv = "fftoday-week" + week + "-2.csv"
espn_csv = "espn-week" + week + "-2.csv"
fl_csv = "fleaflicker-week" + week + "-2.csv"
nfl_csv = "nfl-week" + week + "-2.csv"
cbs_csv = "cbs-week" + week + "-2.csv"
fox_csv = "fox-week" + week + "-2.csv"
fire_csv = "fire-week" + week + "-2.csv"

#getting the data
df_dk = pd.read_excel(dk_file)
df_ff = pd.read_csv(ff_csv)
df_fl = pd.read_csv(fl_csv)
df_espn = pd.read_csv(espn_csv)
df_nfl = pd.read_csv(nfl_csv)
df_cbs = pd.read_csv(cbs_csv)
df_fox = pd.read_csv(fox_csv)
df_fire = pd.read_csv(fire_csv)

s1 = pd.merge(df_dk, df_fl, how='left', left_on='Name', right_on = 'dk_name')
s2 = pd.merge(s1, df_ff, how='left', left_on='Name', right_on = 'dk_name')
s3 = pd.merge(s2, df_espn, how='left', left_on='Name', right_on = 'dk_name')
s4 = pd.merge(s3, df_nfl, how='left', left_on='Name', right_on = 'dk_name')
s5 = pd.merge(s4, df_cbs, how='left', left_on='Name', right_on = 'dk_name')
s6 = pd.merge(s5, df_fox, how='left', left_on='Name', right_on = 'dk_name')
s7 = pd.merge(s6, df_fire, how='left', left_on='Name', right_on = 'dk_name')


df = s7[['Name','Position','Salary','GameInfo','AvgPointsPerGame','teamAbbrev','fftoday','nfl','cbs','fleaflicker','espn','fox','fire']]

#print df



df.to_csv(csv_output)

