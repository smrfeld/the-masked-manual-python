import requests
from typing import Dict

def run_query_large_limit(api_key : str, search_params : Dict[str,str], limit : int):

    limit_each_query = 1000
    skip = 0
    while skip < limit:

        # Run query
        run_query(
            api_key=api_key, 
            search_params=search_params,
            limit=limit_each_query,
            skip=skip
            )
        
        # Advance
        skip += limit_each_query

def run_query(api_key : str, search_params : Dict[str,str], limit : int, skip : int = 0):
    
    if limit > 1000:
        raise ValueError("For limits > 1000 use run_query_large_limit")

    # Api Key
    params = ""
    params += "api_key=%s" % api_key
    params += "&search="

    # Replace commas, spaces
    for key, val in search_params.items():
        search_params[key] = val.replace(',','%2C').replace(' ','%20')

    # Add to params string
    keys = list(search.keys())
    for i, key in enumerate(keys):
        val = search[key]
        params += '%s:%s' % (key, val)
        if i != len(keys) - 1:
            params += "&"

    # Limit
    params += '&limit=%d' % limit

    # Skip
    params += '&skip=%d' % skip

    r = requests.get('https://api.fda.gov/device/510k.json',params=params)
    print("Made request to URL:")
    print(r.url)

    if r.status_code == 200:
        print("Result: success.")

        data = r.json()
        total = data['meta']['results']['total']
        print('   Total no results: %d' % total)

        print("   Applicants:")
        for res in data['results']:
            print('      %s' % res['applicant'])
        
    else:
        print("Result: error: %d" % r.status_code)
        print(r.json())

if __name__ == "__main__":

    api_key = "eMF4aPNcauk5z6cBe455hsczeXcZzl8yM5tN7FMD"

    search = {
        'device_name':'Mask, Surgical'
    }

    run_query_large_limit(api_key, search, 10366)