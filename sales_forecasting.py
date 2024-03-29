# -*- coding: utf-8 -*-
"""Sales Forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/IshantWadhwa4/Finance-Analytics/blob/master/Sales_Forecasting.ipynb

# Sales Forecasting

## Table of Contents

1.   [Problem Statement](#Section1)
2.   [Basic EDA](#Section2)
3.   [Pre-Modeling](#Section3)
4.   [Modeling](#Section4)
5.   [Post Modeling](#Section5)
6.   [ML Interpretation | Explaninable AI](#Section6)
7.   [Model Deployment | MLOps](#Section7)
8.   [Create Dashbord](#Section8)

## 1. Problem Statement

**<h4>Business Scenario:</h4>**

- A multinational retail corporation named **The Shopper's Depot** operates a chain of hypermarkets, discount department stores, and grocery stores all around the world.

- The company is planning to open some additional stores in different regions and the management wants to **predict** the **future sales** of these stores and the **factors affecting** the sales numbers.

- This will help them in allocating a **budget** to each store according to the amount of mechanical and human resources required in the stores and setting up the **supply chain** and **inventory** systems.

- One challenge of modeling retail data is the need to make decisions based on **limited history**.

- As a result, the company has assigned its Data Science division the task to make the **department-wide sales forecast** for each store.

- The **target feature** is the **Weekly_Sales** column which shows the **sales** for the given department in the given store for a particular week.

## 2.Data Collection

| Column | Description |
| :--:| :--: |
| **Store** | The store number. |
| **Dept** | The department number. |
| **Date** | The week |
| **Weekly_Sales** | Sales for the given department in the given store. |
| **IsHoliday** | Whether the week is a special holiday week. |
| **Temperature** | Average temperature in the region. |
| **Fuel_Price** | Cost of fuel in the region. |
| **MarkDown1** | Anonymized data related to promotional markdowns that **The Shopper's Depot** is running. |
| **MarkDown2** | Anonymized data related to promotional markdown. |
| **MarkDown3** | Anonymized data related to promotional markdowns. |
| **MarkDown4** | Anonymized data related to promotional markdowns. |
| **MarkDown5** | Anonymized data related to promotional markdowns. |
| **CPI** | The consumer price index. |
| **Unemployment** | The unemployment rate. |
| **Type** | Type of the store. |
| **Size** | Size of the store. |
"""

import pandas as pd
DataUrl = 'https://raw.githubusercontent.com/insaid2018/Domain_Case_Studies/master/Retail/Data/weekly_sales_data.csv'
data = pd.read_csv(DataUrl)

data.shape

data.head()

data.info()
# date datatype
#markdown1 to 5 has null values

data.describe()
# find relation b/w weekly sales and temp --> Graph
# find relation b/w weekly sales and Fuel_Price --> Graph

data.groupby('Store').count()['Dept']
# number of department in each store

# how many null and zeros value
def get_number_zeros_null(df):
  '''
       LIb : need pandas lib for this function.

       Input : Only required dataframe for which you want zeros and null for each column
       Output: dataframe with number of zeros and null
  '''
  null_zero_dict={ }
  null_zero_dict['Number_of_nulls'] = df.isnull().sum()
  null_zero_dict['Number_of_zeros'] = (df==0).astype(int).sum()
  return pd.DataFrame(null_zero_dict).T

get_number_zeros_null(data)

# Tasks solution
# date datatype
# in first experiment i will replace null with zero

# date datatype
def convert_dateTime(df,column_list):
  for col in column_list:
    df[col] = pd.to_datetime(df[col])
  return df

data = convert_dateTime(data,['Date'])

# In first experiment i will replace null with zero
def replace_null_columns(df,list_columns):
  for col in list_columns:
      df[col].fillna(0,inplace=True)
  return df

replace_null_columns(data,['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5'])

"""## 3. Visualization"""

import seaborn as sns
import matplotlib.pyplot as plt

def get_numeric_data_columns(df):
  '''
      return list of all numeric data columns name
  '''
  return list(df._get_numeric_data().columns)

def get_catagorical_data_columns(df):
  '''
      return list of all catagoric data columns name
  '''
  return list(set(df.columns) - set(df._get_numeric_data().columns))

def draw_countPlot_grid(df):
  import math
  fig=plt.figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
  list_columns = get_catagorical_data_columns(df)
  n_rows = math.ceil(len(list_columns)/3)
  n_cols = 3
  for i, var_name in enumerate(list_columns):
    if len(df[var_name].unique()) < 8:
      ax=fig.add_subplot(n_rows,n_cols,i+1)
      sns.countplot(x = var_name, data=df)
      ax.set_title(var_name)
  fig.tight_layout()  # Improves appearance a bit.
  plt.show()

draw_countPlot_grid(data)
# alittle disbalance data in type c

from random import randint
def draw_distributionPlot_grid(df):
  import math
  fig=plt.figure(num=None, figsize=(12, 15), dpi=80, facecolor='w', edgecolor='k')
  list_columns = get_numeric_data_columns(df)
  n_rows = math.ceil(len(list_columns)/3)
  n_cols = 3
  colors = []
  for i in range(n_rows*n_cols):
    colors.append('#%06X' % randint(0, 0xFFFFFF))
  for i, var_name in enumerate(list_columns):
    ax=fig.add_subplot(n_rows,n_cols,i+1)
    sns.distplot(df[var_name],hist=True,axlabel=var_name,color=colors[i])
    ax.set_title(var_name)
  fig.tight_layout()  # Improves appearance a bit.
  plt.show()

draw_distributionPlot_grid(data)
# weekly sales is right skew on few days the sale is very high may b holydays
# q: find relation b/w holiday and weekly sales
# q: on holiday which store has max sale in wich departament
# how temp/fuleprice affect the sales

# relation b/w each
def heatmap_allcolumns(df):
  fig, ax = plt.subplots(figsize=(10,10))
  sns.heatmap(data=df.corr(),annot=True, cmap="Blues", ax=ax)

heatmap_allcolumns(data)

import numpy as np

def create_seaborn_heatmap_highcorelated(df,posThreshold,negThreshold):
  '''
      create Heatmap for highly co-related(given threshold) columns

      Input: dataframe, positive threshold, negitive threshold
      Plot: Heatmap
  '''
  df_corr = df.corr()
  tempdf = df_corr[(df_corr > posThreshold) | (df_corr < -negThreshold)]
  tempdf.replace(to_replace=1,value=np.nan,inplace=True)
  tempdf.dropna(axis=1,how='all',inplace=True)
  tempdf.dropna(axis=0,how='all',inplace=True)
  sns.heatmap(tempdf,annot=True, cmap="Blues")

create_seaborn_heatmap_highcorelated(data,0.6,0.6)
# There is no good relation

# Feature engg.
data['Month'] = data['Date'].dt.month

#list of question for EDA
# q: find relation b/w holiday/Date and weekly sales
# q: on holiday which store has max sale in which departament
# q: how petrol price and weekly sales are related
# q which store sell max with which department
# q: relation between temp and department and store
# q: relation b/w cpm size and unemployment

# Q :Is the Size of the Store related to the Type of the Store?
data_type = data[['Type','Size']].drop_duplicates()
data.groupby(['Type','Size']).count().index

plt.figure(figsize=(8, 8))
sns.boxplot(data=data, x='Type', y='Size', palette='winter', width=0.8)
plt.xlabel('Type', fontsize=14)
plt.ylabel('Size', fontsize=14)
plt.title('Relationship Between the Size and Type of the Store', fontsize=16)

# Yes there is relation b/w size and type

# Does the Larger Sized Stores have Higher Weekly Sales?

data.groupby('Type')['Weekly_Sales'].sum()

plt.figure(figsize=(8, 8))
sns.boxplot(data=data, x='Type', y='Weekly_Sales', width=0.8, showfliers=False)
plt.xlabel('Type', fontsize=14)
plt.ylabel('Weekly Sales', fontsize=14)
plt.title('Relationship Between the Weekly Sales and Type of the Store', fontsize=16)

# Is there a Strong Positive Correlation between the Size and the Weekly Sales of a Store?
plt.figure(figsize=(8, 8))
sns.scatterplot(x='Size',y='Weekly_Sales',data=data,hue='Type')
plt.title('Relationship Between the Weekly Sales ,Type of the Store and size', fontsize=16)

#How does each Store perform on the basis of Weekly Sales?
plt.figure(figsize=(19, 7))
sns.boxplot(x='Store',y='Weekly_Sales',data = data,hue='Type',showfliers=False)

#  Do the Holidays impact the Weekly Sales of the Stores?