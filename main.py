from googlesearch import search
import requests
from bs4 import BeautifulSoup

def email_finder(website_url):
    emails = []
    contact_links = []
    page = requests.get(website_url)
    soup = BeautifulSoup(page.content, "lxml")

    for link in soup.find_all("a"):
        if "Kontakt" in link.text or "Contact" in link.text or "Impressum" in link.text or "kontakt" in link.text or "contact" in link.text or "impressum" in link.text:
            contact_links.append(link)
        elif "@" in link.text:
            emails.append(link.text)
    
    ### TODO Go through all the contact links.
    
    return emails



# Get the query to search for.

query = input("Main theme of the companies to hunt:\n")

# Go through all the links from google search and save them in a list.

website_urls = []

for i in search(query, tld="de", num = 30, stop = 30, pause = 2):
    website_urls.append(i)

for url in website_urls:
    print(email_finder(url))




