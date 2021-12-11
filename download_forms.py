import os
import requests
import sys
from search_forms import find_num_of_page_results, search_webpage



def retrieve_pdfs(forms_to_add, form_name, start_year, end_year):
    """Takes in the html of the form results, parses it, and returns the pdf files to be downloaded"""

    for item in forms_to_add:
   
        product_name = item.find("a").get_text().strip()
        year = item.find("td", class_="EndCellSpacer").get_text().strip() 

        if product_name == form_name:
            if int(year) in range(int(start_year), int(end_year + 1)):
                pdf = item.find(href=True)
                pdf = pdf['href']

                p = f"{product_name}-{year}.pdf"   

                path = os.path.join(product_name, p)

                if not os.path.exists(product_name):
                    os.makedirs(product_name)

                with open(path, "wb") as f_out:
                    f_out.write(requests.get(pdf).content)





def download_forms(form_name, start_year, end_year):
    results_html = search_webpage(form_name, 0)

    num_page_results = find_num_of_page_results(results_html)
    if not num_page_results:
            return None

    print(num_page_results)

    for page_number in range(num_page_results):
            ind_of_first_row = (200 * page_number)

            parsed_html = search_webpage(form_name, ind_of_first_row)

            evens = parsed_html.find_all("tr", class_="even")
            odds = parsed_html.find_all("tr", class_="odd")

            retrieve_pdfs(evens, form_name, start_year, end_year)
            retrieve_pdfs(odds, form_name, start_year, end_year)


        

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