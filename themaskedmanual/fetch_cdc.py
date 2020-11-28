from .mask import Mask, remove_newlines, ValveType
from typing import List, Any
from datetime import date

def _check_obsolete(model: str) -> bool:
    bad_words = ["Inactive", "Obsolete", "Discontinued"]
    for word in bad_words:
        if word in model:
            return True
    return False

def _check_fda(model: str) -> bool:
    if "(FDA)" in model or "FDA" in model:
        return True
    else:
        return False

def _strip_fda(model: str) -> str:
    return model.replace('(FDA)','').replace('FDA','')

def _strip_company(company: str) -> str:
    s = company

    # Strip anything after external icon
    idx = s.find('external icon')
    s = s[:idx]
    # s = s.replace('external icon','')

    # Strip anything after an opening bracket
    s.rstrip('[')

    return s

def fetch_cdc_niosh_n95(soup : Any, masks : List[Mask], date_last_updated: date, url_source: str):

    for tbody in soup.findAll('tbody'):

        # Iterate over table rows
        for tr in tbody.findAll("tr"):

            # First cell = manufacturer
            td = tr.find("td")
            if td != None:
                company = td.get_text()

                # Strip other text in the company name
                company = _strip_company(company)

                # Get url for company
                url_company = ""
                a_url_company = td.find("a", attrs={'class':'tp-link-policy', 'data-domain-ext':"com"}, href=True)
                if a_url_company != None:
                    url_company = a_url_company['href']

                # Second cell = models, newline separated
                # Also may contain bold statements about discontinued!
                td = td.find_next_sibling("td")
                if td != None:
                    models = td.get_text()

                    # Models are newline seperated
                    models = models.split('\n')
                    
                    # Remove all extra characters
                    models = [remove_newlines(m) for m in models]

                    # Check for inactive
                    obsolete = False
                    for model in models:
                        if _check_obsolete(model):
                            obsolete = True
                            break
                    
                    if obsolete:
                        # Next row in the table
                        continue

                    # Third cell = approval number
                    td = td.find_next_sibling("td")
                    if td != None:
                        # approval_number = remove_newlines(td.get_text())

                        # Fourth cell = yes/no for valve
                        td = td.find_next_sibling("td")
                        if td != None:
                            valve = remove_newlines(td.get_text())
                            if valve == "Yes":
                                valve = ValveType.YES
                            elif valve == "No":
                                valve = ValveType.NO
                            else:
                                valve = ValveType.UNKNOWN

                            # Check for inactive
                            obsolete = False
                            for model in models:
                                if _check_obsolete(model):
                                    obsolete = True
                                    break

                            # Fifth cell = url to instructions
                            url_instructions = ""
                            td = td.find_next_sibling("td")
                            if td != None:
                                a_url_instructions = td.find("a", attrs={'class':'tp-link-policy', 'data-domain-ext':"org"}, href=True)
                                if a_url_instructions != None:
                                    url_instructions = a_url_instructions['href']
                                
                            for model in models:

                                # Check FDA
                                fda = _check_fda(model)
                                model = _strip_fda(model)

                                m = Mask.createAsNioshApprovedN95(
                                    company=company, 
                                    model=model,
                                    fda_approved=fda,
                                    valve_type=valve,
                                    url_company=url_company,
                                    url_instructions=url_instructions,
                                    date_last_updated=date_last_updated,
                                    url_source=url_source
                                    )

                                masks.append(m)