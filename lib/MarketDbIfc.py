##!/usr/bin/python3

from lib.MongoIfc import MongoIfc
import json


class MarketDbIfc:
    # declare global variables
    stocks_coll = None
    companies_coll = None

    # initialize connection to market db, stocks and companies collection
    # two instances of MongoIfc class, one for each collection
    def __init__(self):
        self.stocks_coll = MongoIfc('market', 'stocks')
        self.companies_coll = MongoIfc('market', 'companies')

    # import stock from file
    # argument is a string - relative path to a json file
    # returns True if success, false if failure
    def import_stock(self, filename):
        print("Importing ", filename)
        return self.stocks_coll.create_doc(json.load(open(filename)))

    # function to read only _id, ticker, and volume from a document
    # argument is a string - Ticker for the desired stock
    # returns a list of documents matching the ticker containing only _id, ticker, and volume
    # list length will expected to be one due to unique index on Ticker field
    def read_volume(self, ticker):
        try:
            result = self.stocks_coll.read_doc({"Ticker": ticker}, {"Ticker": 1, "Volume": 1})
        except Exception as e:
            print(e)
            return e
        return result

    # function to read only ticker, company, sector, industry, price, and volume
    # argument is a string matching Ticker
    # returns list of documents with summary data for matching Ticker
    # list length will expected to be one due to unique index on Ticker field
    def read_summary(self, ticker):
        try:
            result = self.stocks_coll.read_doc({"Ticker": ticker},
                                               {"_id": False, "Ticker": 1, "Company": 1, "Sector": 1,
                                                "Industry": 1, "Price": 1, "Volume": 1})
        except Exception as e:
            return e
        return result

    # function to update stock
    # arguments are a string - ticker of the stock and an integer - the new volume
    # returns true if success, false if failure
    def update_stock(self, ticker, volume):
        return self.stocks_coll.update_doc({"Ticker": ticker}, {"Volume": volume})

    # function to delete a stock
    # argument is a string - ticker of the stock to delete
    # returns true if success, false if failure
    def delete_stock(self, ticker):
        return self.stocks_coll.delete_doc({"Ticker": ticker})

    # function to count number of stocks with 50-day simple moving average between high and low
    # arguments are two floats - the high and the low values
    # returns integer
    def read_hilo(self, high, low):
        try:
            result = self.stocks_coll.read_doc({"50-Day Simple Moving Average": {"$lt": high, "$gt": low}})
        except Exception as e:
            return e
        return result.count()

    # function to return tickers for companies matching given industry
    # argument is a string - the industry to search for
    # returns a list of tickers (strings)
    def read_industry(self, industry):
        try:
            result = self.stocks_coll.read_doc({"Industry": industry}, {"Ticker": 1})
        except Exception as e:
            return e
        tickers = []
        for doc in result:
            tickers.append(doc['Ticker'].encode("utf-8"))
        return tickers

    # function to read top 5 by price, returns only ticker, company, industry, and price in a given industry
    # argument is a string - the industry to search for
    # returns a list of documents with company data
    def read_industryreport(self, industry):
        pipeline = [
            {"$match": {"Industry": industry}},
            {"$sort": {"Price": -1}},
            {"$limit": 5},
            {"$project": {"Ticker": 1, "Company": 1, "Industry": 1, "Price": 1}},
        ]
        try:
            result = self.stocks_coll.aggregate(pipeline)
        except Exception as e:
            return e
        companies = []
        for doc in result:
            company = {"Ticker": doc['Ticker'].encode("utf-8"),
                       "Company": doc['Company'].encode("utf-8"),
                       "Industry": doc['Industry'].encode("utf-8"),
                       "Price": doc['Price']}
            companies.append(company)
        return companies

    # function to return list of key/value pairs, key is industry value is total shares outstanding
    # argument is a string - the sector to search for
    # returns list of documents with industry name and total outstanding shares
    def read_sectors(self, sector):
        pipeline = [
            {"$match": {"Sector": sector}},
            {"$project": {"Industry": 1, "Shares Outstanding": 1}},
            {"$group": {"_id": "$Industry", "sum": {"$sum": "$Shares Outstanding"}}}
        ]
        try:
            result = self.stocks_coll.aggregate(pipeline)
        except Exception as e:
            return e
        industries = []
        for doc in result:
            industry = {"Industry": doc['_id'].encode("utf-8"), "Total Outstanding Shares": doc['sum']}
            industries.append(industry)
        return industries
