from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup
import math

# browser = mechanicalsoup.Browser()

#these do not change
BEGINNING_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow=0&value=" 
END_URL = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

form_list = ["Form 1095-C", "Form W-2"]


def find_num_of_pages(results_count):
    """returns the number of pages of results with each page showing 200 results at a time"""
    num_of_pages = math.ceil(results_count / 200)
    return num_of_pages


def get_number_of_results(results_html):
        """returns the number of results from a search"""
        num_of_results = results_html.find("th", class_="ShowByColumn").get_text().strip()
        num_of_results = num_of_results.split()
        num_of_results = int(num_of_results[5])
        num_of_results_pages = find_num_of_pages(num_of_results)
        return num_of_results_pages


def initial_search(form_name):
    """returns the number of page results after from searching for a form"""
    joined_name = form_name.replace(" ", "+")
    url = BEGINNING_URL + joined_name + END_URL
    page = urlopen(url)
    html_bytes = page.read()
    page_html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(page_html, "html.parser")

    results_pages = get_number_of_results(parsed_html)

    return results_pages

        

def get_search_results(forms_to_search):

    final_results = []

    for form in forms_to_search:
        num_page_results = initial_search(form)
        results_lst = []

        for page_number in range(num_page_results):
            ind_of_first_row = (200 * page_number)

            # print(form, page_number, ind_of_first_row)
            first_part_url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow={ind_of_first_row}&value=" 

            url = first_part_url + form + END_URL
            url = url.replace(" ","")
            # print(url)

            page = urlopen(url)
            html_bytes = page.read()
            page_html = html_bytes.decode("utf-8")
            parsed_html = BeautifulSoup(page_html, "html.parser")

            evens = parsed_html.find_all("tr", class_="even")
            odds = parsed_html.find_all("tr", class_="odd")


            for item in evens:
                product_name = item.find("a").get_text().strip()
                title = item.find("td", class_="MiddleCellSpacer").get_text().strip()
                year = item.find("td", class_="EndCellSpacer").get_text().strip()
                # print(product_name, title, year)

                if product_name == form:
                    results_lst.append([product_name, title, year])


            for item in odds:
                product_name = item.find("a").get_text().strip()
                title = item.find("td", class_="MiddleCellSpacer").get_text().strip()
                year = item.find("td", class_="EndCellSpacer").get_text().strip()
                # print(product_name, title, year)

                if product_name == form:
                    results_lst.append([product_name, title, year])



            years = []

            for item in results_lst:
                years.append(int(item[2]))

        # print("years: ", years)
        
        minimum = min(years)
        maximum = max(years)

        # print(minimum, maximum)


        form_dict = {"form_number": results_lst[0][0], "form_title": results_lst[0][1],
                    "min_year": minimum, "max_year": maximum}

        final_results.append(form_dict)

    print(final_results)



get_search_results(form_list)






