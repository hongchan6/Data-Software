from re import sub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# calendar = pd.read_csv('airbnb-data/calendar_dec18.csv', header=0)

def getSuburb():
  neighbourhoods = pd.read_csv('airbnb-data/neighbourhoods_dec18.csv', header=0)
  new_row = pd.DataFrame({ 'neighbourhood_group': '' , 'neighbourhood': 'All'}, index =[0])
  neighbourhoods = pd.concat([new_row, neighbourhoods]).reset_index(drop = True)
  return neighbourhoods[['neighbourhood']].unstack().values.tolist()

def getPropertiesByKeywords(filter):
  listings = pd.DataFrame()
  if not filter:
    return listings
  listings = pd.read_csv('airbnb-data/listings_dec18.csv', header=0)
  result = listings[(listings['amenities'].str.contains(filter, case=False)==True) | (listings['name'].str.contains(filter, case=False)==True) | (listings['description'].str.contains(filter, case=False)==True)]
  return result

def getPropertyList(state, prevState):
  filter = state['filter']
  suburb = state['suburb']
  dateFrom = state['dateFrom']
  dateTo = state['dateTo']
  listingsSummary = pd.read_csv('airbnb-data/listings_summary_dec18.csv', header=0)
  result = listingsSummary

  if dateFrom and dateTo and (dateFrom != prevState['dateFrom'] or dateTo != prevState['dateTo']):
    listingsByDate = pd.read_csv('airbnb-data/calendar_dec18.csv', header=0)
    mask = (listingsByDate['date'] >= dateFrom) & (listingsByDate['date'] < dateTo)
    listingsByDate = listingsByDate.loc[mask]
    listingsByDate = listingsByDate.drop_duplicates(subset=["listing_id"])
    result = listingsSummary[listingsSummary['id'].isin(listingsByDate['listing_id'])]
  
  if (filter):
    # Filter
    print('filter')
    listings = getPropertiesByKeywords(filter)
    result = result[result['id'].isin(listings['id'])]
    # result = listingsSummary
  if suburb and suburb != 'All':
    # propertyList = listingsSummary.values
    print('with suburb', suburb)
    result = result[result['neighbourhood'].isin([suburb])]
  return result

def analysisCleanliness(filteredResult: pd.DataFrame):
  csvData = pd.read_csv("airbnb-data/reviews_dec18.csv", header=0)
  if isinstance(filteredResult, pd.DataFrame) and filteredResult.shape[0] > 0:
    csvData = csvData[csvData['listing_id'].isin(filteredResult['id'])]
  mask = csvData['comments'].str.contains('dirty|smelly|unclean|messy|dust|dusty|disgusting', case=False, na=False)
  labels = ['not dirty', 'dirty']
  return (mask, labels)

def analysisProperties(filteredResult: pd.DataFrame):
  csvData = pd.read_csv('airbnb-data/listings_dec18.csv', header=0)
  if isinstance(filteredResult, pd.DataFrame) and filteredResult.shape[0] > 0:
    csvData = csvData[csvData['id'].isin(filteredResult['id'])]
  cancellationPolicy = csvData['cancellation_policy'].value_counts()
  return cancellationPolicy

def displayPriceDistribution(filteredResult: pd.DataFrame):
  csvData = pd.read_csv("airbnb-data/listings_summary_dec18.csv", header=0)
  if isinstance(filteredResult, pd.DataFrame) and filteredResult.shape[0] > 0:
    csvData = csvData[csvData['id'].isin(filteredResult['id'])]
  return csvData

def viewPropertyDetail(id):
  if not id:
    return pd.Series()
  listings = pd.read_csv('airbnb-data/listings_dec18.csv', header=0).fillna('n/a')
  result = listings[listings['id'] == id]
  return result


