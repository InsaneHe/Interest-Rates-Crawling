import traceback
import time
from datetime import date
import re
import ssl
import random
import requests
from typing import Tuple, List
TODAY = date.today()
from datetime import datetime
from urllib import error
import urllib.request
WEB_TIMEOUT = 10
_context = ssl._create_unverified_context()
def sonia() -> Tuple[List[str], List[str]]:

    D=0
    M=0
    Y=0
    localtime = time.asctime(time.localtime(time.time()))
    Y = localtime[-4:]
    M = localtime[4:7]
    D = re.findall(r'\S+\s+\S+\s+(\S+)\s+', str(localtime))[0]

    url = "https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxAZxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FD=1&FM=Jan&FY=2016&TD=28&TM=Oct&TY=2024&FNY=Y&CSVF=TT&html.x=66&html.y=26&SeriesCodes=IUDSOIA&UsingCodes=Y&Filter=N&title=IUDSOIA&VPD=Y"

    url_0 = r"https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?Travel=NIxAZxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FD=1&FM=Jan&FY=2016&TD={}&TM={}&TY={}&FNY=Y&CSVF=TT&html.x=66&html.y=26&SeriesCodes=IUDSOIA&UsingCodes=Y&Filter=N&title=IUDSOIA&VPD=Y".format(D, M, Y)
    surl = url_0

    def extract(h:str, d:date = TODAY) -> Tuple[List[str], List[str]]:
        try:
            search1st_d_title = [t.lstrip('> ') for t in re.findall(r'<tr>\r\n\t\t<td align="right"(.*?)</td><td align="right">', h)[::-1]]
            search1st_d_dates = re.findall(r'"Date": "(.*?)"', h)[::-1]
            search1st_d_values = re.findall(r'"Value": "(.*?)"', h)[::-1]
            return(search1st_d_title, search1st_d_dates, search1st_d_values,)
        except:
            print('-')

    def internal():
        try:
            headerseand = [{"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"},
                       {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"},
                       {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"},
                       {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"},
                       {"User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"},
                       {"User-Agent": 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
                       {"User-Agent": 'Opera/9.25 (Windows NT 5.1; U; en)'},
                       {"User-Agent": 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
                       {"User-Agent": 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
                       {"User-Agent": 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
                       {"User-Agent": 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
                       {"User-Agent": 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7'},
                       {
                           "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
                       ]
            s = requests.get(url, headers = random.choice(headerseand))
            print(s)
            print_s_text = s.text

            with open ('snrtext.html', mode='w', encoding = 'utf8') as u8w:
                u8w.write(print_s_text)
            return extract(print_s_text)

        except BaseException as bs:
            print(bs)
            return None
    try:
        # local_var_cnt = 0
        connection_req_s = urllib.request.Request(surl)
        connection_res_s = urllib.request.urlopen(connection_req_s, context=_context, timeout=WEB_TIMEOUT)
    except error.HTTPError as ehttp:
        print(ehttp)
        return internal()
    except error.URLError as eurlopen:
        print(eurlopen)

if __name__ == '__main__':
    sonia()