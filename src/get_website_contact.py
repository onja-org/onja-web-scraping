import requests
from bs4 import BeautifulSoup
import re

def get_website_contact(website_url):

    # Define user-agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    # Send an HTTP GET request to the URL with headers
    response = requests.get(website_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all text on the page
        text = soup.get_text()
        # Define a regex pattern for email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # Search for email addresses in the text
        matches = re.findall(email_pattern, text)
        # Check if the email address you're looking for is in the matches
        return matches
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

