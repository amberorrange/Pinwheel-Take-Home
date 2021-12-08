from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

search_box = soup.find("input", id="searchFor")

submit_button = soup.find("input", type="submit", value="Find")


#the top steps get me the html
#now I need to parse through the html and fill out the form with the given form name
#click submit and receive results
# on the results page I need to sort by date, earliest to latest and make s
#names are an exact match....how to deal with multiple pages of results


print(search_box)
print() 
print(submit_button)