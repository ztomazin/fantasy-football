import pandas as pd
import numpy as np
import csv
from datetime import datetime
import FF_scoring 


data_set = 'finalscore-week7-2.csv'
#getting the data
df = pd.read_csv(data_set)

start_time = datetime.now()


df_final = FF_scoring.optimize_lineup('final',df)




df_final.to_csv('final.csv')


print datetime.now() - start_time