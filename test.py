from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = "https://www.efa-dienstleistung.de/de/kontakt"

headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

session = HTMLSession()


page = session.get(url, headers = headers)
page.html.render()
soup = BeautifulSoup(page.html.raw_html, "lxml")

words_in_page = soup.body.get_text().split()

for word in words_in_page:
    if "@" in word:
        print(word)

for link in soup.find_all("a"):
    if "@" in link.text:
        print(link.text)