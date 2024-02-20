import os
import requests
from dotenv import load_dotenv
import logging
import csv
import json
from bs4 import BeautifulSoup

from src.google_sheet_connection import connect_to_google_spreadsheet, get_google_sheet_records, add_row_to_google_sheet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f'[Parameters]')

load_dotenv()

def get_website_contacts(website_url):
    try:
        response = requests.get(website_url)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all contact information
        contacts = []
        contact_elements = soup.find_all('a', href=True)
        for contact_element in contact_elements:
            contact = contact_element.get('href')
            if contact.startswith('mailto:'):
                contacts.append(contact[7:])  # Remove 'mailto:' prefix

        return contacts
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during website request: {e}")
        return []
    
def read_csv(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip the header
        header = next(reader)
        updated_data = [row for row in reader]
        data = []
        new_data = []
        for concatenated_string in updated_data:
            data.append(concatenated_string)
        for inner_array in data:
            keys = [
                "name",
                "website",
                "company_type",
                "contact_email",
                "founder",
            ]
            obj = dict(zip(keys, inner_array))
            new_obj = {}
            for key, value in obj.items():
                if key == "name":
                    new_obj["name"] = value
                if key == "website":
                    new_obj["website_url"] = value
                if key == "contact_email":
                    new_obj["contact_email"] = value
                if key == "founder":
                    new_obj["founder"] = value
                if key == "company_type":
                    new_obj["company_type"] = value

            new_data.append(new_obj)

    return new_data
    
def get_api_key():
    print(f'"""Retrieve API key from environment variables."""')
    """Retrieve API key from environment variables."""
    return os.getenv("API_KEY")

def new_company_data(name, email, type, founders, website, custom_paragraph, profile_sentence, respondent_email, proposed_developer, proposed_developer_experience, chase_email_subject, date_applied, link_to_open_position, company_code):
    return {
        "company_name": name,
        "email": email,
        "company_type": type,
        "founders": founders,
        "company_website": website,
        "custom_paragraph": custom_paragraph,
        "profile_sentence": profile_sentence,
        "respondent_email": respondent_email,
        "proposed_developer(s)": proposed_developer,
        "proposed_developer_experience": proposed_developer_experience,
        "chase_email_subject": chase_email_subject,
        "date_applied": date_applied,
        "link_to_open_position": link_to_open_position,
        "company_code": company_code,
    }

def data_scrapper(companies_from_csv, companies_from_api):
    # Compare companies from CSV with companies from API and update contact_email
    updated_companies = []

    for company in companies_from_api:
        properties = company.get('properties', {})
        company_name = properties.get('name')
        contact_email = ""
        company_type = ""
        founder = ""
        # contacts = get_website_contacts(properties.get('website_url'))

        for company_csv in companies_from_csv:
            if company_name == company_csv.get("name"):
                contact_email = company_csv.get("contact_email")
                # company_type = company_csv.get("company_type")
                founder = company_csv.get("founder")

        new_company = new_company_data(
            company_name,
            contact_email,
            company_type,
            founder,
            properties.get('website_url'),
            "",
            "Here's a link to my portfolio: daniel.onja.org",
            "",
            "Multiple",
            "0",
            "Application for Strong interest in socialhub.io Position role",
            "21 Feb 2024",
            "link of open position can't be find",
            "No code found"
        )

        updated_companies.append(new_company)
    return updated_companies

def check_company_exists(companies, records, worksheet):
        for company in companies:
            new_company = new_company_data(
                company.get('name'),
                company.get('contact_email'),
                company.get('company_type'),
                company.get('founder'),
                company.get('website_url'),
                company.get('custom_paragraph'),
                company.get('profile_sentence'),
                company.get('respondent_email'),
                company.get('proposed_developer(s)'),
                company.get('proposed_developer_experience'),
                company.get('chase_email_subject'),
                company.get('date_applied'),
                company.get('link_to_open_position'),
                company.get('company_code')
            )
            
            if new_company["company_name"] not in records:
                records.append(new_company)
                # Why is the "Chase email subject" and "date applied" not added in the google sheet?

                add_row_to_google_sheet(worksheet, [
                    new_company["email"],
                    new_company["profile_sentence"],
                    new_company["proposed_developer(s)"],
                    new_company["proposed_developer_experience"],
                    new_company["profile_sentence"],
                    new_company["custom_paragraph"],
                    new_company["chase_email_subject"],
                    new_company["date_applied"],
                    new_company["link_to_open_position"],
                    new_company["company_website"],
                    new_company["company_name"],
                    new_company["company_code"],
                    new_company["founders"],
                    new_company["company_type"]
                ])
        
def find_companies(query_params, output_csv_file):
    """Fetches companies from the API and exports the data to a CSV file."""
    try:
        api_key = get_api_key()
        userkey = {"user_key": api_key}

        # Fetch companies from API
        response = requests.post("https://api.crunchbase.com/api/v4/searches/organizations", params=userkey, json=query_params)
        response.raise_for_status()
        companies = response.json().get("entities", [])

        # Get company names and contact_emails from csv
        data = read_csv("companies.csv")
        companies_from_csv = []
        for company in data:
            companies_from_csv.append({
                "name": company.get("name"),
                "contact_email": company.get("company_type"),
                "founder": company.get("founder"),
                "website_url": company.get("website_url"),
            })

        updated_companies = data_scrapper(companies_from_csv, companies)

        # Connect to the Google Sheet
        worksheet = connect_to_google_spreadsheet().get_worksheet(0)
        headers = worksheet.row_values(1)
        logger.info(f'headers: {headers}')
        records = get_google_sheet_records()
        # how to check if the company already exists in the google sheet
        # new_companies = check_company_exists(updated_companies, records, worksheet)

        return headers
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during API request: {e}")
        return { "message": f"Error occurred during API request: {e}"}
    
