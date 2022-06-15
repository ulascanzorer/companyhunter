from googlesearch import search
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def email_finder(website_url):
    emails = set()
    contact_links = set()
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}


    session = HTMLSession()

    main_page = session.get(website_url, headers = headers)
    main_soup = BeautifulSoup(main_page.html.raw_html, "lxml")

    ### Get all links from the main page of the website, save the "contact-links" in contact_links and links that contain "@" in emails.

    for link in main_soup.find_all("a"):
        if "Kontakt" in link.text or "KONTAKT" in link.text or "Contact" in link.text or "CONTACT" in link.text or "Impressum" in link.text or "IMPRESSUM" in link.text or "kontakt" in link.text or "contact" in link.text or "impressum" in link.text:
            contact_links.add(link)
        elif "@" in link.text or "(at)" in link.text:
            emails.add(link.text)
    

    ### Go through all the contact links by going to the corresponding contact website, then save every string that contains "@" in emails.

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
            if "@" in word or "(at)" in word:
                emails.add(word)

        for link in contact_soup.find_all("a"):
            if "@" in link.text or "(at)" in link.text:
                emails.add(word)


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
