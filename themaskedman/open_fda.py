import requests

api_key = "eMF4aPNcauk5z6cBe455hsczeXcZzl8yM5tN7FMD"

params = ""
params += "api_key=%s" % api_key
params += "&search="

search = {
    'device_name':'Mask, Surgical'
}
for key, val in search.items():
    search[key] = val.replace(',','%2C').replace(' ','%20')

print(search)

keys = list(search.keys())
for i, key in enumerate(keys):
    val = search[key]
    params += '%s:%s' % (key, val)
    if i != len(keys) - 1:
        params += "&"

limit = 5
params += '&limit=%d' % limit

print(params)

r = requests.get('https://api.fda.gov/device/510k.json',params=params)
print(r.url)

if r.status_code == 200:
    data = r.json()
    total = data['meta']['results']['total']
    print('Total no results: %d' % total)
    for res in data['results']:
        print('Applicant: %s' % res['applicant'])
else:
    print("Error: %d" % r.status_code)
