from requests import get, ConnectionError

headers = {
    'Accept': 'application/json',
    'Key': 'API_KEY'
}

if headers.get('Key') == 'API_KEY': print('Error, you need insert API_KEY in api.py'); exit()

url = 'https://api.abuseipdb.com/api/v2/check'

def totalReports(__ip):
	try:
		__data = get(url=url, headers=headers, params=dict(ipAddress=__ip, maxAgeInDays='365')).json().get('data')
	except ConnectionError:
		print('Connection error')

	if __data.get('totalReports'):
		return __data.get('ipAddress'), __data.get('totalReports')
	else:
		return None