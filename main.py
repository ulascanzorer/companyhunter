from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def email_finder(website_url):
    emails = []
    contact_links = []
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

    main_page = requests.get(website_url, headers = headers)
    main_soup = BeautifulSoup(main_page.content, "lxml")

    for link in main_soup.find_all("a"):
        if "Kontakt" in link.text or "KONTAKT" in link.text or "Contact" in link.text or "CONTACT" in link.text or "Impressum" in link.text or "IMPRESSUM" in link.text or "kontakt" in link.text or "contact" in link.text or "impressum" in link.text:
            contact_links.append(link)
        elif "@" in link.text:
            emails.append(link.text)
    

    for contact_link in contact_links:
        contact_url = contact_link["href"]

        ### TODO Format the contact url correctly.
        if "http" not in contact_url:
            contact_url = website_url + "/" + contact_url

        contact_page = requests.get(contact_url, headers = headers)
        contact_soup = BeautifulSoup(contact_page.content, "lxml")

        words_in_page = contact_soup.body.get_text().split()

        for word in words_in_page:
            if "@" in word:
                emails.append(word)


    print("------------------------")
    print(website_url)
    print(emails)
    print("------------------------")
    return emails


if __name__ == "__main__":
    # Get the query to search for.

    query = input("Main theme of the companies to hunt:\n")

    # Go through all the links from google search and save them in a list.

    website_urls = []

    for i in search(query, tld="de", num = 30, stop = 30, pause = 2):
        website_urls.append(i)
        print(i)

    for url in website_urls:
        email_finder(url)
