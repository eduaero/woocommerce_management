from woocommerce import API
import os
import dataset
import json
import base64
from glob import glob
from time import sleep
# from pydrive.drive import GoogleDrive
# from pydrive.auth import GoogleAuth

def signInWooVyD(timeout=100):
    wcapi = API(
        url="",
        consumer_key="",
        consumer_secret="",
        wp_api=True,
        version="wc/v2",
        timeout=timeout,
        query_string_auth=True)
    return wcapi



def createDatabase(nameDataBase,tablename='Products'):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pathDb='sqlite:///'+dir_path+'\\'+nameDataBase
    db = dataset.connect(pathDb)
    table = db[tablename]
    return table

def downloadOneProduct(product,wcapi,toCsv=1,folder='OneProduct'):
    if(toCsv):
        file_name = folder+'\\'+'OneProduct%d.csv' % product
        file_pointer = open(file_name, "w")
    # print(wcapi.get("products").json())
    if (1):  # wp-json/wc/v2/products/<id>/variations
        # r=wcapi.get("products/%d" % product)
        while True:
          try:
            r = wcapi.get("products/%d" % product)
            print(r)
          except:
            print(' \n\n\n\n\nHA FALLADOOOOOOOO!!!!!!')
            continue
          break
        your_json = r.text
        parsed = json.loads(your_json)
        if (toCsv):
            file_pointer.write(json.dumps(parsed, indent=4))
        file = json.dumps(parsed, indent=4)
        file_json = json.loads(file)
        print(file_json)
        if (0):
            file_json = json.loads(file)
            for x in range(0, file_json.__len__()):
                #           print(file_json[x]['name'],file_json[x]['name'],file_json[x]['id'])
                print(file_json[x]['slug'])
                print(file_json[x]['cross_sell_ids'])
                for categories in file_json[x]['categories']:
                    print(categories['name'], categories['id'])
    return file_json

def changePrices(writeTable,wcapi,percentage):
    lenDb = writeTable.__len__()
    print(lenDb)
    for id in range(1, lenDb + 1):
        row = writeTable.find_one(id=id)
        print('Reading row %d out of %d' %(id ,lenDb))
        print(row)
        if row is not None:
            if (row['regular_price'] != ''):
                #price=getDecimals(float(row['regular_price'])*percentage,0.1,0.6)
                #writeTable.update(dict(id=id,regular_price_new_01_06=price),['id'])
                price = getDecimals(float(row['regular_price']) * percentage, 0.25, 0.75)
                print(price)
                writeTable.update(dict(id=id, regular_price_new = price), ['id'])
            else:
                print('No price!!!')

def changePriceByCategory(writeTable, wcapi, percentage):
    lenDb = writeTable.__len__()
    for id in range(1, lenDb + 1):
        row = writeTable.find_one(id=id)
        print('Reading row %d out of %d' %(id ,lenDb))

        if (row['regular_price'] != ''):
            #price=getDecimals(float(row['regular_price'])*percentage,0.1,0.6)
            #writeTable.update(dict(id=id,regular_price_new_01_06=price),['id'])
            price = getDecimals(float(row['regular_price']) * percentage, 0.25, 0.75)
            writeTable.update(dict(id=id, regular_price_new = price), ['id'])
        else:
            print('No price!!!')

def getDecimals(number,lim1,lim2):
    fractional = int(number)
    decimal = number - fractional
    if (lim1 < decimal < lim2):
        newNumber = fractional + 0.5
    if (lim2 <= decimal < 1):
        newNumber = fractional + 0.95
    if (decimal <= lim1):
       newNumber = fractional - 1 + 0.95
    return newNumber

def changeProdFeatureFromDB(wcapi,writeTable,varTable, varWC = 'product'):
    lenDb = writeTable.__len__()
    print(lenDb)
    for id in range(1,lenDb + 1):
    # for id in range(1, 2):
        while True:
          try:
            row = writeTable.find_one(id=id)
            print(row)
            if row is not None:
                if (varWC == 'product'):
                    idProd = row['prodID']
                else:
                    idSon = row['sonID']
                    idProd = row['prodID']

                #print(idProd)
                #print(type(idProd))
                value = ""

                newPrice = row[varTable]
                if(float(newPrice) ):
                    newPrice = '%4.2f' % newPrice

                #print(newPrice)
                #print(type(newPrice))
                if(newPrice):
                    print('Contador: %d Nombre: %s Producto: %s   Antiguo Precio: %s Nuevo Precio: %s' % (id, row['prodName'], idProd, row['regular_price'], newPrice))
                    # print('Contador: %d Producto: %s   Fb visibility: %s ' % (id, idProd, value,))
                    # data = {regular_price:newPrice}
                    data={}
                    data['regular_price'] = newPrice
                    if (varWC == 'product'):
                        str = "products/%s" % idProd
                    else:
                        str = "products/%s/variations/%d" % (idProd,idSon)
                    # print(str)
                    #else:
                    #    str = "products/%d" % idProd
                    #print('product')
                    # print(str)
                    # print(data)
                    print(wcapi.put(str, data).json())
                else:
                    print("Price = NULL")
          except:
            print(' \n\n\n\n\nHA FALLADOOOOOOOO!!!!!!')
            continue
          break

def changeProdFeature2FromDB(wcapi,writeTable):
    lenDb = writeTable.__len__()
    for id in range(37,37+200):
        row = writeTable.find_one(id=id)
        idProd=row['prodID']
        catID=row['catID0']
        not2hide=[152,156,157,155,153,143,144,142]
        print(id)
        if catID in not2hide:
            print('esta')
        else:
            print('no esta')
        #try:
            r = wcapi.get("products/%d" % idProd)
            your_json = r.text
            parsed = json.loads(your_json)
            print(parsed)
            try:
                for n in range(0,parsed['meta_data']):
                    data={}
                    if(parsed['meta_data'][n]['key'] == 'fb_visibility'):
                        id_fb_visibility=parsed['meta_data'][n]['key']
                        data['meta_data'] = []
                        data['meta_data'].append({'key': "fb_visibility", 'id': id_fb_visibility, 'value':""})
                str = "products/%d" % idProd
                print(str)
                print(data)
            except:
                continue

def changeProdFeatureFromContent(wcapi,writeTable,varWC,content):
    lenDb = writeTable.__len__()
    for id in range(1,lenDb + 1):
        while True:
          try:
            row = writeTable.find_one(id=id)
            idProd=row['prodID']
            print('Contador: %d Producto: %s  Nueva Variable: %s' %(id, idProd, content))
            data = {varWC:content}
            str = "products/%d" % idProd
            print(wcapi.put(str, data).json())
          except:
            print('\n\n\n\n\nHA FALLADOOOOOOOO!!!!!!')
            continue
          break

def getFolders(folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    dir_where = dir_path + '\\' + folder + '\\*\\'
    print(dir_where)
    prod_folders = glob(dir_where)
    print(prod_folders)
    print(len(prod_folders))
    return prod_folders

class NewProduct:
    '''OBJETO CREADO PARA SUBIR PRODUCTOS Y VARIACIONES A LA WEB'''
    def __init__(self):
        pass
    # def data2object(self, name='', slug='', price='', description='', shortDescription='', AllImages='',
    #             AllCategories='', AllSizes='', AllColours=''):
    def readFromCsv(self,folder, folder1='',VyD_Colaborations=True):
        '''     THE PRODUCT DATA IS READ FROM .CSV FILES AND UPLOAD TO THE OBJECT'''

        dataFile = '%s/%s/data.txt' % (folder, folder1)
        descriptionFile = '%s/%s/description.txt' % (folder, folder1)
        shortDescriptionFile = '%s/%s/shortDescription.txt' % (folder, folder1)
        nameTxtFile = '%s/%s/name.txt' % (folder, folder1)
        snippetFile= '%s/%s/snippet.txt' % (folder, folder1)
        nameTxt = open(nameTxtFile, 'w')
        with open(dataFile) as f:
            data = f.readlines()

        dataName = data[0].replace('\n', '')
        nameTxt.write(dataName)
        nameTxt.close()
        nameFilePointer = open(nameTxtFile, 'r', encoding="utf-8")
        name = nameFilePointer.read()
        slug = data[1].replace('\n', '')
        price = data[2].replace('\n', '')
        AllCategories = data[3].replace('\n', '')
        AllCategories = AllCategories.split(',')
        AllImages = data[4].replace('\n', '')
        AllImages = AllImages.split(',')
        palabrasClave=data[7].replace('\n', '')

        length = data.__len__()
        if length > 5:
            AllSizes = data[5].replace('\n', '')
            AllSizes = AllSizes.split(',')
            if length > 6:
                AllColours = data[6].replace('\n', '')
                AllColours = AllColours.split(',')
                #print(AllColours[1])
                #print(AllColours[1].encode('ascii'))
                #>> > encoded = base64.b64encode('data to be encoded')
                #print(base64.b64encode(AllColours[1]))
                #AllColours[1]=AllColours[1].encode("utf-8", "ignore")
                #print(AllColours[1])

            else:
                AllColours = []
        else:
            AllSizes = []
        print(descriptionFile)
        descriptionFilePointer = open(descriptionFile, 'r', encoding="latin-1")
        shortDescriptionPointer = open(shortDescriptionFile, 'r', encoding="latin-1")
        snippetPointer = open(snippetFile, 'r', encoding="utf-8")
        description = descriptionFilePointer.read()
        shortDescription = shortDescriptionPointer.read()
        snippet = snippetPointer.read()

        # We create an object with the characteristics of the new product
        self.name = name
        self.slug = slug
        self.price = price
        self.description = description
        self.shortDescription = shortDescription
        self.palabrasClave=palabrasClave
        self.snippet=snippet
        self.AllImages = []
        self.AllCategories = []
        self.AllSizes = []
        self.AllColours = []
        for x in range(len(AllImages)):
            self.AllImages.append(AllImages[x].replace(' ',''))
        for x in range(len(AllCategories)):
            self.AllCategories.append(AllCategories[x])
        for x in range(len(AllSizes)):
            self.AllSizes.append(AllSizes[x])
        for x in range(len(AllColours)):
            self.AllColours.append(AllColours[x])

    def upload_product(self, wcapi, pathWebImages, talla, colour,manage_stock=False,stock_quantity=2,toUpload=0,imagesProduct=False):
        product = {}
        product["name"] = self.name
        product["slug"] = self.slug
        # product["regular_price"] = self.price
        # product["in_stock"] = True
        product['description'] = self.description
        product['short_description'] = self.shortDescription


        product['categories'] = []
        product['meta_data']=json_yoast(self.palabrasClave,self.snippet)

        # Las imágenes pertenecen al producto
        x = 0

        product['images'] = []
        for str in self.AllImages:
            print(pathWebImages + str)
            product['images'].append({'src': pathWebImages + str, 'position': x})
            x = x + 1

        x = 0
        for str in self.AllCategories:
            product['categories'].append({'id': str})
            x = x + 1
            self.variable = 0  # Counter to know whether the product is variable or not

        variations = {}
        variations['attributes'] = []
        x=0
        if self.AllSizes:
            x=x+1
            product['attributes'] = []
            product['attributes'].append(
                {'id': talla, 'variation': 'True', 'visible': 'true','position': x, 'options': self.AllSizes})
            self.variable = 1 + self.variable
        if self.AllColours:
            x = x + 1
            variations['attributes'] = []
            product['attributes'].append(
                {'id': colour, 'variation': 'True', 'visible': 'true','position': x, 'options': self.AllColours})
            self.variable = 1 + self.variable
        # If there are no variations the product is simple. If there are variations the product is variable
        if (self.variable):
            product['type'] = 'variable'
        else:
            product['type'] = 'simple'

        self.json_product = product
        print(json.dumps(product, indent=4))
        if (toUpload):
            self.uploadProduct2web(wcapi)
        print('PREPARADO PARA PUBLICAR VARIACIONES')
        z=0

        for x in range(len(self.AllSizes)):
            for y in range(len(self.AllColours)):
                z=z+1 # created to organize the menu order
                print(self.AllSizes)
                print(self.AllColours)
                variations = {}
                variations['attributes'] = []
                variations['regular_price'] = self.price
                # variations['menu_order']=
                print(variations)
                variations['attributes'] = []
                if self.AllSizes:
                    variations['attributes'].append({'id': talla, 'option': self.AllSizes[x]})
                if self.AllColours:
                    variations['attributes'].append({'id': colour, 'option': self.AllColours[y]})
                print(variations['attributes'])
                variations['regular_price'] = self.price

                if (manage_stock):
                    variations['manage_stock'] = True
                    variations['stock_quantity'] = stock_quantity

                if(imagesProduct==True):
                    print('entra')
                    if(self.AllImages):
                        variations['image'] = {'src': pathWebImages + self.AllImages[y],'position': 0}
                        #variations['image'].append() # ,'name': self.AllImages[y] ,

                '''product['images'] = []
                for str in self.AllImages:
                    product['images'].append({'src': pathWebImages + str, 'position': x})
                    x = x + 1'''
                self.json_variation = variations
                print(variations)
                if (toUpload):  # UPLOAD THE VARIATIONS
                    self.uploadVariation2web(wcapi, self.new_prod_id)

    def uploadProduct2web(self,wcapi,time=3):
        # Subimos el producto
        print('\n\nSubiendo el PRODUCTO a la web\n\n')
        while True:
          try:
              print(self.json_product)
              r_out = wcapi.post("products", self.json_product).json()
              print(r_out)
              new_prod_id = r_out['id']
              self.new_prod_id = new_prod_id
              #print(wcapi.post("products", self.json_product).json())
              print('PRODUCTO SUBIDO CORRECTAMENTE     :)   :)')
          except:
            error=ValueError
            print('HA FALLADOOOOOOOO!')
            sleep(time)
            continue
          break


    def uploadVariation2web(self, wcapi,new_prod_id,time=3):
        # Subimos la variacion
        print('\n\nSubiendo la VARIACIÓN a la web\n\n')
        while True:
          try:
            print(self.json_variation)
            r_out_var=wcapi.post("products/%d/variations" % new_prod_id, self.json_variation).json()
            print(r_out_var)
            '''
            var_data2={'image': {'src': 'https://xn--visteydisea-beb.com/wp-content/uploads/Camiseta-mujer-roja-Jane.jpg'}}
            print(wcapi.put("products/13943/variations/13944", var_data).json())
            '''
            print('VARIACIÓN SUBIDA CORRECTAMENTE     :)   :)')
          except:
            print('HA FALLADOOOOOOOO!')
            sleep(time)
            continue
          break




def json_yoast(palabraClave,snippet,score=90):
    '''WE CREATE THE SEO DATA'''
    metadata=[]
    metadata.append({'id': 435340, 'key': '_yoast_wpseo_primary_product_cat','value': ''})
    metadata.append({'id': 435341, 'key': 'page_product_layout', 'value': 'inherit'})
    metadata.append({'id': 435342, 'key': 'page_product_youtube', 'value': ''})
    metadata.append({'id': 435343, 'key': 'product_full_screen_description_meta_box_check', 'value': 'off'})
    metadata.append({'id': 435344, 'key': '_wpb_vc_js_status', 'value': 'false'})
    metadata.append({'id': 435345, 'key': '_vc_post_settings', 'value': '{vc_grid_id: []}'})
    metadata.append({'id': 435350, 'key': '_yoast_wpseo_focuskw_text_input', 'value': palabraClave})
    metadata.append({'id': 435351, 'key':'_yoast_wpseo_focuskw' , 'value': palabraClave})
    metadata.append({'id': 435352, 'key': '_yoast_wpseo_metadesc', 'value': snippet})
    metadata.append({'id': 435353, 'key': '_yoast_wpseo_content_score', 'value': score})
    return metadata

def iniciar_gdrive():
    global drive

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

def descargar_csv():
    global drive
    # Initialize GoogleDriveFile instance with file id.
    stock_csv = drive.CreateFile({'id': 'ID_DEL_ARCHIVO'}) #id puede venir en la url
    stock_csv.GetContentFile('NOMBRE_DEL_ARCHIVO.csv') # Download file as 'NOMBRE_DEL_ARCHIVO.csv'.

'''def subir_csv(name='Stock_Drive.csv'):
    drive = GoogleDrive(gauth)
    stock_csv = drive.CreateFile()
    # Read file and set it as a content of this instance.
    stock_csv.SetContentFile(name)
    stock_csv.Upload() # Upload the file.
    print('title: %s, mimeType: %s' % (stock_csv['title'], stock_csv['mimeType']))'''


def downloadAllVariations(wcapi,nameDataBase):
    readTable = createDatabase(nameDataBase, tablename='Products')
    writeTable = createDatabase(nameDataBase, tablename='Variations')
    columns=readTable.columns
    col2db=[]
    for col in columns:
        if (col.startswith('catID')) | (col.startswith('catName')):
            col2db.append(col)
    variations2db=[]
    for col in columns:
        if (col.startswith('variations')):
            variations2db.append(col)
    #print(variations2db)
    lenDb=readTable.__len__()
    for id in range(1,lenDb+1):
        row=readTable.find_one(id=id)
        for col in col2db:
            print(col)
            #print(row['regular_price'])
        if(row['regular_price'].__len__()>=1): # Because some cells are empty but no NULL
            dataDb = dict(prodName=row['prodName'], prodID=row['prodID'])
            if (row[col] != ''):
                dataDb[col] = row[col]
                dataDb['parentID']=''
                dataDb['regular_price'] = row['regular_price']
                #print('regular_price',row['regular_price'])
                #print(row['prodID'])
                writeTable.insert(dataDb)
        else:
            for col in variations2db:
                if (row[col]):
                    dataDb = dict(parentID=row['prodID'])
                    idVariation=row[col]
                    try:
                        file_json = downloadOneProduct(idVariation, wcapi, 0)
                        dataDb['prodName'] = file_json['name']
                        dataDb['prodID'] = file_json['id']
                        dataDb['regular_price'] = file_json['regular_price']
                        for y in range(0, file_json['attributes'].__len__()):
                            dataDb['att_name%d' % y] = file_json['attributes'][y]['name']
                            dataDb['att_id%d' % y] = file_json['attributes'][y]['id']
                            dataDb['att_option%d' % y] = file_json['attributes'][y]['option']
                        writeTable.insert(dataDb)
                    except:
                        print('Trying again ...!')
                        sleep(time)
                        continue

        print(dataDb)


def downloadAllProducts(wcapi,nameDataBase):
    table=createDatabase(nameDataBase,tablename='Products')
    page=0
    while True:
        page=page+1
        str=("products?page=%d") % page

        try:
            r = wcapi.get(str)
            r_text = r.text
            parsed = json.loads(r_text)
            file = json.dumps(parsed, indent=4)
            file_json = json.loads(file)
            for x in range(0, file_json.__len__()):
                dataDb = dict(prodName=file_json[x]['name'], prodID=file_json[x]['id'],
                              regular_price=file_json[x]['regular_price'])
                for y in range(0, file_json[x]['categories'].__len__()):
                    # print(file_json[x]['categories'].__len__())
                    dataDb['catName%d' % y] = file_json[x]['categories'][y]['name']
                    dataDb['catID%d' % y] = file_json[x]['categories'][y]['id']
                for y in range(0, file_json[x]['variations'].__len__()):
                    dataDb['variations%d' % y] = file_json[x]['variations'][y]
                print(dataDb)
                table.insert(dataDb)
            print("PAGE %d READ PROPERLY" % page)
        except:
            print('Trying again ...!')
            sleep(time)
            continue


        if file_json.__len__()<10:
            break