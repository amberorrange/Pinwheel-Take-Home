from bs4 import BeautifulSoup
import math
import os
import requests
import sys


#input-each form name must be in strings and separated by a comma with no white space in between

form_list = ["Form 1095-C", "Form W-2"]

#functions to find the number page results from searching for a form 
def find_num_of_page_results(num_of_results):
    """Takes in total number of results and returns the number of page results.
        Each page shows 200 results at a time"""
    num_of_pages = math.ceil(num_of_results / 200)
    return num_of_pages


def find_num_of_results(results_html):
        """Takes in the html of the search results page and returns the total number of results"""
        try:
            num_of_results = results_html.find("th", class_="ShowByColumn").get_text().strip()
        except:
            return None

        num_of_results = num_of_results.split()
        num_of_results = num_of_results[5].replace(",", "")
        num_of_results = int(num_of_results)
        return num_of_results


def search_webpage(form_name, starting_point):
    """Retrieves and returns the HTML of a search results page."""

    beginning_url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?sortColumn=currentYearRevDate&indexOfFirstRow={starting_point}&value=" 
    end_url = "&criteria=formNumber&resultsPerPage=200&isDescending=false"

    form_name = form_name.replace(" ", "")
    url = beginning_url + form_name + end_url

    page = requests.get(url)
    page_html = page.text

    parsed_html = BeautifulSoup(page_html, "html.parser")

    print(parsed_html)

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

def retrieve_pdfs(forms_to_add, form_name, range_start, range_end):
    """Takes in the html of the form results, parses it, and returns the pdf files to be downloaded"""

    for item in forms_to_add:

        product_name = item.find("a").get_text().strip()
        year = item.find("td", class_="EndCellSpacer").get_text().strip() 

        if product_name == form_name:
            if int(year) in range(range_start, range_end + 1):
                # print(year)
                pdf = item.find(href=True)
                pdf = pdf['href']
                # print(pdf)


                p = f"{product_name}-{year}"   

                path = os.path.join(product_name, p)

                if not os.path.exists(product_name):
                    os.makedirs(product_name)

                with open(path, "wb") as f_out:
                    #can I do this with beautiful soup?
                    f_out.write(requests.get(pdf).content)
               

                



def get_search_results(forms_to_search):

    final_results = []

    for form in forms_to_search:

        results_html = search_webpage(form, 0)

        num_total_results = find_num_of_results(results_html)
        
        
        if not num_total_results:
            return None

        num_page_results = find_num_of_page_results(num_total_results)

        results_lst = []

        for page_number in range(num_page_results):
            ind_of_first_row = (200 * page_number)

            parsed_html = search_webpage(form, ind_of_first_row)

            evens = parsed_html.find_all("tr", class_="even")
            odds = parsed_html.find_all("tr", class_="odd")


            pdfs = retrieve_pdfs(evens, form, 2018, 2020)
            pdfs_odd = retrieve_pdfs(odds, form, 2018, 2020)
            

            results_lst = parse_forms_list(evens, results_lst, form)
            results_lst = parse_forms_list(odds, results_lst, form)

            #add the years from the results into a list to find min and max
            years = []
            for item in results_lst:
                years.append(int(item[2]))

        if years:
            minimum = min(years)
            maximum = max(years)

            form_dict = {"form_number": results_lst[0][0], "form_title": results_lst[0][1],
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



