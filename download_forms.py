import os
import requests
import sys
from search_forms import find_num_of_page_results, search_webpage, get_results_table


def create_subdirectory(forms_to_add, form_name, start_year, end_year):
    """Creates subdirectory containing pdfs of matching forms"""
    for form_listing in forms_to_add:
   
        product_name = form_listing.find("a").get_text().strip()
        year = form_listing.find("td", class_="EndCellSpacer").get_text().strip() 

        if product_name == form_name:
            if int(year) in range(int(start_year), int(end_year + 1)):
                pdf = form_listing.find(href=True)
                pdf = pdf['href']

                pdf_file = f"{product_name}-{year}.pdf"   

                path = os.path.join(product_name, pdf_file)

                if not os.path.exists(product_name):
                    os.makedirs(product_name)

                with open(path, "wb") as f_out:
                    f_out.write(requests.get(pdf).content)


def download_forms(form_name, start_year, end_year):
    """Downloads pdfs into subdirectory, taking into accoutn multiple page results."""
    results_html = search_webpage(form_name, 0)

    num_page_results = find_num_of_page_results(results_html)
    if not num_page_results:
            return None

    for page_number in range(num_page_results):
        results_table = get_results_table(page_number, form_name)
        create_subdirectory(results_table, form_name, start_year, end_year)
        

def main():
    if len(sys.argv) != 4:
        print("Enter the name of form in quotations marks, followed by the start year and end year.")
        print("Ex: 'Form W-2' 2018 2020")
        return
    
    form_name = sys.argv[1]
    try:
        start_year = int(sys.argv[2])
        end_year = int(sys.argv[3])
    except:
        return

    download_forms(form_name, start_year, end_year)
   

if __name__ == "__main__":
    main()