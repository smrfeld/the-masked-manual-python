import requests
import json
from typing import Any, List
from pathlib import Path
from .mask import Mask

class OpenFDAQuery:

    def __init__(self, api_key : str):

        self.cache_dir = "cache"
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

        self.api_key = api_key
        
    def run_query(self, limit : int):

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

        # Write to cache
        fname = self.cache_dir + ('/cache_open_fda.txt')
        with open(fname, 'w') as outfile:
            print("Wrote to cache: %s" % fname)
            json.dump(results, outfile)
        
        '''
        print("Applicants:")
        for res in data['results']:
            print('   %s' % res['applicant'])
        '''

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

def load_open_fda_cache(fname : str) -> Any:
    with open(fname, 'r') as f:
        data = json.load(f)
    return data