import sys
sys.path.insert(0,'/Projects/lite-excel/')
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def main():
    print("Google bağlantısı başladı. \n")
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    print("Google'a başarıyla bağlanıldı. \n")
    return client