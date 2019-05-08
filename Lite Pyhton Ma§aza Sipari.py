import csv
import gspread
import numpy
from oauth2client.service_account import ServiceAccountCredentials
import time
import schedule
import requests
import json


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
    itemWsOrder = itemInfo.json()
    

    #this part processes json data to array of arrays using numpy. 
    a = numpy.empty((5000,7), dtype = object)
    a[:] = ''
    global index
    index = 0
    for item in itemWsOrder:
        a[index][0] = item["ItemCode"]
        a[index][1] = item["ColorDescription"]
        a[index][2] = item["Web Sipariş Miktarı"]
        a[index][3] = item["Mağaza Sipariş Miktarı"]
        index = index + 1

    #this part pastes gsheet with related data.
    sheet = client.open_by_key("1eELo_AJ7hFLWfXxbU3i87KxnEbOgdIU4vvKVpcxS3Wo").worksheet("Magaza Siparis")
    cell_list = sheet.range('A2:G' + str(index))
    for cell in cell_list:
        cell.value = a[(cell.row-1)][(cell.col-1)]
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')


#schedule the task for every hour
updateLİteExcel()
schedule.every().hour.do(updateLİteExcel, "productInfo updated.")

print("scheduled")

while True:
    schedule.run_pending()
    time.sleep(60)


    
