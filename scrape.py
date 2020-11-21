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

    content = ""
    if opt_src == "--from-web":
        content = get_content_from_web()
        write_content_to_cache(content, "cache.html")
    else:
        content = load_content_from_cache("cache.html")

    soup = BeautifulSoup(content)

    masks : List[Mask] = []

    scrape_authorized_imported_non_niosh_respirators_manufactured_in_china(soup, masks)
    scrape_no_longer_authorized(soup, masks)

    for c in masks:
        print(repr(c))

    write_masks_to_file(masks)