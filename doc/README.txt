Prerequisites:
mongod instance running on localhost
access control enabled
dba:dba in "admin" with roles "userAdminAnyDatabase", "readWriteAnyDatabase" and "dbAdminAnyDatabase"

Run scripts/init_mongo.sh to:
1) Drop/recreate market database
2) create unique index on ticker for stocks
3) create index on name for companies
4) import stocks collection
5) import companies collection
*Note: Applies to mongodb running on default port on localhost

Run MarketAPI.py to start ReST API, see Sample_API_calls.txt for examples

Run MarketCLI.py to interact with database through the command line

GV-7-1.py is the original design/database artifact, included for reference
GV-CS-200-Final3.py is the original algorithms/data structures artifact, included for reference