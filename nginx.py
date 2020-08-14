import gzip
import lzma
import os
import sys
import re
from datetime import datetime
import pytz

tz = pytz.timezone('UTC')

#INPUT_DIR = "/var/log/nginx"
#BASE_DIR = Path(__file__).resolve().parent

NGINX_REGEX = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<remoteuser>.+) \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(?P<method>.+) )(?P<url>.+)(http\/[1-2]\.[0-9]")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)

def fileParser(__fileobj):
    try:
        for line in __fileobj.readlines():
            data = re.search(NGINX_REGEX, str(line))
            if data:
                datadict = data.groupdict()
                ip = datadict["ipaddress"]
                datetimeobj = datetime.strptime(datadict["dateandtime"], "%d/%b/%Y:%H:%M:%S %z") # Converting string to datetime obj
                url = datadict["url"]
                bytessent = datadict["bytessent"]
                referrer = datadict["refferer"]
                useragent = datadict["useragent"]
                status = datadict["statuscode"]
                method = data.group(6)

                return dict(ip=ip, date=tz.normalize(datetimeobj), url=url, bytessent=bytessent,
                    referrer=referrer, useragent=useragent, status_code=status_code, method=method)
    except:
        print('Error, fileParser in nginx.py')
        exit()
    finally:
        __fileobj.close()


def detectCompressionType(__filepath):
    if f.endswith(".gz"):
        return gzip.open(__filepath, errors=None)
    elif f.endswith(".xz"):
        return lzma.open(__filepath, encoding='utf-8', errors=None)
    else:
        return open(__filepath, errors=None)


def dirParser(__INPUT_DIR):
    __result_array = []
    for __file in os.listdir(__INPUT_DIR):
        __result_array.append(fileParser(detectCompressionType(
                os.path.join(INPUT_DIR, __file)
                )))
    return __result_array