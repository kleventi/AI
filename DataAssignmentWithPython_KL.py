###### Final Assignment Python Data - Leventi Konstantina ######
# Liquor Sales Analysis
# Project Overview:
# We are provided with a dataset detailing Liquor Sales in Iowa, USA, spanning the years 2012-2020.
# The tasks at hand are, for the timeframe 2016-2019:
# Discern the most popular item in each zipcode and
# Compute the sales percentage per store (in dollars).

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read data file
df = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')

# Filter records only between 2016 - 2019
df['date'] = pd.to_datetime(df['date'])
filtered_df = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2019)].reset_index()

# Check for missing values
print(filtered_df.info())
# No missing values found, so no need to deal with them (e.g. drop respective lines or fill empty fields with data)

### Task 1 - Discern the most popular item in each zipcode

# Group data by zip code and item number and then sum the number of sold bottles
bottles_sold = filtered_df.groupby(['zip_code','item_number'])['bottles_sold'].sum().reset_index()

# Find them most popular bottles per zip code
index = bottles_sold.groupby('zip_code')['bottles_sold'].idxmax()
most_popular_bottles = bottles_sold.loc[index].reset_index()

# Cast zip code to integer, so that I can display items properly in the bar chart
most_popular_bottles["zip_code"] = most_popular_bottles["zip_code"].astype(int)

# Sort values in descending order and keep only the highest 30 (the rest of the values are very low and cause 'noise' in the chart)
sorted_values = most_popular_bottles.sort_values(by='bottles_sold', ascending=False).head(30)


# Plot results
plt.figure('Task 1 - Most popular items in each zipcode (30 zip codes)', figsize=(10,6))
p = plt.bar(sorted_values['zip_code'].astype(str), sorted_values['bottles_sold'])
plt.bar_label(p)
plt.xlabel('Zip Code')
plt.ylabel('Sold Bottles')
plt.title('Most popular bottles per zip code (30 zip codes)')
plt.xticks(rotation=45)
plt.show()


### Task 2 - Compute the sales percentage per store (in dollars)

# Use only the records between 2016 - 2019 and sum the amount of sales (dollars) for each store.
sales_per_store = filtered_df.groupby('store_name')['sale_dollars'].sum()

# Total sales is the sum of the sales for all stores.
total_sales = sum(filtered_df['sale_dollars'])

# The percentage is calculated by the formula: (storeSales / totalSales)*100
sales_ratio = (sales_per_store / total_sales)*100

# Sort values and keep only the highest 30 (the rest of the values are very low and cause 'noise' in the chart)
sorted_sales_ratio = sales_ratio.sort_values(ascending=False).head(30)

# Plot results
plt.figure('Task 2 - Sales percentage per store (30 stores)', figsize=(10,6))
p = plt.barh(sorted_sales_ratio.index, sorted_sales_ratio.values, height=0.7)
plt.title("%Sales per store (30 stores)")
plt.xlabel("%Sales", fontsize=10)
plt.bar_label(p, fmt="%.2f")
plt.xlim([0,20])
plt.show()