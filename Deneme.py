import csv
import gspread
import numpy
from oauth2client.service_account import ServiceAccountCredentials
import time
import schedule
import requests
import json

#SKU - RENK RAPORU

def updateLİteExcel():
    ##This part authorizes gsheet 
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    ##those are the request links for NEBIM
    link2 = "http://188.132.229.74:9090/IntegratorService/connect"
    link3= "http://188.132.229.74:9090/(S("
    link3cont = "))/IntegratorService/getUserInfo"
    link4 = """http://188.132.229.74:9090/(S("""
    link4cont = """))/IntegratorService/RunProc?{
     "ProcName": "sp_OnlyItemAndColor",
     "Parameters": [
     {
     "Name": "CollectionCode1",
     "Value": "9Y3"
        },
        {
     "Name": "CollectionCode2",
     "Value": "9Y2"
      }
      ]
      }
      """


    ##creates a session and sends the requests. saves responses to related json objects.
    s = requests.Session()
    connect = s.post(link2)
    connectResponse = connect.json()
    print(connectResponse)
    sessionID = connectResponse["SessionID"]
    print(sessionID)

    connectionInfo = s.post(link3 + sessionID + link3cont)
    connectionInfoResponse = connectionInfo.json()
    print(connectionInfoResponse)

   
    itemInfo = s.get(link4 + sessionID + link4cont)
    itemInfoResponse = itemInfo.json()



    #this part processes json data to array of arrays using numpy. 
    a = numpy.empty((5000,15), dtype = object)
    a[:] = ''
    global index
    index = 0
    for item in itemInfoResponse:
        a[index][0] = item["ItemCode"]
        a[index][1] = item["ColorDesc"]
        index = index + 1
    
    return itemInfoResponse

#MAĞAZA SİPARİŞ RAPORU    
def updateOrderStoreLİteExcel():
    ##This part authorizes gsheet 
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    ##those are the request links for NEBIM
    link2 = "http://188.132.229.74:9090/IntegratorService/connect"
    link3= "http://188.132.229.74:9090/(S("
    link3cont = "))/IntegratorService/getUserInfo"
    link4 = """http://188.132.229.74:9090/(S("""
    link4cont = """))/IntegratorService/RunProc?{
    "ProcName": "sp_ItemStoreOrderInfo",
    "Parameters": [
    {
    "Name": "StartDate",
    "Value": "2019-01-01"
    },
    {
    "Name": "EndDate",
    "Value": "2050-04-16"
    },
    {
    "Name": "CollectionCode1",
    "Value": "9Y3"
""    },
    {
    "Name": "CollectionCode2",
    "Value": "9Y2"
    }
    ]
    }
    
    """
    ##creates a session and sends the requests. saves responses to related json objects.
    s = requests.Session()
    connect = s.post(link2)
    connectResponse = connect.json()
    print(connectResponse)
    sessionID = connectResponse["SessionID"]
    print(sessionID)

    connectionInfo = s.post(link3 + sessionID + link3cont)
    connectionInfoResponse = connectionInfo.json()
    print(connectionInfoResponse)

   
    itemStoreOrders = s.get(link4 + sessionID + link4cont)
    itemStoreOrder = itemStoreOrders.json()
    

    #this part processes json data to array of arrays using numpy. 
    a = numpy.empty((5000,15), dtype = object)
    a[:] = ''
    global index
    index = 0
    for item in itemStoreOrder:
        a[index][0] = item["ItemCode"]
        a[index][1] = item["ColorDescription"]
        a[index][2] = item["Web Sipariş Miktarı"]
        a[index][3] = item["Mağaza Sipariş Miktarı"]   
        index = index + 1
    return itemStoreOrder

#MERKEZ SİPARİŞ RAPORU
def updateOrdersLİteExcel():
    ##This part authorizes gsheet 
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

    ##those are the request links for NEBIM
        link2 = "http://188.132.229.74:9090/IntegratorService/connect"
        link3= "http://188.132.229.74:9090/(S("
        link3cont = "))/IntegratorService/getUserInfo"
        link4 = """http://188.132.229.74:9090/(S("""
        link4cont = """))/IntegratorService/RunProc?{
        "ProcName": "sp_ItemOrderInfo",
        "Parameters": [
        {
        "Name": "StartDate",
        "Value": "2019-01-01"
        },
        {
        "Name": "EndDate",
        "Value": "2050-04-16"
        },
        {
        "Name": "OfficeCode",
        "Value": "M"
        },
        {
        "Name": "CollectionCode1",
        "Value": "9Y3"
        },
        {
        "Name": "CollectionCode2",
        "Value": "9Y2"
        }
        ]
        }
        
        """
        ##creates a session and sends the requests. saves responses to related json objects.
        s = requests.Session()
        connect = s.post(link2)
        connectResponse = connect.json()
        print(connectResponse)
        sessionID = connectResponse["SessionID"]
        print(sessionID)

        connectionInfo = s.post(link3 + sessionID + link3cont)
        connectionInfoResponse = connectionInfo.json()
        print(connectionInfoResponse)

       
        itemOrder = s.get(link4 + sessionID + link4cont)
        itemOrder = itemOrder.json()
        

        #this part processes json data to array of arrays using numpy. 
        a = numpy.empty((5000,15), dtype = object)
        a[:] = ''
        global index
        index = 0
        for item in itemOrder:
            a[index][0] = item["ItemCode"]
            a[index][1] = item["ColorDescription"]
            a[index][2] = item["Sipariş Miktarı"]
            a[index][3] = item["Merkez-Ihracat Depo Envanter"]
            index = index + 1
        return itemOrder
            
skuRenk = updateLİteExcel()
siparisStok = updateOrdersLİteExcel()
magaza = updateOrderStoreLİteExcel()

for item in siparisStok:
    sku = item["ItemCode"]
    renk = item["ColorDescription"]
    siparis = item["Sipariş Miktarı"]
    stok = item["Merkez-Ihracat Depo Envanter"]
    for anaItem in skuRenk:
        anaSku = anaItem["ItemCode"]
        anaRenk = anaItem["ColorDesc"]
        if sku == anaSku and anaRenk == renk:
            anaItem["Siparis"] = siparis
            anaItem["Envanter"] = stok
            break
        
for item in magaza:
   sku = item["ItemCode"]
   renk = item["ColorDescription"]
   websiparis = item["Web Sipariş Miktarı"]
   magazasiparis = item ["Mağaza Sipariş Miktarı"]
   for anaItemM in skuRenk:
       skuM = anaItemM["ItemCode"]
       renkM = anaItemM["ColorDesc"]
       if sku == skuM and renk == renkM:
           anaItemM["Web Sipariş Miktarı"] = websiparis
           anaItemM["Mağaza Sipariş Miktarı"] = magazasiparis
           break


#this part pastes gsheet with related data.
sheet = client.open_by_key("1eELo_AJ7hFLWfXxbU3i87KxnEbOgdIU4vvKVpcxS3Wo").worksheet("test")
cell_list = sheet.range('A2:H' + str(index))
for cell in cell_list:
     cell.value = a[(cell.row-1)][(cell.col-1)]
sheet.update_cells(cell_list, value_input_option='USER_ENTERED')

schedule.every().hour.do(updateLİteExcel, updateOrderStoreLİteExcel, updateOrdersLİteExcel)  

print("*")
print(skuRenk)
print("*")

#schedule the task for every hour
while True:
    schedule.run_pending()
    time.sleep(60)

    
