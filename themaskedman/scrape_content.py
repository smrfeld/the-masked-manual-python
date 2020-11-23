from urllib.request import urlopen
from pathlib import Path

def _get_content(url: str) -> str:

    print("Caching: %s ..." % url)
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

def get_content_fda_from_web() -> str:

    url = "https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas"

    return _get_content(url)

def get_content_cdc_n95_from_web(letter : str) -> str:

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

    return _get_content(url)

def write_content_to_cache(content: str, fname: str):

    # Ensure dir exists
    Path('cache/').mkdir(parents=True, exist_ok=True)

    f = open('cache/'+fname,"w")
    f.write(content)
    f.close()

def load_content_from_cache(fname: str) -> str:

    f = open('cache/'+fname, 'r')
    content = f.read()
    f.close()
    return content