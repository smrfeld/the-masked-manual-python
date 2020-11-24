from os import times
from time import time
import requests
import json
from typing import Any, Tuple
from pathlib import Path
from datetime import date
from .helpers import date_to_str, str_to_date

def write_queried_content_to_cache(content: Any, url: str, timestamp: date, fname: str):

    # Ensure dir exists
    Path('cache/').mkdir(parents=True, exist_ok=True)

    fname_write = 'cache/'+fname
    with open(fname_write, 'w') as f:
        data_write = {
            "content": content,
            "url": url,
            "timestamp": date_to_str(timestamp)
        }
        json.dump(data_write, f)
    print("Wrote to cache: %s" % (fname_write))

def load_queried_content_from_cache(fname: str) -> Tuple[Any,str,date]:

    fname_read = 'cache/'+fname
    with open(fname_read, 'r') as f:
        data = json.load(f)
    
    print("Read data from cache: %s" % fname_read)
    return (data["content"],data["url"],str_to_date(data["timestamp"]))

class OpenFDAQuery:

    def __init__(self, api_key : str):

        self.api_key = api_key
        
    def run_query(self, limit : int) -> Tuple[Any,str,date]:

        limit_each_query = 1000
        skip = 0
        results = []
        while skip < limit:
            limit_this_query = min(limit_each_query,limit-skip)

            print("--- Running query for items: %d to %d ~ total: %d ---" % (skip, skip + limit_this_query, limit))

            results += self._make_request(
                limit=limit_this_query,
                skip=skip
                )['results']

            # Advance
            skip += limit_each_query

        '''
        print("Applicants:")
        for res in data['results']:
            print('   %s' % res['applicant'])
        '''

        return (results, "https://open.fda.gov", date.today())

    def get_total_no_possible_results(self) -> int:

        # Make request with only 1
        data = self._make_request(
            limit=1,
            skip=0
            )

        total = data['meta']['results']['total']
        return int(total)

    def _make_request(self, limit : int, skip : int) -> Any:

        search_params = {
            'openfda.device_name':'Mask'
        }

        if limit > 1000:
            raise ValueError("Limit must be <= 1000")

        # Api Key
        params = ""
        params += "api_key=%s" % self.api_key
        params += "&search="

        # Replace commas, spaces
        # See here:
        # https://www.obkb.com/dcljr/charstxt.html
        '''
        for key, val in search_params.items():
            search_params[key] = val.replace(',','%2C').replace(' ','%20').replace('"','%22')
        '''

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

            self._filter_for_surgical_mask(data)

            self._strip_registration_numbers(data)

            print("Got: %d surgical masks from the %d entries" % (len(data['results']), limit))

            return data
            
        else:
            print(r.json())
            raise ValueError("Result: error: %d" % r.status_code)

    def _filter_for_surgical_mask(self, data : Any):
        i_res = 0
        while i_res < len(data['results']):
            res = data['results'][i_res]

            if "openfda" in res:
                if "device_name" in res["openfda"]:
                    actual = str(res['openfda']['device_name']).lower()
                    check = 'Mask, Surgical'.lower()
                    if actual != check:
                        # Delete
                        del data['results'][i_res]
                        continue
            
            # Next!
            i_res += 1

    # 99% of the data is registration numbers
    # We don't care about these so for sanity let's delete them
    # They are under "openfda" / "registration_number"
    def _strip_registration_numbers(self, data : Any):
        for i_res, res in enumerate(data['results']):
            if "openfda" in res:
                if "registration_number" in res["openfda"]:
                    del res["openfda"]["registration_number"]
                    data['results'][i_res] = res
                if "fei_number" in res["openfda"]:
                    del res["openfda"]["fei_number"]
                    data['results'][i_res] = res