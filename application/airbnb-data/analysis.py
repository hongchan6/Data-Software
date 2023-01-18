import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

listings = pd.read_csv('listings_dec18.csv', header=0)
listingSummaryDf =pd.read_csv("listings_summary_dec18.csv")
# reviewsDf =pd.read_csv("reviews_dec18.csv")

# read all the reference data
# calenderDf =pd.read_csv("calendar_dec18.csv")
# listingSummaryDf =pd.read_csv("listings_summary_dec18.csv")
# neighbourhoodsDf =pd.read_csv("neighbourhoods_dec18.csv")
# reviewsSummaryDf =pd.read_csv("reviews_summary_dec18.csv")

# print(calenderDf.shape)
# 13381265, 4

# print(listingsDf.shape)
# 36662, 96

#print(reviewsDf.shape)
# (446708, 6)

# print(listingsDf['id'].isin(calenderDf['listing_id'].value_counts()))
#36662

####################### analyse how many customers comment on cleanliness ###########################
# cleanFilter = reviewsDf.loc[reviewsDf['comments'] == 'clean']
# mask = reviewsDf['comments'].str.contains('clean', case=False, na=False)
# print(reviewsDf[mask].shape)
#(112310, 6)
# make a pie chart showig percentage?


####################### find top 10 scores ###########################
# top_10 = (listingsDf.groupby(['review_scores_value'])['id'].count().sort_values(ascending=False).head(10))
# print(top_10)


# suburbFilter = listings.loc[listings['neighbourhood'] == 'Glebe']
# top10 = pd.DataFrame({
#     'id':suburbFilter['id'],
#     'name': suburbFilter['name'],
#     'Suburb': suburbFilter['neighbourhood'],
#     'rating': suburbFilter['review_scores_value']
# })
# ratingCounts = top10.sort_values(by='rating',ascending=False).head(10)
# print(ratingCounts)

# def findTop10(suburb):
#     suburbFilter = listings.loc[listings['neighbourhood'] == suburb]
#     top10 = pd.DataFrame({
#         'id':suburbFilter['id'],
#         'name': suburbFilter['name'],
#         'Suburb': suburbFilter['neighbourhood'],
#         'rating': suburbFilter['review_scores_value']
#         })
#
#     ratingCounts = top10.sort_values(by='rating',ascending=False).head(10)
#     return ratingCounts

####################### distribution of prices ###########################

df = pd.DataFrame(listingSummaryDf)

name = df['neighbourhood']
price = df['price'].replace("[$,]", "", regex=True)

# df['price'] = pd.to_numeric(df['price'])

plt.bar(name, price)
plt.title("Price Distribution")
plt.xlabel("Suburb")
plt.xticks(rotation=90)
plt.ylabel("Price ($)")
plt.show()

# Join 3 csv files to one df
# concate_listing = pd.concat([calenderDf, listingsDf, listingSummaryDf])

# print(concate_listing['listing_id'], concate_listing['id'].head())
# print(concate_listing.dtypes)
# print(concate_listing[lisitng_id])

cancellationPolicy = listings['cancellation_policy'].value_counts()
plt.title("cancellationPolicy", x = 0.5, fontsize = 16)
outL = plt.pie(cancellationPolicy, labels = cancellationPolicy.index, autopct='%.2f')
circle = plt.Circle((0,0), 0.3, color='white')
donut = plt.gcf()
donut.gca().add_artist(circle)
plt.show()

#########bar#################
# fig, ax = plt.subplots()
# plt.figure(figsize=(15,15))
# counts = listings['cancellation_policy'].value_counts()
# term = counts.index
#
# ax.bar(term, counts, label=counts.index)
# ax.set_ylabel('Counts for each Policy')
#
#
# plt.show()
