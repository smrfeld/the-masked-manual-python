from themaskedman import *

from bs4 import BeautifulSoup
from typing import List, Any
import sys

def print_help_and_exit():
    print("Usage:")
    print("python scrape [OPTIONS]")
    print("")
    print("OPTIONS:")
    print("--from-web")
    print("--from-cache")

    sys.exit(1)

def scrape_fda(masks: List[Mask], from_cache: bool):

    content_fda = ""
    if from_cache:
        content_fda = load_content_from_cache("cache_fda.html")
    else:
        content_fda = get_content_fda_from_web()
        write_content_to_cache(content_fda, "cache_fda.html")
    
    # FDA
    soup_fda = BeautifulSoup(content_fda)
    scrape_fda_authorized_surgical_masks(soup_fda, masks)
    scrape_fda_authorized_imported_non_niosh_respirators_manufactured_in_china(soup_fda, masks)
    scrape_fda_no_longer_authorized(soup_fda, masks)
    scrape_fda_authorized_imported_non_niosh_disposable_filtering_facepiece_respirators(soup_fda, masks)

def scrape_cdc(masks: List[Mask], from_cache: bool):

    # Letters - all alphabetical letters + 3M
    # x,y,z are in one called page yz
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','yz']
    letters = ["3M"] + letters
    # letters = ['a']
    for letter in letters:

        content_cdc = ""
        if from_cache:
            content_cdc = load_content_from_cache("cache_cdc_%s.html" % letter)
        else:
            content_cdc = get_content_cdc_n95_from_web(letter)
            write_content_to_cache(content_cdc, "cache_cdc_%s.html" % letter)
        
        soup_cdc = BeautifulSoup(content_cdc)
        scrape_cdc_niosh_n95(soup_cdc, masks)

def read_open_fda(masks: List[Mask], from_cache: bool):

    # Download data via query if not from cache
    if not from_cache:

        api_key = "eMF4aPNcauk5z6cBe455hsczeXcZzl8yM5tN7FMD"

        query = OpenFDAQuery(api_key)

        total_no_records = query.get_total_no_possible_results()
        print("Total no records: %d" % total_no_records)

        query.run_query(total_no_records)

    # Load cache
    fname = "cache/cache_open_fda.txt"
    data = load_open_fda_cache(fname)
    
    # Make masks
    for entry in data:
        required_fields = ['applicant', 'device_name', 'decision_code']
        has_all_fields = True
        for field in required_fields:
            if not field in entry:
                print("Warning: could not process an entry because of missing field: %s" % field)
                has_all_fields = False

        if not has_all_fields:
            continue

        mask = Mask.createAsSurgicalMaskFDA(
            company=entry['applicant'],
            model=entry['device_name'],
            recalled=entry['decision_code'] == 'SESR'
            )
        masks.append(mask)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print_help_and_exit()

    opt_src = sys.argv[1]
    if opt_src == "--from-web":
        from_cache = False
    elif opt_src == "--from-cache":
        from_cache = True
    else:
        print_help_and_exit()

    masks : List[Mask] = []

    # Scrape FDA
    scrape_fda(masks, from_cache)

    # Scrape CDC
    scrape_cdc(masks, from_cache)
    
    # Scrape FDA
    read_open_fda(masks, from_cache)

    # Print
    print("--- Masks ---")
    for c in masks:
        print(c)

    print("----------------------------")
    print("Result: scraped: %d masks!" % len(masks))

    write_masks_to_file(masks)