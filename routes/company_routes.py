from flask import Blueprint, jsonify
from src.get_companies import get_companies

company_bp = Blueprint('company_bp', __name__)

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
    "limit": 100
}


@company_bp.route('/companies', methods=['GET'])
def fetch_companies():
    companies = get_companies(query)  # Assuming 'query' is defined in get_companies.py
    return jsonify(companies)