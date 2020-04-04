// drop market db to ensure it starts clean
use market
db.runCommand({dropDatabase:1})

// create unique index for Ticker in stocks collection
// create index for name in Companies collection
use market
db.stocks.createIndex({"Ticker":1},{unique:true})
db.companies.createIndex({"name":1})
exit