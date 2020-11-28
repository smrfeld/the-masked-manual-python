from urllib.request import urlopen
from typing import Tuple
from datetime import date
import json
from .helpers import date_to_str, str_to_date

def _get_content(url: str) -> str:

    print("Caching: %s ..." % url)
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

def get_content_fda_from_web() -> Tuple[str,str,date]:

    url = "https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas"

    return (_get_content(url), url, date.today())

def get_content_cdc_n95_from_web(letter : str) -> Tuple[str,str,date]:

    url = "https://www.cdc.gov/niosh/npptl/topics/respirators/disp_part/N95list1"
    if letter.lower() == "3m":
        url += ".html"
    elif letter.lower() in ['a','b','c','d','e','f','g','h','i']:
        url += "-" + letter.lower() + ".html"
    elif letter.lower() == 'j':
        url += "sect2.html"
    elif letter.lower() in ['k','l','m','n','o','p','q','r']:
        url += "sect2-" + letter.lower() + ".html"
    elif letter.lower() == 's':
        url += "sect3.html"
    else:
        url += "sect3-" + letter.lower() + ".html"

    return (_get_content(url), url, date.today())

def write_scraped_content_to_cache(content: str, url: str, timestamp: date, fname: str):

    with open(fname, 'w') as f:
        data_write = {
            "content": content,
            "url": url,
            "timestamp": date_to_str(timestamp)
        }
        json.dump(data_write, f)
    print("Wrote to cache: %s" % (fname))

def load_scraped_content_from_cache(fname: str) -> Tuple[str,str,date]:

    fname_read = fname
    with open(fname, 'r') as f:
        data = json.load(f)
    
    print("Read data from cache: %s" % fname_read)
    return (data["content"],data["url"],str_to_date(data["timestamp"]))