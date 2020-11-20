from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List

def remove_newlines(s : str) -> str:
    return s.replace('\n',"").replace('\xa0',"")

class Manufacturer:
    def __init__(self, name : str):
        self.name = remove_newlines(name)
        self.models : List[str] = []

    def set_models_from_comma_sep_str(self, full_str : str):
        full_str = remove_newlines(full_str)
        for s in full_str.split(','):
            self.models.append(s)

    def __repr__(self): 
        return "%s: %s" % (self.name, ','.join(self.models))

    def __str__(self):
        return self.name

url = "https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas"
page = urlopen(url)
html_bytes = page.read()
content = html_bytes.decode("utf-8")

companies : List[Manufacturer] = []

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

            # First cell = manufacturer
            td = tr.find("td")
            if td != None:
                company = Manufacturer(name=td.get_text())

                # Second cell = models, comma separated
                td = td.find_next_sibling("td")
                if td != None:
                    company.set_models_from_comma_sep_str(td.get_text())

                # Save company
                companies.append(company)

for c in companies:
    print(repr(c))