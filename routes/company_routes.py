from flask import Blueprint, jsonify
from src.find_companies import find_companies

company_bp = Blueprint('company_bp', __name__)

query = {
    "field_ids": [
        "name",
        "website_url",
        "linkedin",
        'contact_email'
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
    "limit": 50
}


@company_bp.route('/companies/bulk', methods=['GET'])
def fetch_companies():
    companies = find_companies(query)
    return jsonify(companies)