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

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print_help_and_exit()

    opt_src = sys.argv[1]
    if opt_src != "--from-web" and opt_src != "--from-cache":
        print_help_and_exit()

    masks : List[Mask] = []

    '''
    content_fda = ""
    if opt_src == "--from-web":
        content_fda = get_content_fda_from_web()
        write_content_to_cache(content_fda, "cache_fda.html")
    else:
        content_fda = load_content_from_cache("cache_fda.html")

    # FDA
    soup_fda = BeautifulSoup(content_fda)
    scrape_fda_authorized_imported_non_niosh_respirators_manufactured_in_china(soup_fda, masks)
    scrape_fda_no_longer_authorized(soup_fda, masks)
    scrape_fda_authorized_imported_non_niosh_disposable_filtering_facepiece_respirators(soup_fda, masks)
    '''

    # Letters - all alphabetical letters + 3M
    # x,y,z are in one called page yz
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','yz']
    letters = ["3M"] + letters
    for letter in letters:

        content_cdc = ""
        if opt_src == "--from-web":
            content_cdc = get_content_cdc_n95_from_web(letter)
            write_content_to_cache(content_cdc, "cache_cdc_%s.html" % letter)
        else:
            content_cdc = load_content_from_cache("cache_fda_%s.html" % letter)


    for c in masks:
        print(repr(c))

    write_masks_to_file(masks)