from requests import get, ConnectionError
from argparse import ArgumentParser
from prettytable import PrettyTable
from progressbar import ProgressBar

headers = {
    'Accept': 'application/json',
    'Key': 'API_KEY'
}

url = 'https://api.abuseipdb.com/api/v2/check'

parser = ArgumentParser()
parser.add_argument("-f", "--FileWithIPs", help="file with ip addresses", required=True)
parser.add_argument("-n", "--NginxAccessLog", help="access.log of nginx for parsing") # todo
args = parser.parse_args()

table = PrettyTable(field_names=["ipAddress", "totalReports"], sortby="totalReports", reversesort=True)
table.align["ipAddress"] = "l"

with open(args.FileWithIPs) as f:
	_FileWithIPs = f.readlines()

with ProgressBar(max_value=len(_FileWithIPs)) as bar:
	for i, _IP in enumerate(_FileWithIPs):
		try:
			_data = get(url=url, headers=headers, params=dict(ipAddress=_IP, maxAgeInDays='365')).json().get('data')
		except ConnectionError:
			print('Connection error, continue check...')

		if _data.get('totalReports'):
			table.add_row([_data.get('ipAddress'), _data.get('totalReports')])
			bar.update(i)

print(table)