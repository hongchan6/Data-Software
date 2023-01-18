import unittest
import pandas as pd
from data import getSuburb, getPropertiesByKeywords, getPropertyList, analysisCleanliness, analysisProperties, displayPriceDistribution, viewPropertyDetail

class MyTestCase(unittest.TestCase):
    #1 Check the total number of suburb = 39
    def test_getSuburb(self):
        suburbs = getSuburb()
        self.assertEqual(39, len(suburbs))
  
    #2 Check the first option is All
    def test_getSuburbFirstOption(self):
        suburbs = getSuburb()
        self.assertEqual('All', suburbs[0])

    #3 Check if getPropertiesByKeywords returns at least a result
    def test_getPropertiesByKeywords(self):
        key = 'pool'
        filter = 'pool'
        self.assertIsNotNone(key, getPropertiesByKeywords(filter))

    #4 getPropertiesByKeywords should return a empty dataframe if there is no filter keywords
    def test_getPropertiesByKeywordsWithNone(self):
        df = getPropertiesByKeywords(None)
        self.assertEqual(0, df.shape[0])

    #5 getPropertyList should return all properties
    def test_getPropertyList(self):
        filter = ''
        suburb = ''
        dateFrom = ''
        dateTo = ''
        state = {
          'filter': filter,
          'suburb': suburb,
          'dateFrom': dateFrom,
          'dateTo': dateTo
        }
        prevState = state
        total = 36662
        self.assertEqual(total, getPropertyList(state, prevState).shape[0])
    
    #6 getPropertyList should return all properties in Sydney Suburb
    def test_getPropertyListInSydney(self):
        filter = ''
        suburb = 'Sydney'
        dateFrom = ''
        dateTo = ''
        state = {
          'filter': filter,
          'suburb': suburb,
          'dateFrom': dateFrom,
          'dateTo': dateTo
        }
        prevState = state
        total = 9241
        self.assertEqual(total, getPropertyList(state, prevState).shape[0])

    #7 getPropertyList should return all properties with Wifi as Keyword
    def test_getPropertyListWithWifi(self):
        filter = 'wifi'
        suburb = ''
        dateFrom = ''
        dateTo = ''
        state = {
          'filter': filter,
          'suburb': suburb,
          'dateFrom': dateFrom,
          'dateTo': dateTo
        }
        prevState = state
        total = 34198
        self.assertEqual(total, getPropertyList(state, prevState).shape[0])
    
    #8 getPropertyList should return all properties with Wifi as Keyword in Sydney
    def test_getPropertyListWithWifiInSydney(self):
        filter = 'wifi'
        suburb = 'Sydney'
        dateFrom = ''
        dateTo = ''
        state = {
          'filter': filter,
          'suburb': suburb,
          'dateFrom': dateFrom,
          'dateTo': dateTo
        }
        prevState = state
        total = 8000
        self.assertGreater(getPropertyList(state, prevState).shape[0], total)


    #9 getPropertyList should return all properties within a date range
    def test_getPropertyListWithDates(self):
        filter = ''
        suburb = ''
        dateFrom = '2018-12-07'
        dateTo = '2018-12-27'
        state = {
          'filter': filter,
          'suburb': suburb,
          'dateFrom': dateFrom,
          'dateTo': dateTo
        }
        prevState = state
        total = 36662
        self.assertEqual(total, getPropertyList(state, prevState).shape[0])

    #10 getPropertyList should return all properties within a date range + filter + suburb
    def test_getPropertyListWithWifiInSydneyWithDates(self):
        filter = 'wifi'
        suburb = 'Sydney'
        dateFrom = '2018-12-07'
        dateTo = '2018-12-27'
        state = {
          'filter': filter,
          'suburb': suburb,
          'dateFrom': dateFrom,
          'dateTo': dateTo
        }
        prevState = state
        total = 8000
        self.assertGreater(getPropertyList(state, prevState).shape[0], total)

    #11 analysisCleanliness should return all properties and labels even without filtered results passed in
    def test_analysisCleanlinessNoParams(self):
        mask, labels = analysisCleanliness(None)
        self.assertTrue(mask.value_counts().count() > 0)
        self.assertTrue(len(labels) > 0)

    #12 analysisCleanliness should return all properties and labels
    def test_analysisCleanlinessFilter(self):
        filteredResult = pd.DataFrame()
        mask, labels = analysisCleanliness(filteredResult)
        self.assertTrue(mask.value_counts().count() > 0)
        self.assertTrue(len(labels) > 0)

    #13 analysisProperties should return all properties and labels even without filtered results passed in
    def test_analysisPropertiesNoParams(self):
        series = analysisProperties(None)
        self.assertTrue(series.value_counts().count() > 0)

    #14 analysisProperties should return all properties and labels even without filtered results passed in
    def test_analysisProperties(self):
        filteredResult = pd.DataFrame()
        series = analysisProperties(filteredResult)
        self.assertTrue(series.value_counts().count() > 0)

    #15 displayPriceDistribution should return all properties and labels even without filtered results passed in
    def test_displayPriceDistributionNoParams(self):
        df = displayPriceDistribution(None)
        self.assertTrue(df.shape[0] > 0)

    #16 displayPriceDistribution should return all properties and labels even without filtered results passed in
    def test_displayPriceDistribution(self):
        filteredResult = pd.DataFrame()
        df = displayPriceDistribution(filteredResult)
        self.assertTrue(df.shape[0] > 0)
      
    #17 viewPropertyDetail should return the detail of the selected property
    def test_viewPropertyDetail(self):
        id = 1118675
        property = viewPropertyDetail(id)
        self.assertEqual(id, property['id'].values[0])

    #18 viewPropertyDetail should return empty series if property not found
    def test_viewPropertyDetailNotFound(self):
        id = 1
        property = viewPropertyDetail(id)
        self.assertTrue(property['id'].count() == 0)

if __name__ == '__main__':
    unittest.main()
