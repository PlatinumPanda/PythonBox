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

# recursively fixes ebay's ugly obsession with putting things in lists
def recursive_delist(x):
	if isinstance(x, basestring):
		return x
	else:
		if isinstance(x, list):
			if len(x) == 1:
				return recursive_delist(x[0])
			else:
				return [recursive_delist(item) for item in x]
		if isinstance(x, dict):
			temp = {}
			for key in x:
				temp[key] = recursive_delist(x[key])
			return temp

def parse_ebay_json(ebay_json):
	data = ebay_json['findItemsByKeywordsResponse'][0]
	# fields: itemSearchURL, paginationOutput, ack, timestamp, searchResult, version

	parsed = {}
	parsed['itemSearchURL'] = recursive_delist(data['itemSearchURL'])
	parsed['paginationOutput'] = recursive_delist(data['paginationOutput'])
	parsed['ack'] = recursive_delist(data['ack'])
	parsed['timestamp'] = recursive_delist(data['timestamp'])
	parsed['version'] = recursive_delist(data['version'])
	parsed['numResults'] = int(data['searchResult'][0]['@count'])
	results = recursive_delist(data['searchResult'][0]['item']) #this is an array of item JSON's

	# get one price and condition (standardized)
	for r in results:
		try:
			r['conditionBox'] = r['condition']['conditionDisplayName']
		except KeyError:
			r['conditionBox'] = ""
		try:
			r['priceBox'] = r['sellingStatus']['convertedCurrentPrice']['__value__'] # always in USD (converted)
		except KeyError:
			r['conditionBox'] = ""

	parsed['results'] = results
	return parsed

if __name__ == "__main__":
	# test
	keywords = "pokemon%20charizard%20card%20rare%20mega%20ultra%20bonus"
	parsed = parse_ebay_json(get_from_ebay(keywords))

	print parsed

	print "*********************"

	''' AVAILABLE KEYS FOR EACH RESULT:
	u'itemId', u'isMultiVariationListing', u'subtitle', u'galleryPlusPictureURL', 
	u'globalId', u'title', u'country', u'topRatedListing', u'shippingInfo',
	u'galleryURL', u'autoPay', u'location', u'postalCode', u'returnsAccepted', 
	u'viewItemURL', u'sellingStatus', u'paymentMethod', u'primaryCategory', u'condition', 
	u'listingInfo'
	'''

	# for example, print titles of each result
	for r in parsed['results']:
		print r['title']

	# when was this search last done?
	print parsed['timestamp']