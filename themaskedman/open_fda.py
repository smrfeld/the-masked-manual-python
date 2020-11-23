import requests
import json
from typing import Dict, Any
from pathlib import Path

class OpenFDAQuery:

    def __init__(self, api_key : str, search_params : Dict[str,str]):
        self.api_key = api_key
        self.search_params = search_params

    def run_query_large_limit(self, limit : int):

        limit_each_query = 1000
        skip = 0
        while skip < limit:
            
            print("--- Running query for items: %d to %d ~ total: %d ---" % (skip, skip + limit_each_query, limit))

            # Run query
            self.run_query(
                limit=limit_each_query,
                skip=skip
                )
            
            # Advance
            skip += limit_each_query

    def run_query(self, limit : int, skip : int = 0):
        
        data = self._make_request(
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

    def get_total_no_possible_results(self) -> int:

        # Make request with only 1
        data = self._make_request(
            limit=1,
            skip=0
            )

        total = data['meta']['results']['total']
        return int(total)

    def _make_request(self, limit : int, skip : int) -> Any:

        if limit > 1000:
            raise ValueError("For limits > 1000 use run_query_large_limit")

        # Api Key
        params = ""
        params += "api_key=%s" % api_key
        params += "&search="

        # Replace commas, spaces
        for key, val in self.search_params.items():
            self.search_params[key] = val.replace(',','%2C').replace(' ','%20')

        # Add to params string
        keys = list(self.search_params.keys())
        for i, key in enumerate(keys):
            val = self.search_params[key]
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

            self._strip_registration_numbers(data)

            return data
            
        else:
            print(r.json())
            raise ValueError("Result: error: %d" % r.status_code)

    # 99% of the data is registration numbers
    # We don't care about these so for sanity let's delete them
    # They are under "openfda" / "registration_number"
    def _strip_registration_numbers(self, data : Any):
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

    query = OpenFDAQuery(api_key, search)

    total_no_records = query.get_total_no_possible_results()
    print("Total no records: %d" % total_no_records)

    query.run_query_large_limit(total_no_records)