library(DBI)
con <- dbConnect(RSQLite::SQLite(), "C:\\Users\\as857sb\\Documents\\Python Scripts\\VyD\\VyD.db")

orders <- dbReadTable(con, "Orders")
products <- dbReadTable(con, "Products")
variations <- dbReadTable(con, "Variations")
variations2 <- dbReadTable(con, "variations2")

changeprice <- function(products,catName, catID, price) {
  where <- ((products[,catName] == catID)&(!is.na(products[,"regular_price"])))
  where[is.na(where)] <- FALSE
  products[where,"regular_price_new"] <- price 
  print(unique( products[,"regular_price_new"]))
  return(products)
}




!is.na(products[,"catID1"])
# products[((products[,"catID1"] == 85)&(!is.na(products[,"regular_price"]))),"regular_price_new"] <- 8.95   # Delantal
products <- changeprice(products, catName = "catID1", catID = 85, price = 8.95)
# products[products[,"prodID1"] == 2587,"regular_price_new"] <- 10.95   # Delantal denim
products <- changeprice(products, catName = "prodID", catID = 2587, price = 10.95)
# products[products[,"catID0"] == 110,"regular_price_new"] <- 2.95  # Mochila cuerdas
products <- changeprice(products, catName = "catID0", catID = 110, price = 2.95)
#products[products[,"catID0"] == 107,"regular_price_new"] <- 4.5   # Camiseta mujer
products <- changeprice(products, catName = "catID0", catID = 107, price = 4.5)
#products[products[,"catID0"] == 108,"regular_price_new"] <- 4.95 # Camiseta hombre
products <- changeprice(products, catName = "catID0", catID = 108, price = 4.95)
#products[products[,"catID0"] == 118,"regular_price_new"] <- 5.5 # Camiseta gym h
products <- changeprice(products, catName = "catID0", catID = 118, price = 5.5)
#products[products[,"catID0"] == 119,"regular_price_new"] <- 5.95# Camiseta gym m
products <- changeprice(products, catName = "catID0", catID = 119, price = 5.95)
#products[products[,"catID0"] == 106,"regular_price_new"] <- 4.5 # nadador
products <- changeprice(products, catName = "catID0", catID = 106, price = 4.5)
#products[products[,"catID0"] == 116,"regular_price_new"] <- 5.5 # cuello pico
products <- changeprice(products, catName = "catID0", catID = 116, price = 5.5)

#products[products[,"catID0"] == 117,"regular_price_new"] <- 4.95 # cuello pico M
products <- changeprice(products, catName = "catID0", catID = 117, price = 4.95)

#products[products[,"catID0"] == 109,"regular_price_new"] <- 4.5 # nadador
products <- changeprice(products, catName = "catID0", catID = 109, price = 7.95)



products[is.na(products)] <- ""

colnames(variations2)[colnames(variations2) == "sonID"] <- "prodID"
colnames(variations2)[colnames(variations2) == "prodID"] <- "parentID"
variations <- variations[!(variations[,"prodID"] == ""),]
variations.prices <- merge(variations,products[,c("prodID","regular_price_new")],
                           by = "prodID", all.x = TRUE)
# dbWriteTable(con, "Products", products, overwrite=TRUE)

# dbWriteTable(con, "variations2", variations, overwrite=TRUE)

View(cbind(products[,c("prodID","regular_price","catID0","catName0" ,
                       "prodName"   ,       
                       "catName1"   ,       "catID1","regular_price_new")]))
