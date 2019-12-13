import sys
sys.path.insert(0,'/Projects/lite-excel/')
import numpy
import requests
import json

def main(sessionID, client):
    print("Mağaza satış adetleri güncelleme başladı. \n")
    # this part sends requests to NEBIM server and gets related data as JSON.
    link = """http://188.132.229.74:9090/(S("""
    linkcont = """))/IntegratorService/RunProc?{
        "ProcName": "sp_ItemStoreOrderInfo",
        "Parameters": [
        {
        "Name": "StartDate",
        "Value": "2019-07-01"
        },
        {
        "Name": "EndDate",
        "Value": "2050-04-16"
        }
        ]
        }

        """
    itemStoreOrders = requests.get(link + sessionID + linkcont)
    itemStoreOrder = json.loads(itemStoreOrders.text)
    print("Mağaza satış adetleri sorgusu NEBİM'den başarılı döndü. \n")
    # this part processes json data to array of arrays using numpy.
    a = numpy.empty((5000, 15), dtype=object)
    a[:] = ''
    global index
    index = 0
    for item in itemStoreOrder:
        a[index][0] = item["ItemCode"]
        a[index][1] = item["ColorDescription"]
        a[index][2] = item["Web Sipariş Miktarı"]
        a[index][3] = item["Mağaza Sipariş Miktarı"]

        index = index + 1

    # this part pastes gsheet with related data.

    sheet = client.open_by_key("1eELo_AJ7hFLWfXxbU3i87KxnEbOgdIU4vvKVpcxS3Wo").worksheet("Magaza Siparis")

    clear_cell_list = sheet.range("A2:D5000")
    for cell in clear_cell_list:
        cell.value = ""
    sheet.update_cells(clear_cell_list, value_input_option='USER_ENTERED')

    cell_list = sheet.range('A2:D' + str(index))
    for cell in cell_list:
        cell.value = a[(cell.row - 2)][(cell.col - 1)]
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
    print("Mağaza satış adetleri güncellendi. \n")