from urllib.parse import urlparse

def extract_company_code(url):
    # Parse the URL to get the domain
    parsed_url = urlparse(url)
    
    # Get the segments of the domain
    domain_segments = parsed_url.netloc.split('.')

    # Extract the last two segments as the company code
    if len(domain_segments) >= 2:
        company_code = '.'.join(domain_segments[-2:])
        return company_code
    else:
        # Handle cases where the domain doesn't have at least two segments
        return None
    