#!/usr/bin/env python
# coding: utf-8

# In[170]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore') # use to remove warning


# Load dataset

# In[171]:


df =pd.read_csv('hotel_bookings.csv')


# In[172]:


df.head()


# In[173]:


df.tail()


# Exploratory data analysis

# In[174]:


#Total number of rown and column
df.shape


# In[175]:


# Show all columns
df.columns


# In[176]:


df.info()


# In[177]:


# Convert datatypes in date_time types
df["reservation_status_date"]=pd.to_datetime(df['reservation_status_date'])


# In[178]:


df.info()


# In[179]:


df.describe() # this use only for numerical column 


# In[180]:


#Show only object values
df.describe(include='object')


# In[181]:


# Print object values
for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique()) #print unique value of objects
    print('-'*50) #use for sepration between two column and its value


# In[182]:


#Show number of null values
df.isnull().sum()


# In[183]:


#Drop column those have more missing value
df.drop(['company','agent'],axis=1,inplace = True)  #(inplace) use to update df after drop table 
# Use to remove missing value
df.dropna(inplace=True)


# In[184]:


df.isnull().sum()


# In[185]:


df=df[df['adr']<5000] #use that values which are less than 5000


# In[186]:


df.describe()


# Data Analysis and Visualization

# In[187]:


# Calculate cancel persentage
cancelled_perc =df['is_canceled'].value_counts(normalize = True) #(normalize is use to calculate percentage)
print(cancelled_perc)


# In[188]:


plt.figure(figsize=(4,3))
plt.title('Reservation status count')
plt.bar(["Not canceled",'Canceled'],df['is_canceled'].value_counts(),edgecolor='k',width=0.7)
plt.show()


# In[189]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x= 'hotel',hue = 'is_canceled',data=df,palette ='Blues')
legend_lebels,_=ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status in different hotels',size=20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')

plt.legend(['not canceled','canceled'])
plt.show()


# In[190]:


resort_hotel=df[df['hotel']== 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)


# In[191]:


city_hotel=df[df['hotel']== 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize =True)             


# In[192]:


resort_hotel= resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel= city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[193]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in city and Resort Hotel',fontsize=30)
plt.plot(resort_hotel.index, resort_hotel['adr'],label='Resort Hotel')
plt.plot(city_hotel.index,city_hotel['adr'],label='City Hotel')
plt.legend(fontsize=20)
plt.show()


# In[194]:


# Reservation and cancellation a/c to month
df['month']=df['reservation_status_date'].dt.month #use to create a column of month
plt.figure(figsize=(16,8))
ax1 =sns.countplot(x='month',hue= 'is_canceled',data=df ,palette= 'bright')
legend_labels,_=ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month',size=20)
plt.xlabel('month')
plt.ylabel('number of reservation')
plt.legend(['not canceled','canceled'])
plt.show()


# In[195]:


plt.figure(figsize=(15,8))
plt.title('ADR ( Average daily rate) per month',fontsize= 25)
sns.barplot(x='month',y='adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# In[196]:


# Cancellation based on top 10 country
cancelled_data =df[df['is_canceled']==1]
top_10_country =cancelled_data['country'].value_counts()[:10] #[:10] use to show 10 vales only
plt.figure(figsize=(8,8))
plt.title('Top 10 countries with reservation canceled')
plt.pie(top_10_country,autopct= '%.2f',labels=top_10_country.index) #(%.2f) print two value after decimal
plt.show()


# In[197]:


df['market_segment'].value_counts()


# In[198]:


df['market_segment'].value_counts(normalize=True)


# In[199]:


# Cancelled data of market_segment
cancelled_data['market_segment'].value_counts(normalize=True)


# In[200]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

not_cancelled_data = df[df['is_canceled']==0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

plt.figure(figsize =(20,6))
plt.title('Average daily rate')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label='cancelled')
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label='not cancelled')
plt.legend()


# In[201]:


# Use specific data 2016-17
cancelled_df_adr=cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016')&(cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr=not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016')&(not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[202]:


plt.figure(figsize =(20,6))
plt.title('Average daily rate')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label='cancelled')
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label='not cancelled')
plt.legend(fontsize=20)
plt.show()

