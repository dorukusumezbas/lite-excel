import sys
sys.path.insert(0,'/home/ubuntu/projects/lite-excel')
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def main():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    return client