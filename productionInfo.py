import sys
sys.path.insert(0,'/Projects/lite-excel/')
import numpy
import requests
import json

def main(sessionID, client):
    print("Kesim ve Mal Kabul Güncelleme Başladı. \n")

    # this part sends requests to NEBIM server and gets related data as JSON.
    link = """http://188.132.229.74:9090/(S("""
    linkcont = """))/IntegratorService/RunProc?{
        "ProcName": "sp_BPItemOrder",
        "Parameters": [
        {
        "Name": "StartDate",
        "Value": "2019-01-01"
        },
        {
        "Name": "EndDate",
        "Value": "2050-01-01"
        },
        {
        "Name": "ProcessCode",
        "Value": "BP"
        },
        {
        "Name": "CollectionCode1",
        "Value": "9K1"
        },
        {
        "Name": "CollectionCode2",
        "Value": "9Y2"
        },
        {
        "Name": "CollectionCode3",
        "Value": "9Y3"
        },
        {
        "Name": "CollectionCode4",
        "Value": "BAST"
        }
        ]
        }
        """
    print("Kesim ve Mal Kabul Sorguları NEBİM'den başarılı döndü. \n")

    productionInfoResponse = requests.get(link + sessionID + linkcont)
    productionInfo = json.loads(productionInfoResponse.text)
    refactoredArray = []

    for item in productionInfo:
        sku = item["ItemCode"]
        color = item["ColorDescription"]
        qty = item["Qty1"] - item["CancelQty1"]
        shipmentQty = item["ShipmentQty1"]
        isFound = False
        for element in refactoredArray:
            if element["Sku"]== sku and element["Renk"] == color:
                element["Kesim"] = element["Kesim"] + qty
                element["MalKabul"] = element["MalKabul"] + shipmentQty
                isFound = True
                break
        if isFound == False:
            refactoredArray.append({
                "Sku": sku,
                "Renk": color,
                "Kesim": qty,
                "MalKabul": shipmentQty
            })

    # this part processes json data to array of arrays using numpy.
    a = numpy.empty((5000, 4), dtype=object)
    a[:] = ''
    global index
    index = 0
    for item in refactoredArray:
        a[index][0] = item["Sku"]
        a[index][1] = item["Renk"]
        a[index][2] = item["Kesim"]
        a[index][3] = item["MalKabul"]

        index = index + 1

    # this part pastes gsheet with related data.

    sheet = client.open_by_key("1eELo_AJ7hFLWfXxbU3i87KxnEbOgdIU4vvKVpcxS3Wo").worksheet("Uretim")

    clear_cell_list = sheet.range("A2:D5000")
    for cell in clear_cell_list:
        cell.value = ""
    sheet.update_cells(clear_cell_list, value_input_option='USER_ENTERED')

    cell_list = sheet.range('A2:D' + str(index))
    for cell in cell_list:
        cell.value = a[(cell.row - 2)][(cell.col - 1)]
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')
    print("Kesim ve Mal Kabul Güncellendi. \n")