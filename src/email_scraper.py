import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup

def scrape_emails(user_url):
    if "https://" in user_url:
        user_url = user_url
    else:
        user_url = "https://" + user_url

    unscraped_url = deque([user_url])
    scraped_url = set()
    list_emails = set()

    try:
        while len(unscraped_url):
            url = unscraped_url.popleft()
            scraped_url.add(url)
            parts = urlsplit(url)

            base_url = "{0.scheme}://{0.netloc}".format(parts)

            if '/' in parts.path:
                part = url.rfind("/")
                path = url[0:part + 1]
            else:
                path = url

            try:
                response = requests.get(url)
            except (
                requests.exceptions.MissingSchema,
                requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL,
            ):
                continue
            new_emails = (
                (
                    re.findall(
                        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                        response.text,
                        re.I,
                    )
                )
            )
            list_emails.update(new_emails)
            soup = BeautifulSoup(response.text, features="xml")
            for tag in soup.find_all("a"):
                if "href" in tag.attrs:
                    weblink = tag.attrs["href"]
                else:
                    weblink = ""
                if weblink.startswith("/"):
                    weblink = base_url + weblink
                elif not weblink.startswith("https"):
                    weblink = path + weblink
                if base_url in weblink:
                    if (
                        "contact" in weblink
                        or "Contact" in weblink
                        or "About" in weblink
                        or "about" in weblink
                        or "CONTACT" in weblink
                        or "ABOUT" in weblink
                        or "contact-us" in weblink
                    ):
                        if not weblink in unscraped_url and not weblink in scraped_url:
                            unscraped_url.append(weblink)
        return list_emails

    except KeyboardInterrupt:
        print("Program terminated manually!")
        raise SystemExit
