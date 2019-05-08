import numpy
import requests

def main(sessionID, client):

    # this part sends requests to NEBIM server and gets related data as JSON.
    link = """http://188.132.229.74:9090/(S("""
    linkcont = """))/IntegratorService/RunProc?{
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
        },
        {
        "Name": "CollectionCode3",
        "Value": "9Y1"
        }
        ]
        }

        """
    itemStoreOrders = requests.get(link + sessionID + linkcont)
    itemStoreOrder = itemStoreOrders.json()

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
    cell_list = sheet.range('A2:G' + str(index))
    for cell in cell_list:
        cell.value = a[(cell.row - 1)][(cell.col - 1)]
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')