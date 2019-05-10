import sys
sys.path.insert(0,'/Projects/lite-excel/')
import requests

def main():
    print("NEBİM bağlantısı başladı. \n")
    link2 = "http://188.132.229.74:9090/IntegratorService/connect"
    link3 = "http://188.132.229.74:9090/(S("
    link3cont = "))/IntegratorService/getUserInfo"
    s = requests
    connect = s.post(link2)
    connectResponse = connect.json()
    sessionID = connectResponse["SessionID"]
    connectionInfo = s.post(link3 + sessionID + link3cont)
    connectionInfoResponse = connectionInfo.json()
    print("NEBİM'e başarıyla bağlanıldı. \n")
    return sessionID