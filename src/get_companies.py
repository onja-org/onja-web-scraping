import os
import requests
from dotenv import load_dotenv
from .company_code import extract_company_code

from src.google_sheet_connection import connect_to_google_spreadsheet, get_google_sheet_records, add_row_to_google_sheet
from src.email_scraper import scrape_emails


load_dotenv()
api_key = os.getenv("API_KEY")
userkey = {"user_key": api_key}

def check_existing_companies(records, companies, worksheet):
    """Checks for existing companies and adds new ones to the Google Sheet."""
    existing_companies = set(record.get('company name') for record in records)
    new_companies = []

    for company in companies:
        properties = company.get('properties', {})
        company_name = properties.get('name')
        website_url = properties.get('website_url')
        linkedin_url = properties.get('linkedin', {}).get('value')
        company_code = extract_company_code(website_url)
        emails = scrape_emails(website_url)
        
        if company_name not in existing_companies:
          new_companies.append({
              "name": company_name,
              "website_url": website_url,
              "linkedin_url": linkedin_url,
              "company_code": company_code,
              "emails": emails
          })

          row_values = [", ".join(emails), '', '', '', '', '', '', '', '', website_url, company_name, company_code]
          add_row_to_google_sheet(worksheet, row_values)
          
    return new_companies

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
