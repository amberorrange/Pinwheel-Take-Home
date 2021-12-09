from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup


browser = mechanicalsoup.Browser()
beginning_url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow=0&value=" 
end_url = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

form_list = ["Form 1095-C"]

for form in form_list:
    joined_name = form.replace(" ", "+")
   

    url = beginning_url + joined_name + end_url

    page = urlopen(url)
    html_bytes = page.read()
    page_html = html_bytes.decode("utf-8")


    parsed_html = BeautifulSoup(page_html, "html.parser")

    # print(parsed_html.get_text())

    form_table = parsed_html.find_all("table", class_="picklist-dataTable")

    evens = parsed_html.find_all("tr", class_="even")

    odss = parsed_html.find_all("tr", class_="odd")


# print(form_table)

results_lst = []
for item in evens:
    # print(item)

    product_name = item.find("a").get_text().strip()

    title = item.find("td", class_="MiddleCellSpacer").get_text().strip()

    year = item.find("td", class_="EndCellSpacer").get_text().strip()

    print(product_name, title, year)









    def filter_results(lst_of_lists):






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