# common modules
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.stats.api as sms

# plot modules
import matplotlib.pyplot as plt
import matplotlib
%matplotlib inline
matplotlib.style.use('ggplot')

path = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_200201.txt'
col_name_new = ['C/A','UNIT','SCP','STATION','LINENAME','DIVISION','DATE','TIME','DESC','ENTRIES','EXITS']
MTA_raw = pd.read_csv(path, sep=",", header=0, names = col_name_new)

MTA_data=np.array(MTA_raw)

#print(MTA_data[:,0])
x=5

#72 street index
ST_72=[]
for i in range(len(MTA_data)):
  if MTA_data[i,3]=='72 ST'and MTA_data[i,4]=="123" and not MTA_data[i,7]=="07/04/2020" and not MTA_data[i,7]=="07/05/2020":
    ST_72.append(i)
ST_72=np.array(ST_72)
#print(ST_72)
#print(MTA_data[ST_72[0]])

#72nd street entries and exits on 07/04/2020
#Entry differences
print("Entries")
Entry_diff=[]
for i in range(5):
  Entry_diff.append(abs(MTA_data[ST_72[i],9]-MTA_data[ST_72[i]+1,9]))
print(Entry_diff)

#Exit differences
print("Exits")
Exit_diff=[]
for i in range(x):
  Exit_diff.append(abs(MTA_data[ST_72[i],10]-MTA_data[ST_72[i]+1,10]))
print(Exit_diff)

#first five entries of ST_72 to check correctness of data set
plt.scatter(x=np.arange(2,22,4), y=Entry_diff, c='r',label="entry")
plt.scatter(x=np.arange(2,22,4), y=Exit_diff, c='b',label="exit")
plt.legend(loc="upper left")
plt.show