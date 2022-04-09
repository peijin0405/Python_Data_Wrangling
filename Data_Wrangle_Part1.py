#!/usr/bin/env python
# coding: utf-8

# # Part1_peijin

# In[2]:


import sys
import pandas as pd
import numpy as np
from plotnine import*
import seaborn as sns
import warnings
warnings.filterwarnings('ignore') # Ignore warnings
import os
import matplotlib.pyplot as plt


# In[3]:


##Part1:Current COVID Data
##Q1(A)
us_states=pd.read_csv("us_states.csv") ##read the us_states.csv file as a Pandas DataFrame
us_states.head()##Print the first 5 rows in the dataset 


# In[4]:


##print the shape of the dataset
us_states.shape


# In[5]:


##Q1(B)
us_states.sort_values('date',ascending=False).head(3)## find the most recent date in the data


# In[6]:


##Create a new object called sept_covid which contains only observations corresponding to the most recent date in the data.
sept_covid=us_states.loc[us_states.date == "2020-09-28"]
sept_covid.head()##check out the data


# In[7]:


##Q2(A)
##read in the files
election_results=pd.read_csv("2016_election_results.csv")
mask_requirement=pd.read_csv("mask_requirement.csv")
state_ACS_data=pd.read_csv("state_ACS_data.csv")
stay_order=pd.read_csv("stay_order.csv.")


# In[8]:


##sovle the typo pronblem: change Kntucky with Kentucky
election_results["state"]=election_results["state"].replace('Kntucky', "Kentucky")
election_results.head()##check out the data


# In[9]:


##sovle the typo pronblem: change Washington, D.C. with Washington
mask_requirement["state"]=mask_requirement["state"].replace('Washington, D.C.', "District of Columbia")
mask_requirement.head()##check out the data


# In[10]:


state_ACS_data.head()##check out the data


# In[11]:


##solve the typo pronblem: change WestVirginia with West Virginia
stay_order["state"]=stay_order["state"].replace('WestVirginia', "West Virginia")
stay_order.head()##check out the data


# In[12]:


## Merge all of these data files together
ele_mask=election_results.merge(mask_requirement,how="outer",on="state")
ele_mask_ACS=ele_mask.merge(state_ACS_data,how="outer",on="state")
ele_mask_ACS_stay=ele_mask_ACS.merge(stay_order,how="outer",on="state")
##then merge this object with sept_covid
all_merge=ele_mask_ACS_stay.merge(sept_covid,how="outer",on="state")
all_merge.head()


# In[13]:


##Q2(B)
##By visually assessing, here are missing/null values in your data
all_merge=all_merge.dropna(subset = ["trump_2016_vote_share","trump_won","mask_requirement_detail","State_FIPS","State_Population","Pct_White_Non_Hispanic","Pct_Population_in_Poverty","Median_Household_Income","Pct_Population_No_Health_Insurance","date","fips","cases","deaths"])
##Drop all observations containing null values for any of the columns except for the maskreq_effective_date, effective, and enforcement columns
all_merge.head()##checkt the data out


# In[14]:


##Q3(A)
#create the variables: the total number of cases per 100,000 population (as of September 28)
all_merge = all_merge.assign(total_cases_per100k = all_merge["cases"]/all_merge["State_Population"]*100000)
all_merge.head()


# In[15]:


#create the variables: the total number of deaths per 100,000 population (as of September 28)
all_merge = all_merge.assign(total_deaths_per100k = all_merge["deaths"]/all_merge["State_Population"]*100000)
all_merge.head()


# In[16]:


#create the variables: takes on the value of 1 if a state has a statewide (or territory-wide) mask mandate, otherwise
see_diff_typies=pd.get_dummies(all_merge["mask_requirement_detail"])##form dummy variables by using "get_dummies"
see_diff_typies["m_mandate"]=see_diff_typies["Entire State"]+see_diff_typies["Entire Territory"]##form dummy variables of "m_mandate", which is the sum of "Entire State" and "Entire Territory" 
m_mandate=see_diff_typies.iloc[:,8:]## select the column of "m_mandate" only 
m_mandate.head()## look into "m_mandate" 


# In[17]:


##add "m_mandate"  to df
all_merge=pd.concat([all_merge,m_mandate],axis=1)
all_merge.head()


# In[18]:


#create the variables: equal to the number of days for which stay at home orders were in effect
all_merge["a"],all_merge["b"]=all_merge["effective"].str.split("-",1).str##split the the column of effective into two
all_merge.head()


# In[19]:


all_merge['a'].unique()##check the variables in "a" 


# In[20]:


all_merge['b'].unique()##check the variables in "b" , need to change  "Until lifted" into "9/28/2020"


# In[21]:


all_merge_1=all_merge.copy()##since string is unmutable, a new df is needed 
all_merge_1["b"]=all_merge["b"].str.replace("Until lifted", "9/28/2020")##replace "Until lifted" with "9/28/2020"
all_merge_1.head()##look into the data


# In[22]:


all_merge_1["a"]=pd.to_datetime(all_merge_1.a)## transfer the data in "a" into a datetime formate 
all_merge_1["b"]=pd.to_datetime(all_merge_1.b)## transfer the data in "b" into a datetime formate 
all_merge_1.head()##look into the data


# In[23]:


all_merge_1["n_days_1"]=all_merge_1["b"]-all_merge_1["a"]##calculate the days in between
all_merge_1.head()##look into the data


# In[24]:


all_merge_1.n_days_1.fillna(pd.Timedelta(seconds=0),inplace=True)##Convert the missing value of the time data to 0
all_merge_1.head()


# In[25]:


all_merge_2=all_merge_1.copy()##since string is unmutable, a new df is needed 


# In[26]:


all_merge_2["n_days_1"]=all_merge_1.n_days_1.astype("str").apply(lambda x:x[:-5]).astype("int32")##turn the data into int
all_merge_2.head()##look into "all_merge_2"


# In[27]:


all_merge_2["n_days"]=all_merge_2["n_days_1"]+1##add 1 for state had the order
all_merge_3=all_merge_2
all_merge_3["n_days"]=all_merge_2["n_days"].replace(1,0)##for those states do not have order, drop the 1 day record
all_merge_3.head()##check out the data


# In[28]:


all_merge_3=all_merge_3.drop(columns=["a","b","n_days_1"])##drop colums of "a" and "b"
all_merge_3.head()


# In[29]:


# Export "all_merge_2" as csv without index 
all_merge_3.to_csv("all_merge_3.csv",index=False)


# In[30]:


##Q3(B) Visualize the total number of cases and deaths per 100,000 population across all states. 
(ggplot(all_merge, aes(x='total_cases_per100k',y = 'total_deaths_per100k',color="state")) +
 geom_point()+
 labs(x = "total number of cases per 100,000",y="total number of deaths  per 100,000",title="number of cases and deathes across all states"))


# In[31]:


##Q3(C) Display the average length of stay at home orders and the median length (including states that didn’t implement any order). Additionally, find the state(s) that had the shortest stay-at-home orders among states that did implement an order.
##Display the average length of stay at home orders 
all_merge_2.n_days.mean()


# In[32]:


##Display the median length (including states that didn’t implement any order)
all_merge_2.n_days.median()


# In[33]:


## the state(s) that had the shortest stay-at-home orders among states that did implement an order
all_merge_3=all_merge_2.filter(["state","n_days"])## create a new df holding columns of "state" and "n_days" only
all_merge_3.sort_values("n_days",ascending=True).head(10)## Arrange the duration in descending order
##so the state of Alabama had the shortest stay-at-home orders of 27 days.


# In[34]:


##Q4(A) Compare the correlations of cases and deaths per 100,000 residents with the demographic variables contained in the state_ACS_data.csv file as well as the percentage of votes for Donald Trump. Briefly comment on any patterns you notice
all_merge_corr=all_merge_2.filter(["total_cases_per100k","total_deaths_per100k","State_Population","Pct_White_Non_Hispanic","Pct_Population_in_Poverty","Median_Household_Income","Pct_Population_No_Health_Insurance","trump_2016_vote_share"])##form a new df holding the needed variables 
all_merge_corr.head()##look into the data


# In[35]:


all_merge_corr.dtypes##check the data type of "all_merge_corr"


# In[36]:


all_merge_corr.trump_2016_vote_share.astype(str).str[:]##transfer the data type into string


# In[37]:


all_merge_corr["trump_2016_vote_share"]=all_merge_corr["trump_2016_vote_share"].str.strip("%").astype(float)/100##transfer the data type into float


# In[38]:


all_merge_corr.dtypes##check out the data type 


# In[39]:


all_merge_corr.head()##look into the data


# In[40]:


all_merge_corr.corr() ## Compare the correlations between variables
##Briefly comment:
##The population of states is positively correlated with the total cases per 100k and total deaths per 100k, the more population, the more cases and deaths.  Trump's 2016 vote share is negatively correlated with the total cases per 100k and total deaths per 100k, the more deaths and cases, the lower the vote share. What's more, the total deaths per 100k correlates more with vote share than the  total cases per 100k.


# In[42]:


##Q4(B) For the demographic variable that is most strongly correlated with deaths per 100,000 residents, create a scatterplot of this variable on the x-axis, against deaths per 100,000 on the y-axis. 
## "Pct_White_Non_Hispanic" is the variable that is most strongly correlated with deaths per 100,000 residents
### using Seaborn to draw the pic 
plt.figure(figsize=(12,6))
sns.scatterplot(x = "Pct_White_Non_Hispanic",y="total_deaths_per100k",
                alpha=.5,color="green",s=100,
                data = all_merge_corr)
plt.xlabel("Pct_White_Non_Hispanic")
plt.ylabel("Total Deaths per 100k")
plt.title("Pct_White_Non_Hispanic and Total Deaths per 100K")
plt.show()

