from .mask import Mask, remove_newlines, ValveType
from typing import List, Any

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

def scrape_cdc_niosh_n95(soup : Any, masks : List[Mask]):

    for tbody in soup.findAll('tbody'):

        # Iterate over table rows
        for tr in tbody.findAll("tr"):

            # First cell = manufacturer
            td = tr.find("td")
            if td != None:
                company = td.get_text()

                # Strip other text in the company name
                company = _strip_company(company)

                # Second cell = models, newline separated
                # Also may contain bold statements about discontinued!
                td = td.find_next_sibling("td")
                if td != None:
                    models = td.get_text()

                    # Models are newline seperated
                    models = models.split('\n')
                    
                    # Remove all extra characters
                    models = [remove_newlines(m) for m in models]

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

                            if obsolete:
                                models = []

                            for model in models:

                                # Check FDA
                                fda = _check_fda(model)
                                model = _strip_fda(model)

                                m = Mask.createAsNioshApprovedN95(
                                    company=company, 
                                    model=model,
                                    fda_approved=fda,
                                    valve_type=valve
                                    )

                                masks.append(m)