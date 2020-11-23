import requests
import json
from typing import Dict, Any
from pathlib import Path

def run_query_large_limit(api_key : str, search_params : Dict[str,str], limit : int):

    limit_each_query = 1000
    skip = 0
    while skip < limit:
        
        print("--- Running query for items: %d to %d ~ total: %d ---" % (skip, skip + limit_each_query, limit))

        # Run query
        run_query(
            api_key=api_key, 
            search_params=search_params,
            limit=limit_each_query,
            skip=skip
            )
        
        # Advance
        skip += limit_each_query

def run_query(
    api_key : str, 
    search_params : Dict[str,str], 
    limit : int, 
    skip : int = 0):
    
    data = _make_request(
        api_key=api_key,
        search_params=search_params,
        limit=limit,
        skip=skip
        )

    # Write to cache
    Path("cache_open_fda").mkdir(parents=True, exist_ok=True)
    fname = 'cache_open_fda/skip_%08d.txt' % skip
    with open(fname, 'w') as outfile:
        print("Wrote to cache: %s" % fname)
        json.dump(data, outfile)

    '''
    print("Applicants:")
    for res in data['results']:
        print('   %s' % res['applicant'])
    '''

def get_total_no_possible_results(
    api_key : str, 
    search_params : Dict[str,str]
    ) -> int:

    # Make request with only 1
    data = _make_request(
        api_key=api_key,
        search_params=search_params,
        limit=1,
        skip=0
        )

    total = data['meta']['results']['total']
    return int(total)

def _make_request(
    api_key : str, 
    search_params : Dict[str,str], 
    limit : int, 
    skip : int) -> Any:

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
    keys = list(search_params.keys())
    for i, key in enumerate(keys):
        val = search_params[key]
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

        _strip_registration_numbers(data)

        return data
        
    else:
        print(r.json())
        raise ValueError("Result: error: %d" % r.status_code)

# 99% of the data is registration numbers
# We don't care about these so for sanity let's delete them
# They are under "openfda" / "registration_number"
def _strip_registration_numbers(data : Any):
    for i_res, res in enumerate(data['results']):
        if "openfda" in res:
            if "registration_number" in res["openfda"]:
                del res["openfda"]
                data['results'][i_res] = res

if __name__ == "__main__":

    api_key = "eMF4aPNcauk5z6cBe455hsczeXcZzl8yM5tN7FMD"

    search = {
        'device_name':'Mask, Surgical'
    }


    total_no_records = get_total_no_possible_results(api_key, search)
    print("Total no records: %d" % total_no_records)

    run_query_large_limit(api_key, search, total_no_records)