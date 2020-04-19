#!/bin/bash
# George Velonis

# drop all data from market db and create indices
mongo "mongodb://dba:dba@localhost/admin" < '.init_mongo.js'

# import sample data
mongoimport --username=dba --password=dba --authenticationDatabase=admin --db=market --collection=stocks --file='../data/stocks.json'
mongoimport --username=dba --password=dba --authenticationDatabase=admin --db=market --collection=companies --file='../data/companies.json'
