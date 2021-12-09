from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup
import math

# browser = mechanicalsoup.Browser()

#these do not change
BEGINNING_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow=0&value=" 
END_URL = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

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


def initial_search(form_name):
    """Returns the number of page results after searching for a form"""
    joined_name = form_name.replace(" ", "+")
    url = BEGINNING_URL + joined_name + END_URL
    page = urlopen(url)
    html_bytes = page.read()
    page_html = html_bytes.decode("utf-8")
    parsed_html = BeautifulSoup(page_html, "html.parser")

    num_of_results = find_num_of_results(parsed_html)
    page_results = find_num_of_page_results(num_of_results)

    return page_results



def parse_forms_list(forms_to_add, results_lst, form_name):
    """Takes in the html all results, parses it, 
    and adds it to an array. Returns the array"""

    for item in forms_to_add:
            product_name = item.find("a").get_text().strip()
            title = item.find("td", class_="MiddleCellSpacer").get_text().strip()
            year = item.find("td", class_="EndCellSpacer").get_text().strip()
            # print(product_name, title, year)

            if product_name == form_name:
                results_lst.append([product_name, title, year])

    return results_lst








        

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
            print(url)

            page = urlopen(url)
            html_bytes = page.read()
            page_html = html_bytes.decode("utf-8")
            parsed_html = BeautifulSoup(page_html, "html.parser")

            evens = parsed_html.find_all("tr", class_="even")
            odds = parsed_html.find_all("tr", class_="odd")

            results_lst = parse_forms_list(evens, results_lst, form)
            results_lst = parse_forms_list(odds, results_lst, form)


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






