import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Suppress only the InsecureRequestWarning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
api_key = os.getenv("API_KEY")
userkey = {"user_key": api_key}
endpoint = "https://api.crunchbase.com/api/v4/searches/organizations"

def get_companies(query_params):
    try:
        response = requests.post(endpoint, params=userkey, json=query_params, verify=False)
        response.raise_for_status()
        result = response.json()
        companies = result.get("entities", [])
        responseData = []

        for company in companies:
            properties = company.get('properties', {})
            name = properties.get('name')
            website_url = properties.get('website_url')
            linkedin_url = properties.get('linkedin', {}).get('value')

            emails = get_emails(website_url)

            if not emails:
                emails = get_emails(linkedin_url)

            responseData.append({
                "name": name,
                "website_url": website_url,
                "linkedin_url": linkedin_url,
                "emails": emails
            })
        return responseData
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return []
    
def check_email(url):
    try:
        page = requests.get(url, verify=False)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'lxml')
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
        return emails
    except Exception as e:
        print(f"Error extracting emails from {url}: {e}")
        return []

def get_emails(url):
    emails = []
    possible_page_names = ["about", "career", "contact", "footer", "header", "sidebar"]
    emails += check_email(url)

    for page_name in possible_page_names:
        if page_name.lower() in url.lower():
            page_url = urljoin(url, page_name)
            emails += check_email(page_url)

    return emails

