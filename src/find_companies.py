import os
import requests
from dotenv import load_dotenv
import logging

from src.google_sheet_connection import connect_to_google_spreadsheet, get_google_sheet_records, add_row_to_google_sheet
from src.get_website_contact import get_website_contact

load_dotenv()

def get_api_key():
    print(f'"""Retrieve API key from environment variables."""')
    """Retrieve API key from environment variables."""
    return os.getenv("API_KEY")

def check_existing_companies(records, companies, worksheet):
    """Checks for existing companies and adds new ones to the Google Sheet."""
    existing_companies = set(record.get('company name') for record in records)
    
    new_companies = []
    for company in companies:
        properties = company.get('properties', {})
        company_name = properties.get('name')
        website_url = properties.get('website_url')
        linkedin_url = properties.get('linkedin', {}).get('value')
        # matched_emails = get_website_contact(f'{website_url}/careers')
        # print(f'company_name: {company_name}')

        # print(f'emails: {matched_emails}')
        # emails = scrape_emails(website_url)
        if company_name not in existing_companies:
            new_companies.append({
                "name": company_name,
                "website_url": website_url,
                "linkedin_url": linkedin_url,
                # "emails": matched_emails
            })
            # # Add new company to the Google Sheet
            row_values = ["email_to_find@gmail.com", "", '', '', '', '', '', '', '', '', website_url, company_name, 'company_code_to_find']
            add_row_to_google_sheet(worksheet, row_values)

    return new_companies

def find_companies(query_params):
    """Fetches companies from the API and checks for new ones to add to the Google Sheet."""
    try:
        api_key = get_api_key()
        userkey = {"user_key": api_key}

        google_sheet = connect_to_google_spreadsheet()
        worksheet = google_sheet.get_worksheet(0)

        # Fetch records from Google Sheet
        google_sheet_records = get_google_sheet_records()
        print(f'{userkey}')
        # Fetch companies from API
        response = requests.post("https://api.crunchbase.com/api/v4/searches/organizations", params=userkey, json=query_params)
        response.raise_for_status()
        companies = response.json().get("entities", [])

        # Check for new companies not in the Google Sheet and add them
        new_companies = check_existing_companies(google_sheet_records, companies, worksheet)

        return new_companies
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during API request: {e}")
        return { "message": f"Error occurred during API request: {e}"}
