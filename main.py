from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup
import math


# browser = mechanicalsoup.Browser()

form_list = ["Form 1095-C", "Form W-2"]


#functions to find the number page results from searching for a form 
def find_num_of_page_results(num_of_results):
    """Takes in total number of results and returns the number of page results.
        Each page shows 200 results at a time"""
    num_of_pages = math.ceil(num_of_results / 200)
    return num_of_pages


def find_num_of_results(results_html):
        """Takes in the html of the search results page and returns the total number of results"""
        num_of_results = results_html.find("th", class_="ShowByColumn").get_text().strip()
        num_of_results = num_of_results.split()
        num_of_results = int(num_of_results[5])
        return num_of_results


def search_webpage(form_name, starting_point):
    """Retrieves and returns the HTML of a search results page."""

    beginning_url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow={starting_point}&value=" 
    end_url = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

    form_name = form_name.replace(" ", "")
    url = beginning_url + form_name + end_url
    page = urlopen(url) 
    html_bytes = page.read()
    page_html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(page_html, "html.parser")

    return parsed_html

def parse_forms_list(forms_to_add, results_lst, form_name):
    """Takes in the html of the form results, parses it, 
    and adds it to an array. Returns the array"""

    for item in forms_to_add:
            product_name = item.find("a").get_text().strip()
            title = item.find("td", class_="MiddleCellSpacer").get_text().strip()
            year = item.find("td", class_="EndCellSpacer").get_text().strip()

            #ensures that you only return exact matches
            if product_name == form_name:
                results_lst.append([product_name, title, year])

    return results_lst


def get_search_results(forms_to_search):

    final_results = []

    for form in forms_to_search:

        results_html = search_webpage(form, 0)
        num_total_results = find_num_of_results(results_html)
        num_page_results = find_num_of_page_results(num_total_results)

        results_lst = []

        for page_number in range(num_page_results):
            ind_of_first_row = (200 * page_number)

            parsed_html = search_webpage(form, ind_of_first_row)

            evens = parsed_html.find_all("tr", class_="even")
            odds = parsed_html.find_all("tr", class_="odd")

            results_lst = parse_forms_list(evens, results_lst, form)
            results_lst = parse_forms_list(odds, results_lst, form)

            #add the years from the results into a list to find min and max
            years = []
            for item in results_lst:
                years.append(int(item[2]))

        minimum = min(years)
        maximum = max(years)

        form_dict = {"form_number": results_lst[0][0], "form_title": results_lst[0][1],
                    "min_year": minimum, "max_year": maximum}

        final_results.append(form_dict)

    print(final_results)


get_search_results(form_list)






