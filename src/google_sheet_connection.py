import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
userkey = {"user_key": api_key}
SPREADSHEET_URL = os.getenv('SPREADSHEET_URL')

def connect_to_google_spreadsheet():
    """Connects to the Google Sheets API and returns the spreadsheet."""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cat-db.json', scope)
    client = gspread.authorize(creds)
    spreadsheet_url = SPREADSHEET_URL
    spreadsheet = client.open_by_url(spreadsheet_url)
    return spreadsheet

def get_google_sheet_records():
    """Fetches records from the Google Sheet and returns them."""
    spreadsheet = connect_to_google_spreadsheet()
    worksheet = spreadsheet.get_worksheet(0)
    data = worksheet.get_all_records()
    return data

def add_row_to_google_sheet(worksheet, row_values):
    """Adds a row with the specified values to the Google Sheet."""
    worksheet.append_row(row_values)
