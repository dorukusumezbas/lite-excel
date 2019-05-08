import requests

def main():
    link2 = "http://188.132.229.74:9090/IntegratorService/connect"
    link3 = "http://188.132.229.74:9090/(S("
    link3cont = "))/IntegratorService/getUserInfo"
    s = requests
    connect = s.post(link2)
    connectResponse = connect.json()
    print(connectResponse)
    sessionID = connectResponse["SessionID"]
    print(sessionID)
    connectionInfo = s.post(link3 + sessionID + link3cont)
    connectionInfoResponse = connectionInfo.json()
    print(connectionInfoResponse)
    return sessionID