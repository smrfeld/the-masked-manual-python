from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List
import json
import sys

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

    def to_json(self):
        return {
            'name': self.name,
            'models': self.models
        }

def get_content_from_web() -> str:

    url = "https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas"
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

def write_content_to_cache(content: str, fname: str):

    f = open(fname,"w")
    f.write(content)
    f.close()

def load_content_from_cache(fname: str) -> str:

    f = open(fname, 'r')
    content = f.read()
    f.close()
    return content

def print_help_and_exit():
    print("Usage:")
    print("python scrape [OPTIONS]")
    print("")
    print("OPTIONS:")
    print("--from-web")
    print("--from-cache")

    sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print_help_and_exit()

    opt_src = sys.argv[1]
    if opt_src != "--from-web" and opt_src != "--from-cache":
        print_help_and_exit()

    content = ""
    if opt_src == "--from-web":
        content = get_content_from_web()
        write_content_to_cache(content, "cache.html")
    else:
        content = load_content_from_cache("cache.html")

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

    data = {}
    data['masks'] = []
    for c in companies:
        for m in c.models:
            data['masks'].append({
                'company': c.name,
                'model': m
            })

    with open('data.txt','w') as outfile:
        json.dump(data,outfile)