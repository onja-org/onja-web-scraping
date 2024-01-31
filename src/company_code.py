from urllib.parse import urlparse

def extract_company_code(url):
    # Parse the URL to get the domain
    parsed_url = urlparse(url)
    
    # Get the segments of the domain
    domain_segments = parsed_url.netloc.split('.')

    # Handle common subdomains like 'www'
    if len(domain_segments) >= 2:
        if domain_segments[0] == 'www':
            return '.'.join(domain_segments[1:])
        else:
            return '.'.join(domain_segments)
  
