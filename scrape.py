from themaskedman import *

from bs4 import BeautifulSoup
from typing import List
import sys

def get_letters_cdc() -> List[str]:
    # Letters - all alphabetical letters + 3M
    # x,y,z are in one called page yz
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','yz']
    letters = ["3M"] + letters
    # letters = ['a']
    return letters

def print_help_and_exit():
    print("Usage:")
    print("python scrape [OPTIONS]")
    print("")
    print("OPTIONS:")
    print("--from-web")
    print("--from-cache")

    sys.exit(1)

def get_content_from_web(cache : Cache):

    # FDA
    content, url, timestamp = get_content_fda_from_web()
    write_scraped_content_to_cache(content, url, timestamp, cache.get_cache_fname_fda())

    # CDC NIOSH
    for letter in get_letters_cdc():
        content, url, timestamp = get_content_cdc_n95_from_web(letter)
        write_scraped_content_to_cache(content, url, timestamp, cache.get_cache_fname_cdc(letter))

    # Open FDA
    api_key = "eMF4aPNcauk5z6cBe455hsczeXcZzl8yM5tN7FMD"
    query = OpenFDAQuery(api_key)

    total_no_records = query.get_total_no_possible_results()
    print("Total no records: %d" % total_no_records)

    content, url, timestamp = query.run_query(total_no_records)
    write_queried_content_to_cache(content, url, timestamp, cache.get_cache_fname_open_fda())

def scrape_fda(masks: List[Mask], cache : Cache):

    # Load content
    content_fda, url, timestamp = load_scraped_content_from_cache(cache.get_cache_fname_fda())
    
    # FDA
    soup_fda = BeautifulSoup(content_fda, features="lxml")
    scrape_fda_authorized_surgical_masks(soup_fda, masks, timestamp, url)
    scrape_fda_authorized_imported_non_niosh_respirators_manufactured_in_china(soup_fda, masks, timestamp, url)
    scrape_fda_no_longer_authorized(soup_fda, masks, timestamp, url)
    scrape_fda_authorized_imported_non_niosh_disposable_filtering_facepiece_respirators(soup_fda, masks, timestamp, url)

def scrape_cdc(masks: List[Mask], cache : Cache):

    for letter in get_letters_cdc():

        # Load content
        content_cdc, url, timestamp = load_scraped_content_from_cache(cache.get_cache_fname_cdc(letter))
        
        soup_cdc = BeautifulSoup(content_cdc, features="lxml")
        scrape_cdc_niosh_n95(soup_cdc, masks, timestamp, url)

def read_open_fda(masks: List[Mask], cache : Cache):
    
    data, url, timestamp = load_queried_content_from_cache(cache.get_cache_fname_open_fda())
    
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
            recalled=(entry['decision_code'] == 'SESR'),
            url_source=url,
            date_last_updated=timestamp
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

    cache = Cache()

    # Get content from web if needed
    if not from_cache:
        cache.move_cache_to_bkup_if_exists()
        try:
            get_content_from_web(cache)
        except:
            print("ERROR: something went wrong!")
            print("Reverting to back-up cache...")
            cache.move_bkup_cache_back()
        cache.remove_bkup_cache_if_exists()

    masks : List[Mask] = []

    # Scrape FDA
    scrape_fda(masks, cache)

    # Scrape CDC
    scrape_cdc(masks, cache)
    
    # Scrape FDA
    read_open_fda(masks, cache)

    # Fix duplicates
    fix_duplicate_companies(masks)

    # Fix models
    fix_model_names(masks)

    # Print
    print("--- Masks ---")
    masks = sorted(masks, key=lambda x: x.company, reverse=False)
    for c in masks:
        print(c)

    print("----------------------------")
    print("Result: scraped: %d masks!" % len(masks))

    write_masks_to_file(masks)