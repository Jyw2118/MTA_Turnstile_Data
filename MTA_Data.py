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


#finding mean of time increments (1-5-9-13-17-21)
#loop through that 72nd street data, find difference, if 7th column = 1,5,9,13 or 17
#subtract add to corresponding values, divide by 7

#Entry differences
print("Mean of Entries")
M_Entry_diff=[0,0,0,0,0]
for i in range(len(ST_72)-1):
  diff=(abs(MTA_data[ST_72[i],9]-MTA_data[ST_72[i]+1,9]))
  if (MTA_data[ST_72[i],7]=='01:00:00'):
    M_Entry_diff[0]+=diff
  elif (MTA_data[ST_72[i],7]=='05:00:00'):
    M_Entry_diff[1]+=diff
  elif (MTA_data[ST_72[i],7]=='09:00:00'):
    M_Entry_diff[2]+=diff
  elif (MTA_data[ST_72[i],7]=='13:00:00'):
    M_Entry_diff[3]+=diff
  elif (MTA_data[ST_72[i],7]=='17:00:00'):
    M_Entry_diff[4]+=diff
#print(M_Entry_diff)

M_Entry=[]
for i in M_Entry_diff:
  M_Entry.append(int(i/7))
print (M_Entry)

#Exit differences
print("Mean of Exits")
M_Exit_diff=[0,0,0,0,0]
for i in range(len(ST_72)-1):
  diff=(abs(MTA_data[ST_72[i],10]-MTA_data[ST_72[i]+1,10]))
  if (MTA_data[ST_72[i],7]=='01:00:00'):
    M_Exit_diff[0]+=diff
  elif (MTA_data[ST_72[i],7]=='05:00:00'):
    M_Exit_diff[1]+=diff
  elif (MTA_data[ST_72[i],7]=='09:00:00'):
    M_Exit_diff[2]+=diff
  elif (MTA_data[ST_72[i],7]=='13:00:00'):
    M_Exit_diff[3]+=diff
  elif (MTA_data[ST_72[i],7]=='17:00:00'):
    M_Exit_diff[4]+=diff
#print(M_Exit_diff)

M_Exit=[]
for i in M_Exit_diff:
  M_Exit.append(int(i/7))
print (M_Exit)


plt.scatter(x=np.arange(3,23,4), y=M_Entry, c='r',label="Mean Entry")
plt.scatter(x=np.arange(3,23,4), y=M_Exit, c='b',label="Mean Exit")
plt.legend(loc="lower right")
plt.show()


#prints out the mean of all the entries and exits in 24 hours
print("Mean of All Entries")
M_Entry_All=[0,0,0,0,0]
for i in range(len(MTA_data)-1):
  diff=(abs(MTA_data[i,9]-MTA_data[i+1,9]))
  if (MTA_data[i,7]=='01:00:00'):
    M_Entry_All[0]+=diff
  elif (MTA_data[i,7]=='05:00:00'):
    M_Entry_All[1]+=diff
  elif (MTA_data[i,7]=='09:00:00'):
    M_Entry_All[2]+=diff
  elif (MTA_data[i,7]=='13:00:00'):
    M_Entry_All[3]+=diff
  elif (MTA_data[i,7]=='17:00:00'):
    M_Entry_All[4]+=diff
print(M_Entry_All)

M_Entry_A=[]
for i in M_Entry_All:
  M_Entry_A.append(int(i/7))
print (M_Entry_A)

print("Mean of All Exits")
M_Exit_All=[0,0,0,0,0]
for i in range(len(MTA_data)-1):
  diff=(abs(MTA_data[i,10]-MTA_data[i+1,10]))
  if (MTA_data[i,7]=='01:00:00'):
    M_Exit_All[0]+=diff
  elif (MTA_data[i,7]=='05:00:00'):
    M_Exit_All[1]+=diff
  elif (MTA_data[i,7]=='09:00:00'):
    M_Exit_All[2]+=diff
  elif (MTA_data[i,7]=='13:00:00'):
    M_Exit_All[3]+=diff
  elif (MTA_data[i,7]=='17:00:00'):
    M_Exit_All[4]+=diff
print(M_Exit_All)

M_Exit_A=[]
for i in M_Exit_All:
  M_Exit_A.append(int(i/7))
print (M_Exit_A)


plt.scatter(x=np.arange(3,23,4), y=M_Entry_A, c='r',label="Mean Entry")
plt.scatter(x=np.arange(3,23,4), y=M_Exit_A, c='b',label="Mean Exit")
plt.legend(loc="upper left")
plt.show()



#Morning rush hour in a specific day (all stations)
#07/21/2020
#times start at 4,5,6,7- 8,9,10,11
print("Morning Rush Hour Entries")
Morning_Entry=0
for i in range(len(MTA_data)-1):
  if (MTA_data[i,6] == "07/21/2020" and (MTA_data[i,7]=='04:00:00' or
                                         MTA_data[i,7]=='05:00:00' or
                                         MTA_data[i,7]=='06:00:00' or
                                         MTA_data[i,7]=='07:00:00')):
    diff=(abs(MTA_data[i,9]-MTA_data[i+1,9]))
    Morning_Entry+=diff
print(Morning_Entry)

print("Morning Rush Hour Exits")
Morning_Exit=0
for i in range(len(MTA_data)-1):
  if (MTA_data[i,6] == "07/21/2020" and (MTA_data[i,7]=='04:00:00' or
                                         MTA_data[i,7]=='05:00:00' or
                                         MTA_data[i,7]=='06:00:00' or
                                         MTA_data[i,7]=='07:00:00')):
    diff=(abs(MTA_data[i,10]-MTA_data[i+1,10]))
    Morning_Exit+=diff
print(Morning_Exit)

print("Difference",abs(Morning_Entry-Morning_Exit))


#Evening rush hour in a specific day (all stations)
#07/21/2020
#times start at 16,17,18,19-20,21,22,23
print("Evening Rush Hour Entries")
Evening_Entry=0
for i in range(len(MTA_data)-1):
  if (MTA_data[i,6] == "07/21/2020" and (MTA_data[i,7]=='16:00:00' or
                                         MTA_data[i,7]=='17:00:00' or
                                         MTA_data[i,7]=='18:00:00' or
                                         MTA_data[i,7]=='19:00:00')):
    diff=(abs(MTA_data[i,9]-MTA_data[i+1,9]))
    Evening_Entry+=diff
print(Evening_Entry)

print("Evening Rush Hour Exits")
Evening_Exit=0
for i in range(len(MTA_data)-1):
  if (MTA_data[i,6] == "07/21/2020" and (MTA_data[i,7]=='16:00:00' or
                                         MTA_data[i,7]=='17:00:00' or
                                         MTA_data[i,7]=='18:00:00' or
                                         MTA_data[i,7]=='19:00:00')):
    diff=(abs(MTA_data[i,10]-MTA_data[i+1,10]))
    Evening_Exit+=diff
print(Evening_Exit)

print("Difference", abs(Evening_Entry-Evening_Exit))



