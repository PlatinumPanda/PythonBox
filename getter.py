import requests
from requests.exceptions import HTTPError

def get_from_ebay(keywords):
	app_id = "Platinum-dbd7-41d0-89bf-d6e6bf69ea8f" ### HARDCODED APP ID ###
	request_url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0" + "&SECURITY-APPNAME=" + app_id + "&RESPONSE-DATA-FORMAT=JSON" + "&REST-PAYLOAD" + "&keywords=" + keywords

	print request_url
	try:
	    r = requests.get(request_url)
	    r.raise_for_status()
	    return r.json()

	except HTTPError:
		print 'Could not download page'
		return None
	else:
	    print r.url, 'downloaded successfully'
	    return None

def parse_ebay_json(ebay_json):
	data = ebay_json['findItemsByKeywordsResponse'][0]
	# fields: itemSearchURL, paginationOutput, ack, timestamp, searchResult, version

	parsed = {}
	parsed['itemSearchURL'] = data['itemSearchURL']
	parsed['paginationOutput'] = data['paginationOutput']
	parsed['ack'] = data['ack']
	parsed['timestamp'] = data['timestamp']
	parsed['version'] = data['version']
	parsed['numResults'] = int(data['searchResult'][0]['@count'])
	parsed['results'] = data['searchResult'][0]['item'] #this is an array of item JSON's

	return parsed

if __name__ == "__main__":
	keywords = "pokemon%20charizard%20card%20rare%20mega%20ultra%20bonus"
	parsed = parse_ebay_json(get_from_ebay(keywords))

	# print titles of each result
	for r in parsed['results']:
		print r['title']
	print parsed['timestamp']