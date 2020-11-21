from .mask import *
from typing import List, Any

def scrape_fda_authorized_imported_non_niosh_respirators_manufactured_in_china(soup : Any, masks : List[Mask]):

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
                    company = td.get_text()

                    # Second cell = models, comma separated
                    td = td.find_next_sibling("td")
                    if td != None:
                        models = remove_newlines(td.get_text())
                        for model in models.split(','):

                            m = Mask.createAsAuthorizedImportedNonNioshRespiratorsManufacturedInChina(
                                company=company, 
                                model=model,
                                countries_of_origin=["China"]
                                )

                            masks.append(m)

def scrape_fda_no_longer_authorized(soup : Any, masks : List[Mask]):

    for h4 in soup.findAll('h4'):

        # Check it has correct appendix
        for a in h4.findAll('a', attrs={'id':"#nolongerauth"}):
            print("Found h4: " + str(h4))
            print("- Found correct appendix: " + str(a))
            
            # Search for the table div
            div = h4.find_next_sibling("div", attrs={'class':'lcds-datatable lcds-datatable--ckeditor'})

            # Iterate over table rows
            for tr in div.findAll("tr"):

                # First cell = date
                td = tr.find("td")
                if td != None:
                    
                    # Second cell = manufacturer
                    td = td.find_next_sibling("td")
                    if td != None:
                        company = td.get_text()

                        # Third cell = models, comma separated
                        td = td.find_next_sibling("td")
                        if td != None:
                            models = remove_newlines(td.get_text())
                            for model in models.split(','):

                                m = Mask.createAsNoLongerAuthorized(
                                    company=company, 
                                    model=model,
                                    countries_of_origin=["China"]
                                    )

                                masks.append(m)

def scrape_fda_authorized_imported_non_niosh_disposable_filtering_facepiece_respirators(soup : Any, masks : List[Mask]):

    for h4 in soup.findAll('h4'):

        # Check it has correct appendix
        for a in h4.findAll('a', attrs={'id':"#exhibit1"}):
            print("Found h4: " + str(h4))
            print("- Found correct appendix: " + str(a))
            
            # Search for the table div
            div = h4.find_next_sibling("div", attrs={'class':'lcds-datatable lcds-datatable--ckeditor'})

            # Iterate over table rows
            for tr in div.findAll("tr"):

                # First cell = manufacturer
                td = tr.find("td")
                if td != None:
                    company = td.get_text()

                    # Second cell = models, comma separated
                    td = td.find_next_sibling("td")
                    if td != None:
                        models = remove_newlines(td.get_text())

                        # Third cell = country, comma seperated
                        td = td.find_next_sibling("td")
                        if td != None:
                            countries = remove_newlines(td.get_text())

                            for model in models.split(','):

                                m = Mask.createAsAuthorizedImportedNonNioshRespiratorsManufacturedInChina(
                                    company=company, 
                                    model=model,
                                    countries_of_origin=countries.split(',')
                                    )

                                masks.append(m)
