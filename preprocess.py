
# coding: utf-8

# In[1]:

import pandas as pd
import scipy as sp
import numpy as np
import csv
import sys
import os
import math


# In[2]:

columns = ('date', 'time', 'sensor', 'reading', 'activity','activity_switch')


# In[3]:

dataset='hh122'


# In[4]:

df = pd.read_csv('./data/'+dataset+'/data.txt',delim_whitespace=True, names=columns,parse_dates=[[0,1]])


# In[5]:

df.loc[df.activity=='Leave_Home'].head()


# In[6]:

df.reading.unique()


# In[7]:

sensor_bi = df.loc[(df.reading=='ON')|(df.reading=='OFF')].sensor.unique()
sensor_bi


# In[8]:

tdf = pd.DataFrame(df,index = df.date_time)
h = tdf.index.hour
d = tdf.index.day
df['hour']=h
df['day']=d


# In[9]:

sensors_name = df.sensor.unique()
sensors_name


# In[10]:

switch = df.activity_switch.unique()
switch


# In[29]:

df.loc[df.activity_switch=='begin'].head()


# In[11]:

activity = df.activity.unique()
activity


# In[12]:

begin = df[(df.activity_switch == 'begin')].index
end = df[(df.activity_switch == 'end')].index


# In[13]:

for i,j in zip(begin,end):
    act = df.loc[i,'activity']
    if (df.loc[j,'activity']==act):
        df.loc[i+1:j,'activity'] = act


# In[14]:

for act in activity:
    print act
    begin = df[(df.activity == act) & (df.activity_switch == 'begin')].index
    end = df[(df.activity == act) & (df.activity_switch == 'end')].index
    print len(begin),len(end)

# In[16]:

sensor_bi


# In[17]:

sdf = pd.DataFrame()
i = 1
for s in sensor_bi:
    #idx = df.loc[df.activity == a]
    print s,i
    #print df.loc[df.activity == a]
    sdf = sdf.append(df.loc[df.sensor == s])
    sdf.loc[sdf.sensor==s,'sensor']=i
    i+=1
sdf.shape


# In[18]:

sdf.loc[sdf.reading=='ON','reading']=1
sdf.loc[sdf.reading=='OFF','reading']=-1
sdf.head()


# In[19]:

#ndf = pd.DataFrame()
i = 1
for a in activity:
    #idx = df.loc[df.activity == a]
    print a,i
    sdf.loc[sdf.activity==a,'activity']=i
    i+=1
    #print df.loc[df.activity == a]
    #ndf = ndf.append(sdf.loc[sdf.activity == a])
sdf.head()


# In[20]:

activity = sdf.activity.unique()
activity


# In[26]:

acts=np.array(sdf.activity)
tmp=(acts>0)==False
acts[tmp]=np.argmin((activity>0))+1
sdf.activity=acts


# In[27]:

sdf=sdf.sort_index()
sdf.head()


# In[28]:

sdf=sdf.drop('activity_switch',1)
sdf.head()


# In[45]:

sdf.to_csv('./data/'+dataset+'/raw_filtered.csv',index=False,encoding='utf-8')





