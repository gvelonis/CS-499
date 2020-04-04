##!/usr/bin/python
# Python 2.7.6
# Probably works with python3 but codio doesn't have pymongo installed for it

import json
from bson import json_util
import bottle
from bottle import route, run, request, abort, response
import datetime
from pprint import pprint
from pymongo import MongoClient

#set mongodb connection variables
connection = MongoClient('localhost', 27017)
db = connection['market']
stocks_coll = db['stocks']
companies_coll = db['companies']

# set up URI paths for REST service
@route('/stocks/api/v1.0/createStock/<ticker>', method='POST')
def post_create(ticker):
  req = json.loads(json.dumps(request.json, indent=4, default=json_util.default))
  req["Ticker"] = ticker
  if create_document(req):
    response.status = '201 Created'
  else:
    req = {}
    response.status = '200 OK'
  return json.loads(json.dumps(req, indent=4, default=json_util.default))

@route('/stocks/api/v1.0/getStock/<ticker>', method='GET')
def get_read(ticker):
  result = read_document({"Ticker":ticker})
  for r in result:
    response.status = '200 OK' 
    return json.loads(json.dumps(r, indent=4, default=json_util.default))
  #if it gets here, result was empty, ticker not found
  response.status = '404 Not Found'
  return result

@route('/stocks/api/v1.0/updateStock/<ticker>', method='PUT')
def get_update(ticker):
  query = {"Ticker" : ticker}
  new_value = request.json
  if update_document(query, new_value):
    response.status = '201 Created'
    result = read_document(query)
    for r in result:
       return json.loads(json.dumps(r, indent=4, default=json_util.default))
  else:
    response.status = '200 OK'
    return 
  #if it gets here, no matching Ticker found
  response.status = '404 Not Found'
  return

@route('/stocks/api/v1.0/deleteStock/<ticker>', method='DELETE')
def get_delete(ticker):
  query = { "Ticker" : ticker }
  if delete_document(query):
    response.status = '200 OK'
  else:
    response.status = '404 Not Found'
  return

@route('/stocks/api/v1.0/stockReport', method='POST')
def stock_report():
  req = json.loads(json.dumps(request.json, indent=4, default=json_util.default))
  list = req["list"]
  result = []
  for ticker in list:
    for summary in read_summary(ticker):
      result.append(summary)
  if len(result) == 0:
    #abort(404, "Not Found") - i want it to fail 'silently'
    response.status = '404 Not Found'
    return
  response.status = '200 OK'
  return json.dumps(result, indent=4, default=json_util.default)

@route('/stocks/api/v1.0/industryReport/<industry>', method='GET')
def industry_report(industry):
  result = read_industryReport(industry)
  if len(result) == 0:
    response.status = '404 Not Found'
    return
  response.status = '200 OK'
  return json.dumps(result, indent=4, default=json_util.default)

@route('/stocks/api/v1.0/portfolio/<company>', method='GET')
def portfolio(company):
  result = companies_coll.find({"name":company}, {"_id":False, "name":1, "investments":1})
  portfolio = []
  for doc in result:
    portfolio.append(doc)
  if len(portfolio) == 0:
    response.status = '404 Not Found'
    return
  return json.dumps(portfolio, indent=4, default=json_util.default)

  
# BASIC FUNCTIONS FOR MONGO
# function to create a document
# argument is a document (dictionary with full set of key/value pairs)\
# returns True if success, False if failure
def create_document(document):
  try:
    stocks_coll.save(document)
  except Exception as e:
    print(e)
    return False
  return True

# function to read a document
# argument is a key/value lookup pair (dictionary with 1 key/value pair)
# returns list of documents matching the query
def read_document(query):
  try:
    result = stocks_coll.find(query)
  except Exception as e:
    return e
  return result

# function to update a document
# first argument is key/value pair to select the document
# second argument is key/value pair to update
# returns True if Success, False if fail
def update_document(query, newValue):
  try:
    result = stocks_coll.update_many(query, {'$set' : newValue} )
  except Exception as e:
    print(e)
    return False
  return True

# function to delete a document
# argument is a key/value lookup pair
# returns True if success, false if failure
def delete_document(query):
  result = stocks_coll.delete_many(query)
  if result.deleted_count == 0:
    return False
  return True

# ADVANCED MONGO FUNCTIONS
# import stock from file
# argument is a string - relative path to a json file
# returns True if success, false if failure
def import_stock(filename):
  print("Importing ", filename)
  return create_document(json.load(open(filename)))

# function to read only _id, ticker, and volume from a document
# argument is a string - Ticker for the desired stock
# returns a list of documents matching the ticker containing only _id, ticker, and volume
def read_volume(ticker):
  try:
    result = stocks_coll.find({"Ticker":ticker}, { "Ticker":1, "Volume":1})
  except Exception as e:
    return e
  return result

# function to read only ticker, company, sector, industry, price, and volume
def read_summary(ticker):
  try:
    result = stocks_coll.find({"Ticker":ticker}, { "_id": False, "Ticker":1, "Company":1, "Sector":1, "Industry":1, "Price":1, "Volume":1})
  except Exception as e:
    return e
  return result

# function to update stock
# arguments are a string - ticker of the stock and an integer - the new volume
# returns true if success, false if failure
def update_stock(ticker, volume):
  return update_document({"Ticker":ticker},{"Volume":volume})

# function to delete a stock
# argument is a string - ticker of the stock to delete
# returns true if success, false if failure
def delete_stock(sticker):
  return delete_document({"Ticker":ticker})

# function to count number of stocks with 50-day simple moving average between high and low
# arguments are two floats - the high and the low values
# returns integer
def read_hilo(high, low):
  try:
    result = stocks_coll.find({ "50-Day Simple Moving Average" : { "$lt" : high, "$gt" : low} })
  except Exception as e:
    return e
  return result.count()
  
# function to return tickers for companies matching given industry
# argument is a string - the industry to search for
# returns a list of tickers (strings)
def read_industry(industry):
  try:
    result = stocks_coll.find({ "Industry":industry }, { "Ticker" : 1 } )
  except Exception as e:
    return e
  tickers = []
  for doc in result:
    tickers.append(doc['Ticker'].encode("utf-8"))
  return tickers


# function to read top 5 by price, returns only ticker, company, industry, and price in a given industry
def read_industryReport(industry):
  pipeline = [
    {"$match" : { "Industry" : industry }},
    {"$sort" : {"Price":-1 }},
    {"$limit" : 5 },
    {"$project" : { "Ticker":1, "Company":1, "Industry":1, "Price":1 }},
  ]
  try:
    result = stocks_coll.aggregate(pipeline)
  except Exception as e:
    return e
  companies = []
  for doc in result:
    company = { "Ticker" : doc['Ticker'].encode("utf-8"),
               "Company" : doc['Company'].encode("utf-8"),
               "Industry" : doc['Industry'].encode("utf-8"),
               "Price" : doc['Price'] }
    companies.append(company)
  return companies

# function to return list of key/value pairs, key is industry value is total shares outstanding
# argument is a string - the sector to search for
# returns ???
def read_sectors(sector):
  pipeline = [
    {"$match" : { "Sector" : sector }},
    {"$project" : { "Industry" : 1, "Shares Outstanding" : 1 }},
    {"$group" : { "_id" : "$Industry", "sum" : { "$sum" : "$Shares Outstanding" }}}
  ]
  try:
    result = stocks_coll.aggregate(pipeline)
  except Exception as e:
    return e
  industries = []
  for doc in result:
    industry = { "Industry" : doc['_id'].encode("utf-8"), "Total Outstanding Shares" : doc['sum']}
    industries.append(industry)
  return industries
  
  
#MAIN
if __name__ == '__main__':
  #app.run(debug=True)
  action = ""
  while action != "q":
    print("\nWhat would you like to do?\n")
    print("x = execute server")
    print("i = insert stock from file")
    print("pv = print volume of stock")
    print("u = update volume of stock")
    print("d = delete stock")
    print("hilo = find number of stocks with 50-Day Simple moving average between high and low values")
    print("ind = print list of tickers in given industry")
    print("sec = print list of total oustanding shares in a given sector grouped by industry")
    print("q = quit")

    action = raw_input("\nEnter choice: ")
    
    if action == "x":
      run(host='localhost', port=8080)  
    
    elif action == "i":
      if import_stock("testStock.json"):
        print("Import successful.\n")
      else:
        print("Import failed.\n")
    
    elif action == "pv":
      ticker = raw_input("Enter ticker to read volume of: ")
      for doc in read_volume(ticker):
        pprint(doc)
    
    elif action == "u":
      ticker = raw_input("Enter ticker to update: ")
      volume = raw_input("Enter new value for Volume ")
      if update_stock(ticker, volume):
        print("Update successful.\n")
      else:
        print("Update failed.\n")
    
    elif action == "d":
      ticker = raw_input("Enter ticker to delete: ")
      if delete_stock(ticker):
        print("delete success\n")
      else:
        print("delete failed\n")
    
    elif action == "hilo":
      high = float(raw_input("Enter high 50-day simple moving average value: "))
      low = float(raw_input("Enter low 50-day simple moving average value: "))
      print(read_hilo(high, low))
    
    elif action == "ind":
      industry = raw_input("Enter Industry to search for: ")
      for doc in read_industry(industry):
        pprint(doc)
    
    elif action == "sec":
      sector = raw_input("Enter Sector to query: ")
      for doc in read_sectors(sector):
        pprint(doc)
    
    # secret function to get sample data in testStock.json, manually edited after to remove _id, and change ticker and date fields
    # elif action == "dumpOne":
    #   json.dump(stocks_coll.find_one(), open("testStock.json", 'w'), default=json_util.default)
    
    elif action == "q":
      break
      
    else:
      print("Invalid input, try again")
  
  print("thank you, come again")