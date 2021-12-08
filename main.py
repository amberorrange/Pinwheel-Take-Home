from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup


browser = mechanicalsoup.Browser()
# url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
# page = browser.get(url)
# page_html = page.soup


beginning_url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html;jsessionid=rhBpcYp77FqlnEus-PDcS79Y.20?value=" 
end_url = "&criteria=formNumber&submitSearch=Find"

form_list = ["Form 1095-C"]

for form in form_list:
    joined_name = form.replace(" ", "+")
    print(joined_name)

    url = beginning_url + joined_name + end_url

    page = browser.get(url)
    page_html = page.soup

    print(page_html)







#get the form
# form = page_html.select("form")

# search_box = page_html.select("input", id="searchFor")[0]["value"] = "Form 1095-C"

# results_page = (browser.submit((form, page.url)))



# submit_btn = page_html.select("input", id="searchFor")[1]

# print(search_box)
# print(submit_btn)





# form.select("input")[3]["value"] = "zeus"



# print(form)
# form.select("input")[0]["value"] = "Form 1095-C"
# search_results = browser.submit(form, page.url)



# print(browser.get(search_results))



# url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
# page = urlopen(url)
# html = page.read().decode("utf-8")

# soup = BeautifulSoup(html, "html.parser")

# search_box = soup.find("input", id="searchFor")

# submit_button = soup.find("input", type="submit", value="Find")


#the top steps get me the html
#now I need to parse through the html and fill out the form with the given form name
#click submit and receive results
# on the results page I need to sort by date, earliest to latest and make s
#names are an exact match....how to deal with multiple pages of results


# print(search_box)
# print() 
# print(submit_button)