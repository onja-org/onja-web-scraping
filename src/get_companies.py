import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import re

load_dotenv()
api_key = os.getenv("API_KEY")
userkey = {"user_key": api_key}

def connect_to_google_spreadsheet():
    """Connects to the Google Sheets API and returns the spreadsheet."""
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('cat-db.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open('Copy of First Copy of CAT database and analytics  for duplication analysis')
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

def check_existing_companies(records, companies, worksheet):
    """Checks for existing companies and adds new ones to the Google Sheet."""
    existing_companies = set(record.get('company name') for record in records)
    new_companies = []

    for company in companies:
        properties = company.get('properties', {})
        company_name = properties.get('name')
        website_url = properties.get('website_url')
        linkedin_url = properties.get('linkedin', {}).get('value')
        permalink = properties.get("permalink")

        if not permalink:
            company_code = generate_company_code(company_name)
        else:
            company_code= permalink 
        
        if company_name not in existing_companies:
          new_companies.append({
              "name": company_name,
              "website_url": website_url,
              "linkedin_url": linkedin_url
          })

          row_values = ['contact_to_find@gmail.com', '', '', '', '', '', '', '', '', website_url, company_name, company_code]
          add_row_to_google_sheet(worksheet, row_values)
          
    return new_companies

def generate_company_code(company_name):
    cleaned_name = re.sub(r'\W+', '', company_name).lower()
    company_code = cleaned_name[:10]

    return company_code

# This should be changed to find_companies in the future and will take a payload from the frontend
def get_companies(query_params):
    """Fetches companies from the API and checks for new ones to add to the Google Sheet."""
    try:
        google_sheet = connect_to_google_spreadsheet()
        worksheet = google_sheet.get_worksheet(0)

        # Fetch records from Google Sheet
        google_sheet_records = get_google_sheet_records()

        # Fetch companies from API
        response = requests.post("https://api.crunchbase.com/api/v4/searches/organizations", params=userkey, json=query_params)
        response.raise_for_status()
        companies = response.json().get("entities", [])

        # Check for new companies not in the Google Sheet and add them
        new_companies = check_existing_companies(google_sheet_records, companies, worksheet)

        return new_companies
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return { "message": f"Error occurred during API request: {e}"}
