from bs4 import BeautifulSoup
from urllib.request import urlopen

import math

#note:input- tax form name and range of years

#download the pdfs available in that range into a subdirectory under scripts main directory
#name of the form, and the file name should be
#the "Form Name - Year" (ex: Form W-2/Form W-2 - 2020.pdf)

#first I need a methodical approach for getting the form in the year numbers, 
# for example use: for year in range(2017,2020):
    #go to this url(factor in year)
    #make sure the names match!!!!
