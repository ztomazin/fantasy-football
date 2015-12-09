
import pandas as pd
import numpy as np

week = raw_input("Which week?")
week = str(week)
csv_output = "week-" +week + "/aggregate-week" + week + "fd.csv"





dk_file = "weeks/week-" +week + "/FDweek" +week +"salaries.xlsx"

#each site
ff_csv = "weeks/week-" +week + "/fftoday-week" + week + "-fd.csv"
espn_csv = "weeks/week-" +week + "/espn-week" + week + "-fd.csv"
fl_csv = "weeks/week-" +week + "/fleaflicker-week" + week + "-fd.csv"
nfl_csv = "weeks/week-" +week + "/nfl-week" + week + "-fd.csv"
cbs_csv = "weeks/week-" +week + "/cbs-week" + week + "-fd.csv"
fox_csv = "weeks/week-" +week + "/fox-week" + week + "-fd.csv"
fire_csv = "weeks/week-" +week + "/fire-week" + week + "-fd.csv"
def_csv = "weeks/week-" +week + "/def-week" +week + "-fd.csv"

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
#s6 = pd.merge(s5, df_fox, how='left', left_on='Name', right_on = 'dk_name')
s7 = pd.merge(s5, df_fire, how='left', left_on='Name', right_on = 'dk_name')


df = s7[['Id','Name','Position','Salary','Game','FPPG','Team','fftoday','nfl','cbs','fleaflicker','espn','fire']]

df=df.rename(columns = {'Team':'teamAbbrev'})

#trades.update(config, join = 'left', overwrite = False)
df = df.set_index(['Name'])
print df
df_def = df_def.set_index(['Name'])
print df_def
df.update(df_def, join ='left', overwrite = True)

# need to get another column with averages
df['average'] = df[['fftoday','nfl','cbs','fleaflicker','espn','fire']].mean(axis=1)
df['max'] = df[['fftoday','nfl','cbs','fleaflicker','espn','fire']].max(axis=1)
df['min'] = df[['fftoday','nfl','cbs','fleaflicker','espn','fire']].min(axis=1)
df['range'] = df['max'] - df['min']
df['rel_range'] = df['range']/df['average']
df['upside'] = df['max'] -df['average']

df.to_csv(csv_output)
