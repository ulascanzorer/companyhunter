from googlesearch import search
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def email_finder(website_url):
    emails = set()
    contact_links = set()
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}


    session = HTMLSession()

    main_page = session.get(website_url, headers = headers)
    main_soup = BeautifulSoup(main_page.html.raw_html, "lxml")

    ### Get all links from the main page of the website, save the "contact-links" in contact_links and links that match the email pattern in emails.

    ### Define some patterns to detect contact links or 'valid' emails.
    contact_link_pattern = re.compile(r'([ck]onta[ck]t) | (impressum)', flags=re.IGNORECASE)
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

    for link in main_soup.find_all("a"):
        if re.search(contact_link_pattern, link.text):
            contact_links.add(link)
        elif email_result := re.search(email_pattern, link.text):
            emails.add(email_result.group(0))
    

    ### Go through all the contact links by going to the corresponding contact website, then save every string that matches the email pattern.

    for contact_link in contact_links:
        contact_url = contact_link["href"]

        ### If href isn't a complete url.
        if "http" not in contact_url:
            parts_of_url = urlparse(website_url)
            if contact_url[0] == "/":
                contact_url = parts_of_url.scheme + "://" + parts_of_url.netloc + contact_url
            else:
                contact_url = parts_of_url.scheme + "://" + parts_of_url.netloc + "/" + contact_url  

        contact_page = session.get(contact_url, headers = headers)
        contact_page.html.render()
        contact_soup = BeautifulSoup(contact_page.html.raw_html, "lxml")

        words_in_page = contact_soup.body.get_text().split()

        for word in words_in_page:
            if email_result := re.search(email_pattern, word):
                emails.add(email_result.group(0))

        for link in contact_soup.find_all("a"):
            if email_result := re.search(email_pattern, link.text):
                emails.add(email_result.group(0))


    print("------------------------")
    print(website_url)
    print("Emails from this website: ", emails)
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
