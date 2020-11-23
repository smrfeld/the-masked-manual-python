from .mask import Mask, remove_newlines, ValveType
from typing import List, Any

def scrape_fda_authorized_surgical_masks(soup : Any, masks : List[Mask]):

    for h4 in soup.findAll('h4'):

        # Check it has correct appendix
        a = h4.find('a', attrs={'id':"appendixasurgicalmasks"})
        if a != None:
            print("Found correct section: " + str(h4))
            
            # Search for the table div
            div = h4.find_next_sibling("div", attrs={'class':'lcds-datatable lcds-datatable--ckeditor'})

            # Iterate over table rows
            for tr in div.findAll("tr"):

                # First cell = date of addition
                td = tr.find("td")
                if td != None:
                    date = td.get_text()

                    # Second cell = company
                    td = td.find_next_sibling("td")
                    if td != None:
                        company = td.get_text()

                        # Third cell = models, newline separated
                        td = td.find_next_sibling("td")
                        if td != None:
                            models = td.get_text()

                            # Models are newline seperated
                            models = models.split('\n')
                            
                            # Remove all extra characters
                            models = [remove_newlines(m) for m in models]

                            # Fix pairs of lines that look like this:
                            # Surgical Mask - Disposable Single-Use 3-Ply Earloop
                            # Model #: EcoGuard B ECO01
                            i_model = 0
                            while i_model < len(models):
                                model = models[i_model]
                                if len(model) > 8 and model[0:8] == "Model #:":
                                    if i_model > 0:
                                        # Remove
                                        del models[i_model-1]
                                        continue
                                
                                # Delete empty lines
                                if model == '':
                                    del models[i_model]
                                    continue
                                    
                                # Next!
                                i_model += 1

                            for model in models:

                                m = Mask.createAsSurgicalMaskEua(
                                    company=company, 
                                    model=model
                                    )

                                masks.append(m)

def scrape_fda_authorized_imported_non_niosh_respirators_manufactured_in_china(soup : Any, masks : List[Mask]):

    for h4 in soup.findAll('h4'):

        # Check it has correct appendix
        a = h4.find('a', attrs={'id':"appendixa"})
        if a != None:
            print("Found correct section: " + str(h4))
            
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

                            m = Mask.createAsAuthorizedImportedNonNioshRespirators(
                                company=company, 
                                model=model,
                                countries_of_origin=["China"]
                                )

                            masks.append(m)

def scrape_fda_no_longer_authorized(soup : Any, masks : List[Mask]):

    for h4 in soup.findAll('h4'):

        # Check it has correct appendix
        a = h4.find('a', attrs={'id':"#nolongerauth"})
        if a != None:
            print("Found correct section: " + str(h4))
            
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
        a = h4.find('a', attrs={'id':"#exhibit1"})
        if a != None:
            print("Found correct section: " + str(h4))
            
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

                                m = Mask.createAsAuthorizedImportedNonNioshRespirators(
                                    company=company, 
                                    model=model,
                                    countries_of_origin=countries.split(',')
                                    )

                                masks.append(m)