from requests import get as r_get
from sys import argv as sys_argv
from prettytable import PrettyTable

url = 'https://api.abuseipdb.com/api/v2/check'

headers = {
    'Accept': 'application/json',
    'Key': 'API_KEY'
}


table = PrettyTable()
table.field_names = ["ipAddress", "totalReports"]
table.sortby = "totalReports"
table.align["ipAddress"] = "l"
table.reversesort = True


with open(sys_argv[1]) as f:
	for _IP in f.readlines():
		try:
			_data = r_get(url=url, headers=headers, params=dict(ipAddress=_IP, maxAgeInDays='365')).json().get('data')
			if _data.get('totalReports'):
				table.add_row([_data.get('ipAddress'), _data.get('totalReports')])
		except:
			print('Unknown error, continue check...')

print(table)