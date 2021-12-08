from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup

browser = mechanicalsoup.Browser()
url = "http://olympus.realpython.org/login"
login_page = browser.get(url)
login_html = login_page.soup

form = login_html.select("form")


print(form)