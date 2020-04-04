##!/usr/bin/python3

from lib.MarketDbIfc import MarketDbIfc
import json
from bson import json_util
from bottle import route, run, request, response


# method to create a new stock document. does not check if ticker already exists
@route('/stocks/api/v1.0/createStock/<ticker>', method='POST')
def post_create(ticker):
    req = json.loads(json.dumps(request.json, indent=4, default=json_util.default))
    req["Ticker"] = ticker
    if marketdb.stocks_coll.create_doc(req):
        response.status = '201 Created'
    else:
        req = {}
        response.status = '200 OK'
    return json.loads(json.dumps(req, indent=4, default=json_util.default))


# method to return full stock document based on ticker
@route('/stocks/api/v1.0/getStock/<ticker>', method='GET')
def get_read(ticker):
    result = marketdb.stocks_coll.read_doc({"Ticker": ticker})
    for r in result:
        response.status = '200 OK'
        return json.loads(json.dumps(r, indent=4, default=json_util.default))
    # if it gets here, result was empty, ticker not found
    response.status = '404 Not Found'
    return result


# method to update stock document
@route('/stocks/api/v1.0/updateStock/<ticker>', method='PUT')
def get_update(ticker):
    query = {"Ticker": ticker}
    new_value = request.json
    if marketdb.stocks_coll.update_doc(query, new_value):
        response.status = '201 Created'
        result = marketdb.stocks_coll.read_doc(query)
        for r in result:
            return json.loads(json.dumps(r, indent=4, default=json_util.default))
    else:
        response.status = '200 OK'
        return
        # if it gets here, no matching Ticker found
    response.status = '404 Not Found'
    return


# method to delete stock document
@route('/stocks/api/v1.0/deleteStock/<ticker>', method='DELETE')
def get_delete(ticker):
    query = {"Ticker": ticker}
    if marketdb.stocks_coll.delete_doc(query):
        response.status = '200 OK'
    else:
        response.status = '404 Not Found'
    return


#  method to get a list of stock documents matching posted ticker list
@route('/stocks/api/v1.0/stockReport', method='POST')
def stock_report():
    req = json.loads(json.dumps(request.json, indent=4, default=json_util.default))
    stocklist = req["list"]
    result = []
    for ticker in stocklist:
        for summary in marketdb.read_summary(ticker):
            result.append(summary)
    if len(result) == 0:
        # abort(404, "Not Found") - i want it to fail 'silently'
        response.status = '404 Not Found'
        return
    response.status = '200 OK'
    return json.dumps(result, indent=4, default=json_util.default)


# method to get a list of summary data from companies in a given industry
@route('/stocks/api/v1.0/industryReport/<industry>', method='GET')
def industry_report(industry):
    result = marketdb.read_industryreport(industry)
    if len(result) == 0:
        response.status = '404 Not Found'
        return
    response.status = '200 OK'
    return json.dumps(result, indent=4, default=json_util.default)


# method to funding information for a given company
@route('/stocks/api/v1.0/portfolio/<company>', method='GET')
def get_portfolio(company):
    result = marketdb.companies_coll.read_doc({"name": company}, {"_id": False, "name": 1, "investments": 1})
    portfolio = []
    for doc in result:
        portfolio.append(doc)
    if len(portfolio) == 0:
        response.status = '404 Not Found'
        return
    return json.dumps(portfolio, indent=4, default=json_util.default)


# MAIN
if __name__ == '__main__':
    # initialize MongoIfc instance
    marketdb = MarketDbIfc()

    # start listening for connections
    run(host='localhost', port=8080)
