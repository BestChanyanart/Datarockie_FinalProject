# -*- coding: utf-8 -*-
"""Final Project .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T7yhKZopWRaJ4FodSMGd4cUuUZD64Lb6

# Project

# Final Project - Analyzing Sales Data

**Date**: 6 January 2022

**Author**: Chanyanart KiattipornOpas

**Course**: 'Pandas Foundation'

**Publish DataLore**: https://datalore.jetbrains.com/view/notebook/6Ajd7GdBq25EGV00wVpKT8
"""

# import data
import pandas as pd
df = pd.read_csv("sample-store.csv")

# preview top 5 rows
df.head()

# shape of dataframe
df.shape

# see data frame information using .info()
df.info()

"""We can use `pd.to_datetime()` function to convert columns 'Order Date' and 'Ship Date' to datetime."""

# example of pd.to_datetime() function
pd.to_datetime(df['Order Date'].head(), format='%m/%d/%Y')

# TODO - convert order date and ship date to datetime in the original dataframe
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')
df.head(5)

# TODO - count nan in postal code column
print( "Total NaN on Postal Code column: ", df['Postal Code'].isnull().sum() )

# TODO - filter rows with missing values
df[df['Postal Code'].isnull()]

# TODO - Explore this dataset on your owns, ask your own questions

# To look at Start and End date of this trannsaction (from 'Order Date' column)
print("Earliest date:", df['Order Date'].min() )
print("Lastest Date:", df['Order Date'].max() )

# How many Transaction days in this dataset? 
date_count = df['Order Date'].unique()
print("There are", len(date_count), "transaction days in this dataset." )

# To create new column of 'Year' from 'Order Date' 
df['year'] = pd.DatetimeIndex(df['Order Date']).year
df[['Order Date', 'year']].sample(5)

# How many customer in this dataset ? 
customer = df[[ 'Customer ID', 'Customer Name']].value_counts().reset_index()
print("There are", len(customer), "customers in this dataset.")

# Top5 customer who has transaction the most. "Loyal Customer"
customer.columns = ['Customer ID', 'Customer Name', 'Number of Transaction']
customer.head(5)

# Who is our Top Spender ? 
df.groupby(['Customer ID', 'Customer Name'])['Sales'].sum().sort_values(ascending = False).reset_index().head(5)

# Top 5 Cities where has transaction the most 
top_state = df[[ 'City', 'State']].value_counts().reset_index().head(5)
top_state.columns = ['City', 'State', 'Number of Transaction']
top_state

# Top Spender Cities 
df.groupby(['City', 'State'])['Sales'].sum().sort_values(ascending = False).reset_index().head(5)

# Total Sale by Category
df.groupby(['Category', 'Sub-Category'])['Sales'].agg(['sum','mean', 'std']).style.background_gradient()

# Profit generate by Category 
byProfit = df.groupby(['Category', 'Sub-Category'])['Profit'].agg(['sum'])
byProfit.style.background_gradient()

# Which Category need to be considered?

byProfit[ byProfit ['sum'] < 0 ]
# Comment: Tables, Bookcases and Supplies should be considered because they can't generate any profit.

# Which Category generate the highest profit? 
byProfit.sort_values('sum', ascending=False).head(5)

# Comment: Copiers is the category that generate highest profit.

"""## Data Analysis Part

Answer 10 below questions to get credit from this course. Write `pandas` code to find answers.
"""

# TODO 01 - how many columns, rows in this dataset
print("Number of rows and columns are", df.shape)

# TODO 02 - is there any missing values?, if there is, which colunm? how many nan values?
showNaN = df.isnull().sum()
showNaN[showNaN > 0]

# TODO 03 - your friend ask for `California` data, filter it and export csv for him
calfornia_data = df[ df['State'] == 'California' ]
calfornia_data.to_csv('california.csv', index=False)

# TODO 04 - your friend ask for all order data in `California` and `Texas` in 2017 (look at Order Date), send him csv file

# Filter only Texas and California State
by_state = df[ (df['State'] == 'California') | (df['State'] == 'Texas')]

# Filter only Year 2017 (between 2017-01-01 to 2017-12-31)
target_year_state = by_state[ (by_state['year'] == 2017) ]
target_year_state.sort_values('Order Date').head(3)

# Save to CSV 
target_year_state.to_csv('result.csv', index=False)

# TODO 05 - how much total sales, average sales, and standard deviation of sales your company make in 2017
year_2017 = df.query('year == 2017')

print("Total Sales in 2017:", year_2017['Sales'].sum() )
print("Average Sales in 2017:", year_2017['Sales'].mean() )
print("Standard Deviation of Sales in 2017:", year_2017['Sales'].std() )

# TODO 06 - which Segment has the highest profit in 2018
year_2018 = df.query('year == 2018')
year_2018.groupby('Segment')['Profit'].sum()

# Comment: 'Consumer' Segment has the highest profit in 2018

year_2018.groupby('Segment')['Profit'].sum().plot(kind='barh', color=['salmon', 'orange', 'gold']);

# TODO 07 - which top 5 States have the least total sales between 15 April 2019 - 31 December 2019

# Extract Sale time duration 
sale_between = df[ (df['Order Date'] >= '2019-04-15') & (df['Order Date'] <= '2019-12-31') ]
sale_between.sort_values('Order Date').head(3)

# Total Sales on every States
total_sales = sale_between.groupby('State')['Sales'].sum().reset_index()

# The 5 states which has the least Total Sales (between 15 April 2019 - 31 December 2019)
total_sales.sort_values('Sales').head(5)

# TODO 08 - what is the proportion of total sales (%) in West + Central in 2019 e.g. 25%

year_2019 = df.query('year == 2019')

sale_byRegion = year_2019.groupby('Region')['Sales'].sum().reset_index()
sale_byRegion

# to find Total Sales in Year 2019
total_sales_year2019 = year_2019['Sales'].sum()
print("Total Sales in Year 2019:", total_sales_year2019)

# To create Percent columns 
sale_byRegion['percent'] = (sale_byRegion['Sales'] / total_sales_year2019) * 100
sale_byRegion

# The proportion of Total Sales in West + Central region in Year 2019 
target = sale_byRegion.iloc[[0,3]]
print("The proportion of Sales in West + Central (2019): ", target['percent'].sum() )

# TODO 09 - find top 10 popular products in terms of number of orders vs. total sales during 2019-2020
year_19_20 = df.query('year == 2019 | year == 2020')

# Top 10 popular products in number of Order (top10_byOrder)
top10_byOrder = year_19_20.groupby( [ 'Sub-Category', 'Product Name'] )['Quantity', 'Sales']\
                    .sum().reset_index()\
                    .sort_values('Quantity',ascending=False)\
                    .head(10)
top10_byOrder

# Top 10 of highest total Sale product 
top10_bySales = year_19_20.groupby( [ 'Sub-Category', 'Product Name'] )['Quantity', 'Sales']\
                    .sum().reset_index()\
                    .sort_values('Sales',ascending=False).head(10)

top10_bySales

# To count the highest order by Category
df.groupby('Sub-Category')['Quantity'].sum().reset_index().sort_values('Quantity',ascending=False).head(10)

# TODO 10 - plot at least 2 plots, any plot you think interesting :)

# Total Sales by Region
df.groupby('Region')['Sales'].sum().plot(kind='barh', color=['yellow', 'gold', 'orange', 'brown']);

# Comment: It is clearly seen that 'West' region got the highest Sale among regions.

# Total Sales by Year
df.groupby('year')['Sales'].sum().plot(kind='barh');

# Comment: Year 2020 is the peak Sale year.

# The More you Sales, The More You Gain (Profit) ? 
df[['Sales', 'Profit']]\
    .plot(x='Sales', y='Profit', kind='scatter', color='orange');

# Comment: Most transaction are around 0 - 5000. There are a trends both gaining and losing the profit.

# The High number of ordering products(per transaction), The High profit ? , Is that true?
df[['Quantity', 'Profit']]\
    .plot(x='Quantity', y='Profit', kind='scatter', color='salmon');

# Comment: It look like not true. "Wholesale" (more than 10 pieces) does not gain high profit. Comparing the transaction that ordering between 2 - 8 pieces. (Retail) There are a larger range of gaining profit.

# TODO Bonus - use np.where() to create new column in dataframe to help you answer your own questions
import numpy as np

# If profit more than 0, it means that transaction got the profit. 
df['Sale status'] = np.where(df['Profit'] > 0, 'gain', 'loss')
df[['Profit', 'Sale status']].sample(5)

# Segmentation

# How long does it take of preparing the parcel? 
# To create new column of preparing product. 
df['prepare_product'] = (df['Ship Date'] - df['Order Date']).dt.days
df[['Ship Date', 'Order Date', 'prepare_product']].head(3)

df['prepare_product'].describe()

# If prepare the product more than 5 days means 'slow' and less than 3 day is 'fast'

# Create function
def transform_prepare_parcel(_prepareday): 
    if _prepareday < 3:
        return "Fast"
    elif _prepareday > 5:
        return "Slow"
    else:
        return "Normal"

# Apply function
df['prepare_status'] = df['prepare_product'].apply(transform_prepare_parcel)

df[['prepare_product', 'prepare_status']].sample(5)

df.groupby( ['Category'] )['prepare_status'].value_counts()