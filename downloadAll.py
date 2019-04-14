from functions import signInWooValerie, downloadAllVariations, downloadAllProducts, downloadOneProduct, signInWooVyD,\
    changeProdFeature2FromDB, createDatabase
from functionsStock import downloadAllOrders, identifyVariations
import json
import os
import dataset  # https://github.com/pudo/dataset
import csv



wcapi = signInWooVyD()
nameDataBase = 'VyD0.db'
# downloadAllOrders(wcapi, nameDataBase)
downloadAllProducts(wcapi, nameDataBase)
downloadAllVariations(wcapi, nameDataBase)

'''
# For downloading one product


print(wcapi)
nameDataBase = 'VyD.db'
table = createDatabase(nameDataBase, tablename='Products')
print(table)
# changeProdFeature2FromDB(wcapi, table)
'''
'''
product=7275
downloadOneProduct(product,wcapi,1)
product=7180
downloadOneProduct(product,wcapi,1)
product=7918
downloadOneProduct(product,wcapi,1)
'''