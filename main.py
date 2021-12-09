from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup


# browser = mechanicalsoup.Browser()
beginning_url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow=0&value=" 
end_url = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

form_list = ["Form 1095-C", "Form W-2"]

def get_search_results(forms_to_search):

    for form in forms_to_search:
        joined_name = form.replace(" ", "+")
    
        url = beginning_url + joined_name + end_url

        page = urlopen(url)
        html_bytes = page.read()
        page_html = html_bytes.decode("utf-8")
        parsed_html = BeautifulSoup(page_html, "html.parser")

        evens = parsed_html.find_all("tr", class_="even")
        odds = parsed_html.find_all("tr", class_="odd")

        results_lst = []

        for item in evens:
            product_name = item.find("a").get_text().strip()
            title = item.find("td", class_="MiddleCellSpacer").get_text().strip()
            year = item.find("td", class_="EndCellSpacer").get_text().strip()
            print(product_name, title, year)

            if product_name == form:
                results_lst.append([product_name, title, year])


        for item in odds:
            product_name = item.find("a").get_text().strip()
            title = item.find("td", class_="MiddleCellSpacer").get_text().strip()
            year = item.find("td", class_="EndCellSpacer").get_text().strip()
            print(product_name, title, year)

            if product_name == form:
                results_lst.append([product_name, title, year])






        years = []
        for item in results_lst:
            years.append(int(item[2]))
        
        minimum = min(years)
        maximum = max(years)

        print(minimum, maximum)


        final_results = []

        form_dict = {"form_number": results_lst[0][0], "form_title": results_lst[0][1],
                    "min_year": minimum, "max_year": maximum}

        final_results.append(form_dict)

        print(final_results)


    def filter_results(lst_of_lists):
        pass


get_search_results(form_list)






