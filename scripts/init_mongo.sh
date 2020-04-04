#!/bin/bash
# George Velonis

# drop all data from market db and create indices
mongo < '.init_mongo.js'

# import sample data
mongoimport --db=market --collection=stocks --file='../data/stocks.json'
mongoimport --db=market --collection=companies --file='../data/companies.json'
