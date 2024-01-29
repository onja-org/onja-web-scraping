import os
from dotenv import load_dotenv
import requests
import json
import pandas as pd
from pandas import json_normalize

load_dotenv()

api_key = os.getenv("API_KEY")
userkey = {"user_key":api_key}

query = {
  "field_ids": [
    "name",
    "short_description",
    "website_url",
    "linkedin",
  ],
  "query": [
    {
      "type": "predicate",
      "field_id": "location_identifiers",
      "operator_id": "includes",
      "values": [
        "Europe"
      ]
    }
  ],
  "limit": 10
}

def company_count(query):
    r = requests.post("https://api.crunchbase.com/api/v4/searches/organizations", params = userkey , json = query)
    result = json.loads(r.text)
    print(result)
    total_companies = result["count"]
    return total_companies

comp_count = company_count(query)

print(comp_count)
