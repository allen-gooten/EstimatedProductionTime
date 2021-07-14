
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 11:01:22 2021
@company: Gooten
@author: allen
"""
# Import Libraries
import pandas as pd
import numpy as np
import math
import datetime
import matplotlib.pyplot as plt
from scipy import stats

# Load in data file
plt.close("all")
file = "Data/Production Days Data 2020.csv"
df = pd.read_csv(file, header=0, low_memory=False)

#  DataFrame pre-processing
# 1. Reduce dataframe
# 2. Convert date columns to datetime
# 3. Remove nan values 
df.iloc[:,7:10] = df.iloc[:,7:10].apply(pd.to_datetime, errors='coerce', utc=True)
df = df[['VENDOR_ID', 'CATEGORY_ID','PRODUCT_ID','SKU_ID','IN_PRODUCTION_DATE','SHIP_DATE']]
df.dropna(inplace=True)
df = df.sort_values(by='IN_PRODUCTION_DATE')

# Calculate Production Days: Ship Date - In Production Date
df['PRODUCTION_DAYS'] = (df['SHIP_DATE'] - df['IN_PRODUCTION_DATE']).astype('timedelta64[D]')

# Group data by Vendor and Product
df['VenProd'] = df.iloc[:,[0,2]].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

# Filter by Date Range
df_filter = df.loc[(df['IN_PRODUCTION_DATE']>="2021-01-05") & (df['IN_PRODUCTION_DATE']<="2021-01-22")]

# Filter by particular VenProd
filter_param = "3_43"
vp = df_filter.query('VenProd == "' + filter_param +'"')

# General Analysis of Filter VenProd
print("############ VenProd = " + filter_param + " ################")
print(vp['PRODUCTION_DAYS'].describe())
fig, axs = plt.subplots(2)
plt.figure(figsize=(8,8))
axs[0].hist(vp['PRODUCTION_DAYS'])

# Calculate Z Score and filter out the outliers
vp['Z_SCORE'] = vp.groupby('VenProd')['PRODUCTION_DAYS'].transform(lambda x: (x-x.mean())/x.std()).abs()
vp = vp[vp['Z_SCORE'] < 3]
print("############ Filtered Outliers ################")
print(vp['PRODUCTION_DAYS'].describe())
axs[1].hist(vp['PRODUCTION_DAYS'])

UpperLim = math.ceil(vp['PRODUCTION_DAYS'].mean()+2*vp['PRODUCTION_DAYS'].std())
vp['TEST'] = vp['PRODUCTION_DAYS'].between(0,UpperLim)
print("############ Orders with Production Days less than ", UpperLim ," ################")
print(vp['TEST'].value_counts(normalize=True)*100)


'''
# Export Dataframe to a CSV file
compression_opts = dict(method='zip',archive_name='out.csv')
df.to_csv("output.zip", index=False, compression=compression_opts)
'''
