from functions import *

writeNameDb = 'VyD.db'
writeTable = createDatabase(writeNameDb, tablename='variations2')
wcapi = signInWooVyD() # We initiate session
print(writeTable)
# Run to crete new prices, being the new_price=percentage*regular_price
#percentage=0.86
#changePrices(writeTable, wcapi, percentage)


varTable = 'regular_price_new'
varWC = 'regular_price'
# changeProdFeatureFromDB(wcapi,writeTable,varTable,varWC)

content='<p>Los descuentos por cantidad se aplican en el carrito</p>\n'
# varWC='short_description'
changeProdFeatureFromDB(wcapi, writeTable, varTable , varWC = 'variation')