from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas"
page = urlopen(url)
html_bytes = page.read()
content = html_bytes.decode("utf-8")

companies = []

soup = BeautifulSoup(content)
for h4 in soup.findAll('h4'):

    # Check it has correct appendix
    for a in h4.findAll('a', attrs={'id':"appendixa"}):
        print("Found h4: " + str(h4))
        print("- Found correct appendix: " + str(a))
        
        # Search for the table div
        div = h4.find_next_sibling("div", attrs={'class':'lcds-datatable lcds-datatable--ckeditor'})

        # Iterate over table rows
        for tr in div.findAll("tr"):

            # Iterate over cells
            td = tr.find("td")

            if td != None:
                companies.append(td.get_text())

print(companies)