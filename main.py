from argparse import ArgumentParser
from prettytable import PrettyTable
from progressbar import ProgressBar
import api
import files
import nginx

parser = ArgumentParser()
parser.add_argument("-f", "--FileWithIPs", help="textplain file with ip addresses")
parser.add_argument("-d", "--DirNginxLog", help="/var/log/nginx, dir with multiple access.log")
parser.add_argument("-t", "--totalReports", help="display table with totalReports for your IPs from input file")
args = parser.parse_args()


if args.FileWithIPs and not args.DirNginxLog:
	with open(args.FileWithIPs) as f:
		_IPsArray = f.readlines()
elif args.DirNginxLog and not args.FileWithIPs:
	_IPsArray = []
	for parsedLineOfLogfile in nginx.dirParser(args.DirNginxLog):
		_IPsArray.append(parsedLineOfLogfile.get('ip'))


if args.totalReports:
	table = PrettyTable(field_names=["ipAddress", "totalReports"], sortby="totalReports", reversesort=True)
	table.align["ipAddress"] = "l"
	
	with ProgressBar(max_value=len(_FileWithIPs)) as bar:
		for i, _IP in enumerate(_FileWithIPs):
			table.add_row(list(api.totalReports(_IP)))
			bar.update(i)

	print(table)