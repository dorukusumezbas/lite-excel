import numpy
import requests
import json

def main(sessionID, client):

    link = """http://188.132.229.74:9090/(S("""
    linkProducts = """))/IntegratorService/RunProc?{
    "ProcName": "sp_OnlyItemAndColor",
    "Parameters": [
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

    linkKunye = """))/IntegratorService/RunProc?{
    "ProcName": "sp_ItemInfo",
    "Parameters": [
    {
    "Name": "CollectionCode1",
    "Value": "9Y3"
    },
    {
    "Name": "CollectionCode2",
    "Value": "9Y1"
    },
    {
    "Name": "CollectionCode3",
    "Value": "9Y2"
    }
    ]
    }
    """
    #pulls sku-renk
    itemInfo =requests.get(link + sessionID + linkProducts)
    itemInfoResponse = json.loads(itemInfo.text)

    #pulls künye
    kunye = requests.get(link + sessionID + linkKunye)
    kunyeResponse = json.loads(kunye.text)

    #counts asorti, adds AsortiCount prop to kunye json
    for item in kunyeResponse:
        asorti = item["LotDesc"]
        asortiList = asorti.split("-")
        asortiCount = len(asortiList)
        item["AsortiCount"] = asortiCount

    # this part processes json data to array of arrays using numpy. - SKU & Asorticount
    b = numpy.empty((5000,2), dtype=object)
    b[:] = ''
    global secondIndex
    secondIndex = 0
    for item in kunyeResponse:
        b[secondIndex][0] = item["ItemCode"]
        b[secondIndex][1] = item["AsortiCount"]
        secondIndex = secondIndex + 1

    #this part reads sipariş amounts from gsheet

    worksheet = client.open_by_key("1nodf_m9xd7jRcRRIx_CvS3VNjNTUAau_mpz7dTUfzFY").worksheet("Sipariş-Üretim")
    values = worksheet.get_all_values()
    for row in values:
        rowSku = row[0]
        rowRenk = row[1]
        rowKesimAdetSeri = row[6]
        rowNot = row[11]
        for item in itemInfoResponse:
            sku = item["ItemCode"]
            renk = item["ColorDesc"]
            if sku == rowSku and renk == rowRenk:
                item["SeriKesimAdet"] = rowKesimAdetSeri
                item["Not"] = rowNot

    # this part processes json data to array of arrays using numpy.
    a = numpy.empty((5000, 15), dtype=object)
    a[:] = ''
    global index
    index = 0
    for item in itemInfoResponse:
        a[index][0] = item["ItemCode"]
        a[index][1] = item["ColorDesc"]
        try:
            a[index][2] = item["SeriKesimAdet"]
        except KeyError:
            print("keyerror")
        try:
            a[index][3] = item["Not"]
        except KeyError:
            print("keyerror")
        index = index + 1

    clear_cell_list3 = worksheet.range("A5:B5000")
    for cell in clear_cell_list3:
        cell.value = " "
    worksheet.update_cells(clear_cell_list3, value_input_option='USER_ENTERED')

    cell_list3 = worksheet.range("A5:B" + str(index + 5))
    for cell in cell_list3:
        cell.value =  a[(cell.row - 5)][(cell.col - 1)]
    worksheet.update_cells(cell_list3, value_input_option='USER_ENTERED')

    clear_cell_list4 = worksheet.range("G5:G5000")
    for cell in clear_cell_list4:
        cell.value = " "
    worksheet.update_cells(clear_cell_list4, value_input_option='USER_ENTERED')

    cell_list4 = worksheet.range("G5:G" + str(index + 5))
    for cell in cell_list4:
        cell.value =  a[(cell.row - 5)][(cell.col - 5)]
    worksheet.update_cells(cell_list4, value_input_option='USER_ENTERED')

    clear_cell_list5 = worksheet.range("L5:L5000")
    for cell in clear_cell_list5:
        cell.value = " "
    worksheet.update_cells(clear_cell_list5, value_input_option='USER_ENTERED')

    cell_list5 = worksheet.range("L5:L" + str(index + 5))
    for cell in cell_list5:
        cell.value =  a[(cell.row - 5)][(cell.col - 9)]
    worksheet.update_cells(cell_list5, value_input_option='USER_ENTERED')

    # this part pastes gsheet with related data.
    sheet2 = client.open_by_key("1nodf_m9xd7jRcRRIx_CvS3VNjNTUAau_mpz7dTUfzFY").worksheet("Seri Künye")

    clear_cell_list = sheet2.range("A2:B5000")
    for cell in clear_cell_list:
        cell.value = " "
    sheet2.update_cells(clear_cell_list, value_input_option='USER_ENTERED')

    cell_list = sheet2.range('A2:B' + str(secondIndex + 2))
    for cell in cell_list:
        cell.value = b[(cell.row - 2)][(cell.col - 1)]
    sheet2.update_cells(cell_list, value_input_option='USER_ENTERED')

    # this part pastes gsheet with related data.
    sheet = client.open_by_key("1eELo_AJ7hFLWfXxbU3i87KxnEbOgdIU4vvKVpcxS3Wo").worksheet("newLiteExcel")

    clear_cell_list2 = sheet.range("A2:B5000")
    for cell in clear_cell_list2:
        cell.value = ""
    sheet.update_cells(clear_cell_list2, value_input_option='USER_ENTERED')

    cell_list = sheet.range('A2:B' + str(index + 2))
    for cell in cell_list:
        cell.value = a[(cell.row - 2)][(cell.col - 1)]
    sheet.update_cells(cell_list, value_input_option='USER_ENTERED')