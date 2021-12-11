from bs4 import BeautifulSoup
import math
import requests
import sys


def find_num_of_results(results_html):
        """Takes in the html of the search results page and returns the total number of results"""
        try:
            num_of_results = results_html.find("th", class_="ShowByColumn").get_text().strip()
        except:
            return None

        num_of_results = num_of_results.split()
        num_of_results = int(num_of_results[5].replace(",", ""))
    
        return num_of_results


def find_num_of_page_results(page_html):
    """Takes in total number of results and returns the number of page results.
        Each page shows 200 results at a time"""
    num_of_results =  find_num_of_results(page_html)

    if not num_of_results:
            return None

    num_of_pages = math.ceil(num_of_results / 200)

    return num_of_pages


def search_webpage(form_name, starting_point):
    """Retrieves and returns the HTML of a search results page."""

    beginning_url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow={starting_point}&value=" 
    end_url = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

    form_name = form_name.replace(" ", "")
    url = beginning_url + form_name + end_url

    page = requests.get(url)
    page_html = page.text
    parsed_html = BeautifulSoup(page_html, "html.parser")
   
    return parsed_html

def find_matching_forms(forms_to_add, results_lst, form_name):
    """Takes in the html of the form results, and adds
      matching results to an array. Returns the array"""

    for form_listing in forms_to_add:
            product_name = form_listing.find("a").get_text().strip()
            title = form_listing.find("td", class_="MiddleCellSpacer").get_text().strip()
            year = form_listing.find("td", class_="EndCellSpacer").get_text().strip()

            #ensures that you only return exact matches
            if product_name == form_name:
                results_lst.append([product_name, title, year])

    return results_lst


def create_years_lst(matching_forms):
        """Returns a list of years from forms that match"""
        years = []
        for item in matching_forms:
            years.append(int(item[2]))
        return years

def get_results_table(page_number, form_name):
    """Returns list of forms(in HTML" from the results page."""
    ind_of_first_row = (200 * page_number)

    parsed_html = search_webpage(form_name, ind_of_first_row)

    evens_table = parsed_html.find_all("tr", class_="even")
    odds_table = parsed_html.find_all("tr", class_="odd")

    return evens_table + odds_table



def get_search_results(forms_to_search):
    """Returns a list of all matching forms information in JSON"""
    final_results = []

    for form in forms_to_search:

        #first part is to get the number of pages results
        results_html = search_webpage(form, 0)

        num_page_results = find_num_of_page_results(results_html)
        if not num_page_results:
            return None

        #loop through each page of results
        results_lst = []
        for page_number in range(num_page_results):

            results_table = get_results_table(page_number, form)
            matching_results = find_matching_forms(results_table, results_lst, form)
           
            #add the years from the results into a list to find min and max
            years = create_years_lst(matching_results)

        if years:
            minimum = min(years)
            maximum = max(years)

            form_dict = {"form_number": matching_results[0][0], "form_title": matching_results[0][1],
                    "min_year": minimum, "max_year": maximum}

            final_results.append(form_dict)

    return final_results


def main():
    if len(sys.argv) != 2:
        print("Enter names of forms in quotations marks. \nSeparate with a comma and no spaces in between forms.")
        print("Ex: 'Form W-2','Form 1095-C'")
        return

    forms_lst = sys.argv[1].split(',')
    search_results = get_search_results(forms_lst)

    if search_results:
        print(search_results)
        return search_results
    else:
        print("No matches.")

    
if __name__ == "__main__":
    main()



