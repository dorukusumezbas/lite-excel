import sys
sys.path.insert(0,'/Projects/lite-excel/')
import numpy
import requests
import json

def main(sessionID, client):
    print("Toptan satış adetleri güncelleme başladı. \n")
    link = """http://188.132.229.74:9090/(S("""
    linkcont = """))/IntegratorService/RunProc?{
        "ProcName": "sp_ItemOrderInfo",
        "Parameters": [
        {
        "Name": "StartDate",
        "Value": "2019-07-01"
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
        "Value": "9K1"
        },
        {
        "Name": "CollectionCode4",
        "Value": "BAST"
        }
        ]
        }

        """
    itemOrder = requests.get(link + sessionID + linkcont)
    itemOrderResponse = json.loads(itemOrder.text)
    print("Toptan satış adetleri sorgusu NEBİM'den başarılı döndü. \n")
    # this part processes json data to array of arrays using numpy.
    a = numpy.empty((5000, 15), dtype=object)
    a[:] = ''
    global index
    index = 0
    for item in itemOrderResponse:
        a[index][0] = item["ItemCode"]
        a[index][1] = item["ColorDescription"]
        a[index][2] = item["Sipariş Miktarı"]
        a[index][3] = item["Merkez-Ihracat Depo Envanter"]
        index = index + 1

    # this part pastes gsheet with related data.
    sheet = client.open_by_key("1eELo_AJ7hFLWfXxbU3i87KxnEbOgdIU4vvKVpcxS3Wo").worksheet("Siparis")

    clear_cell_list = sheet.range("A2:D5000")
    for cell in clear_cell_list:
        cell.value = ""
    sheet.update_cells(clear_cell_list, value_input_option='USER_ENTERED')

    cell_list = sheet.range('A2:D' + str(index))
    for cell in cell_list:
        cell.value = a[(cell.row - 2)][(cell.col - 1)]
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
    print("Toptan satış adetleri güncellendi.\n")