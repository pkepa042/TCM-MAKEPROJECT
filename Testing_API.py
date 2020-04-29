import requests, pprint

request = requests.get('https://api.covid19api.com/summary')
pprint.pprint(request.text)
