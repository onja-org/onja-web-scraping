import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

userkey = {"user_key": api_key}

def get_companies(query_params):
    try:
        response = requests.post("https://api.crunchbase.com/api/v4/searches/organizations", params=userkey, json=query_params)
        # Raise an exception for HTTP errors
        response.raise_for_status()
        result = response.json()
        companies = result.get("entities", [])
        responseData = []
        for company in companies:
          properties = company.get('properties', {})
          name = properties.get('name')
          website_url = properties.get('website_url')
          linkedin_url = properties.get('linkedin', {}).get('value')
          responseData.append({
              "name": name,
              "website_url": website_url,
              "linkedin_url": linkedin_url
          })
        return responseData
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return []