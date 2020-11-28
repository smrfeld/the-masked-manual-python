from .mask import Mask
from typing import List

class Company:
    def __init__(self, name: str, masks: List[Mask]):
        self.name = name
        self.masks = masks

def fix_duplicate_companies(masks: List[Mask]):
    
    # List of companies to masks
    company_names = [mask.company for mask in masks]
    # Delete duplicates
    company_names = list(dict.fromkeys(company_names))
    # Make objects
    companies : List[Company] = []
    for company_name in company_names:
        # Get masks
        company_masks = [mask for mask in masks if mask.company == company_name]
        # Make company
        companies.append(Company(
            name=company_name,
            masks=company_masks
        ))

    # Sort by company name
    companies = sorted(companies, key=lambda x: x.name, reverse=False)

    # Go through every company
    i_company = 0
    while i_company < len(companies):
        ci = companies[i_company]
        ni = ci.name

        # Check every other company name
        print("Findind duplicates for: %s" % ci.name)
        j_company = i_company + 1
        while j_company < len(companies):
            cj = companies[j_company]
            nj = cj.name

            # Strip periods, commas, lowercase
            ni = _strip_extra_words_in_company_name(ni)
            nj = _strip_extra_words_in_company_name(nj)

            # Check for match
            if ni == nj:
                
                print("Found duplicate company: %s is a duplicate of %s" % (cj.name, ci.name))

                # Match!
                # Fix all mask names in cj masks
                for mask in cj.masks:
                    mask.company = ci.name

                # Delete company
                del companies[j_company]
            else:
                # Next!
                j_company += 1
        
        # Next!
        i_company += 1

def _strip_extra_words_in_company_name(s_in : str) -> str:
    s = s_in

    # Lowercase
    s = s.lower()

    # Commas, periods, paretheses
    # Replace with spaces to fix problems such as co.ltd. -> co ltd
    s = s.replace('.',' ').replace(',',' ').replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('&',' ')

    # International
    phrases_remove = [
        'health care',
        'automatic disposable',
        'professional products',
        'safety products',
        'filter technologies'
    ]
    for phrase in phrases_remove:
        s = s.replace(phrase, '')

    # Words cut
    words_cut = [
        'industries',
        'healthcare',
        'international',
        'co',
        'ltd',
        'limited',
        'coltd',
        'company',
        'asia',
        'inc',
        'intl',
        'llc',
        'medical',
        'corp',
        'corporation',
        'and',
        'japan',
        'health',
        'safety',
        'trading',
        'america',
        'ag'
    ]
    sp = s.split()
    sp = [x for x in sp if not x in words_cut]
    s = ' '.join(sp)

    # Strip words after aka
    sp = s.split()
    if 'aka' in sp:
        idx = sp.index('aka')
        sp = sp[:idx]
    s = ' '.join(sp)

    # Fix double spaces
    s = s.replace('  ', ' ')

    # Remove leading/trailing spaces
    s = s.strip()

    return s
