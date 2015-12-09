
import pandas as pd
import numpy as np

week = raw_input("Which week?")
week = str(week)


#--------get the defense--------
def_csv = "weeks/week-" +week + "/def-week" +week + '-2.csv'

df_def = pd.read_csv(def_csv)


csv_dk = "weeks/week-" +week + "/aggregate-week" + week + "dk.csv"
csv_fd = "weeks/week-" +week + "/aggregate-week" + week + "fd.csv"

dk_file = "weeks/week-" +week + "/DKweek" +week +"salaries.xlsx"
fd_file = "weeks/week-" +week + "/FDweek" +week +"salaries.xlsx"



#---------------------

score_list = ['fire','fftoday','fox','fleaflicker','espn','cbs','nfl']

#-----------------------------

s_n = len(score_list)

x=0
for x in range(0,s_n):

ff_csv = "weeks/week-" +week + "/fftoday-week" + week + "-2.csv"
df = pd.read_excel(dk_file)
df_ff = pd.read_csv(ff_csv)
s1 = pd.merge(df_dk, df_ff, how='left', left_on='Name', right_on = 'dk_name')



#-----------------------------

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
df_def = pd.read_csv(def_csv)

s1 = pd.merge(df_dk, df_fl, how='left', left_on='Name', right_on = 'dk_name')
s2 = pd.merge(s1, df_ff, how='left', left_on='Name', right_on = 'dk_name')
s3 = pd.merge(s2, df_espn, how='left', left_on='Name', right_on = 'dk_name')
s4 = pd.merge(s3, df_nfl, how='left', left_on='Name', right_on = 'dk_name')
s5 = pd.merge(s4, df_cbs, how='left', left_on='Name', right_on = 'dk_name')
s6 = pd.merge(s5, df_fox, how='left', left_on='Name', right_on = 'dk_name')
s7 = pd.merge(s6, df_fire, how='left', left_on='Name', right_on = 'dk_name')


df = s7[['Name','Position','Salary','GameInfo','AvgPointsPerGame','teamAbbrev','fftoday','nfl','cbs','fleaflicker','espn','fox','fire']]

#trades.update(config, join = 'left', overwrite = False)
df = df.set_index(['Name'])
print df
df_def = df_def.set_index(['Name'])
print df_def
df.update(df_def, join ='left', overwrite = True)

# need to get another column with averages
df['average'] = df[['fftoday','nfl','cbs','fleaflicker','espn','fox','fire']].mean(axis=1)
df['max'] = df[['fftoday','nfl','cbs','fleaflicker','espn','fox','fire']].max(axis=1)
df['min'] = df[['fftoday','nfl','cbs','fleaflicker','espn','fox','fire']].min(axis=1)
df['range'] = df['max'] - df['min']
df['rel_range'] = df['range']/df['average']
df['upside'] = df['max'] -df['average']

df.to_csv(csv_output)

