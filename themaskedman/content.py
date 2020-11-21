from urllib.request import urlopen

def get_content_from_web() -> str:

    url = "https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/personal-protective-equipment-euas"
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

def write_content_to_cache(content: str, fname: str):

    f = open(fname,"w")
    f.write(content)
    f.close()

def load_content_from_cache(fname: str) -> str:

    f = open(fname, 'r')
    content = f.read()
    f.close()
    return content