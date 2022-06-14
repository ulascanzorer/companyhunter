import requests
from bs4 import BeautifulSoup


def email_finder(website_url):
    emails = []
    contact_links = []
    main_page = requests.get(website_url)
    main_soup = BeautifulSoup(main_page.content, "html.parser")

    for link in main_soup.find_all("a"):
        if "Kontakt" in link.text or "KONTAKT" in link.text or "Contact" in link.text or "CONTACT" in link.text or "Impressum" in link.text or "IMPRESSUM" in link.text or "kontakt" in link.text or "contact" in link.text or "impressum" in link.text:
            contact_links.append(link)
        elif "@" in link.text:
            emails.append(link.text)
    
    ### TODO Go through all the contact links.


    for contact_link in contact_links:
        contact_url = contact_link["href"]
        if "http" not in contact_url:
            contact_url = website_url + "/" + contact_url

        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

        contact_page = requests.get(contact_url, headers = headers)
        contact_soup = BeautifulSoup(contact_page.content, "lxml")

        words_in_page = contact_soup.body.get_text().split()

        for word in words_in_page:
            if "@" in word:
                emails.append(word)

    return emails


print(email_finder("https://www.hellas-gmbh.com/"))