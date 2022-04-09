#!/usr/bin/env python
# coding: utf-8

# # Part2_peijin

# In[2]:


import pandas as pd
import numpy as np
from plotnine import*
import seaborn as sns
from statistics import *
import os
import matplotlib.pyplot as plt


# In[3]:


##PART 2
##Q1 Using the original data from the us_states.csv file, find the state that has recorded the highest number of new cases per 100,000 residents between September 1 and September 28, inclusive5 . Display the state and the number of new cases per 100,000 residents.
us_states=pd.read_csv("us_states.csv") ##read the us_states.csv file as a Pandas DataFrame
us_states.head()##Print the first 5 rows in the dataset 


# In[4]:


state_ACS_data=pd.read_csv("state_ACS_data.csv")##load the data of ACS
state_ACS_data.head()


# In[5]:


us_states_selec=us_states.filter(["date","state","cases"])##select the columns needed in Q1


# In[6]:


us_states_selec=us_states_selec.merge(state_ACS_data,how="left",on="state")


# In[7]:


us_states_selec.sort_values(by=["state","date"])## sort the data and look into the data
us_states_selec.head()


# In[8]:


us_states_selecA=us_states_selec.loc[us_states_selec.date=="2020-08-31", :]##select the data of "2020-09-01" and form a df
us_states_selecA.head()##look into the data


# In[9]:


us_states_selecB=us_states_selec.loc[us_states_selec.date=="2020-09-28", :]##select the data of "2020-09-28" and form a df
us_states_selecB.head()##look into the data


# In[10]:


us_states_selecC=us_states_selecA.merge(us_states_selecB,how="outer",on="state")
us_states_selecC=us_states_selecC.rename(columns={"cases_x":"cases_0831","cases_y":"cases_0928","date_x":"date_0831","date_y":"date_0928","State_Population_x":"State_Population"})##rename the columns 
us_states_selecC.head()##look into the data 


# In[11]:


us_states_selecC["diff_0831_0928"]=us_states_selecC["cases_0928"]-us_states_selecC["cases_0831"]
us_states_selecC["new_cases_per_100000_residents"]=us_states_selecC["diff_0831_0928"]/us_states_selecC["State_Population"]*100000
us_states_selecC.head()##look into the data 


# In[12]:


us_states_selecC.sort_values("new_cases_per_100000_residents",ascending=False).head(3)## sort the data and look into the highest number of new cases per 100,000 residents between September 1 and September 28
##North Dakota has the highest number of new cases per 100,000 residents between September 1 and September 28, with the new_cases_per_100000_residents of 1218.557274


# In[13]:


##Display the state and the number of new cases per 100,000 residents
us_states_selecC=us_states_selecC.filter(["state","date_0831","cases_0831","date_0928","cases_0928","diff_0831_0928","new_cases_per_100000_residents"])##rearrange the columns 
us_states_selecC.head()


# In[14]:


us_states_selecC=us_states_selecC.drop(columns=["date_0831","cases_0831","date_0928","cases_0928"])##drop colums 
us_states_selecC.head()##Display the state and the number of new cases per 100,000 residents


# In[15]:


##Q2 Using the original data from the us_states.csv file, create new variables equal to the number of daily new cases and deaths.6 Display summary statistics for these two variables
us_states_Q2=us_states##load the data and look into it 
us_states_Q2.head()


# In[16]:


us_states_Q2=us_states_Q2.sort_values(by=["state","date"])## sort the data and look into the data
us_states_Q2


# In[17]:


us_states_Q2["daily_new_cases"]=us_states_Q2.groupby(['state'])[['cases']].diff()##creat a new df of "daily_new_cases"
us_states_Q2["daily_new_deaths"]=us_states_Q2.groupby(['state'])[['deaths']].diff()##creat a new df of "daily_new_deaths"
us_states_Q2.fillna(0)##fill the NaN with 0


# In[18]:


##Display summary statistics for these two variables.
us_states_Q2[['daily_new_cases','daily_new_deaths']].describe()


# In[19]:


##Q3 Pick a state that had a stay at home order that expired (before September 28) and generate a plot of daily new cases. Add vertical lines corresponding to the start and end dates of the stay-at-home order. Comment briefly on any patterns you notice.
all_merge_2=pd.read_csv("all_merge_2.csv") ##read the all_merge_2.csv file as a Pandas DataFrame
all_merge_2.head(3)##check out the data 


# In[20]:


##pick the state:Alabama( accoring to "all_merge_2", it had a stay at home order that expired)
all_merge_2.loc[all_merge_2.state=="Alabama"]##look up the data of "Alabama"
##the start and end dates of the stay-at-home order is 4/4/2020 - 4/30/2020


# In[21]:


us_states_Alabama=us_states.loc[us_states.state=="Alabama"]##select the data of "Alabama"
us_states_Alabama##look into the data


# In[22]:


us_states_Alabama["daily_new_cases"]=us_states_Alabama["cases"].diff()##create a new column of "daily_new_cases" of Alabama
us_states_Alabama=us_states_Alabama.fillna(0)##fill the NaN with 0
us_states_Alabama## look into the data


# In[23]:


us_states_Alabama.loc[us_states_Alabama.date=="2020-04-04"]##look up the data of "2020-04-04"


# In[24]:


us_states_Alabama.loc[us_states_Alabama.date=="2020-04-30"]##look up the data of "2020-04-30"


# In[25]:


us_states_Alabama["date"]=pd.to_datetime(us_states_Alabama.date)


# In[26]:


plt.figure(figsize=(12,8))
##draw the plot of daily new cases.
sns.scatterplot(x = 'date', y = 'daily_new_cases',data=us_states_Alabama)
plt.xlabel("Cases per day")
plt.title("Alabama Daily New Cases")
plt.axvline(x=pd.to_datetime("2020-04-04"),ls="-",c="green")###add vertical lines corresponding to the start and end dates of the stay-at-home order.
plt.axvline(x=pd.to_datetime("2020-04-30"),ls="-",c="green")
plt.show()
##Comment:Cases per day increased more slowly during the stay-at-home order period than during other periods of the time


# In[27]:


##Q4 Create a new DataFrame that contains the number of daily new cases and deaths per 100,000 residents among the states that Donald Trump won and the states that Hillary Clinton won (i.e., for a given date you should have one observation corresponding to the group of states that voted for Trump in 2016, and another corresponding to the group of states that voted for Clinton). Plot the number of daily new deaths per 100,000 over time in these two groups of states, using appropriate colors (i.e., red and blue) for the corresponding lines. Comment briefly on any patterns you notice.
election_results=pd.read_csv("2016_election_results.csv")##load the election results data
election_results.head()


# In[28]:


df=pd.get_dummies(election_results.trump_won)##create a dummy variable based on "trump_won"
df=df.rename(columns={"No":"Trump","Yes":"Clinton"})##rename the columns 
df.head()


# In[29]:


df=pd.merge(df, election_results, left_index=True, right_index=True)
df=df.rename(columns={"state_x":"state"})##rename the columns 
df.head()


# In[30]:


us_states_Q4=us_states
us_states_Q4##create a new df for Q4


# In[31]:


us_states_Q4=pd.merge(us_states_Q4, df, how="left",on="state")## merge two columns 
us_states_Q4##look into the data


# In[32]:


us_states_Q4.sort_values(by=["state","date"])## sort the data and look into the data
us_states_Q4##look into the data


# In[33]:


us_states_Q4["daily_new_deaths"]=us_states_Q4.groupby(['state'])[['deaths']].diff()##create a new df of "daily_new_deaths"
us_states_Q4["daily_new_cases"]=us_states_Q4.groupby(['state'])[['cases']].diff()##create a new df of "daily_new_cases"
us_states_Q4##look into the data


# In[34]:


us_states_Q4=us_states_Q4.fillna(0)##fill the NaN with 0
us_states_Q4.head()##look into the data


# In[35]:


us_states_Q4=us_states_Q4.merge(state_ACS_data,how="left",on="state")##add the column of "State_Population"
us_states_Q4.head()##look into the data


# In[36]:


us_states_Q4["new_cases_per_100000_residents"]=us_states_Q4["daily_new_cases"]/us_states_Q4["State_Population"]*100000##cacluate the "new_cases_per_100000_residents"
us_states_Q4["new_deaths_per_100000_residents"]=us_states_Q4["daily_new_deaths"]/us_states_Q4["State_Population"]*100000##cacluate the "new_deaths_per_100000_residents"
us_states_Q4.head()##look into the data


# In[37]:


us_states_Q4=us_states_Q4.merge(election_results,how="left",on="state")##merge two columns
us_states_Q4##look into the data


# In[38]:


us_states_Q4["Trump_state"]=us_states_Q4["Trump"]*us_states_Q4["new_deaths_per_100000_residents"]##calulate the data of "new_deaths_per_100000_residents" for "Trump_state"
us_states_Q4["Clinton_state"]=us_states_Q4["Clinton"]*us_states_Q4["new_deaths_per_100000_residents"]####calulate the data of "new_deaths_per_100000_residents" for "Clinton_state"


# In[39]:


us_states_Q4##look into the data


# In[40]:


us_states_Q4_1=us_states_Q4.groupby(["date"])[["Trump_state"]].sum()##add up the data of one group od states 


# In[41]:


us_states_Q4_2=us_states_Q4.groupby(["date"])[["Clinton_state"]].sum()##add up the data of one group od states 


# In[42]:


us_states_Q4_3=pd.merge(us_states_Q4_1, us_states_Q4_2, left_index=True, right_index=True)###merge the columns together
us_states_Q4_3##look into the data


# In[43]:


us_states_Q4_3 = us_states_Q4_3.reset_index(drop=False)##reset the index in the column 
us_states_Q4_3##look into the data


# In[44]:


us_states_Q4_3["date"]=pd.to_datetime(us_states_Q4_3.date)


# In[45]:


##Plot the number of daily new deaths per 100,000 over time in these two groups of states
plt.figure(figsize=(18,6))
plt.plot(us_states_Q4_3.loc[:,"date"],us_states_Q4_3.loc[:,"Trump_state"],color="blue")##set the line of "Trump_state"
plt.plot(us_states_Q4_3.loc[:,"date"],us_states_Q4_3.loc[:,"Clinton_state"],color="red")##set the line of "Clinton_state"
plt.xticks(rotation=40)
plt.title("daily new deaths per 100,000 of two grous_states_Q4_3ups of states")
plt.xlabel("date")##label the x axis
plt.ylabel("new_deaths_per_100000_residents")##label the y axis
plt.show## show the plot
##Comment:daily new deaths per 100,000  were higher in states that supported Trump before May, and higher in states that supported Clinton after May.

