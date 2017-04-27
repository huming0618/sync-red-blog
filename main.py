import os

import requests
from urllib import quote,unquote
import cookielib

import json
import execjs
import datetime

try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS

try:
    import json
except ImportError:
    import simplejson as json
from config import config

def get_archive_list(ts, count):
    None

def sync():
    cookieFile = 'cookie'
    cookiejar = cookielib.MozillaCookieJar(cookieFile)
    headers = {
        'Referer': config['referUrl'],
        'Accept-Language': 'zh-CN',
        'Host': config['host'],
        'User-Agent': 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0',
        'Connection': 'Keep-Alive'
    }

    session = requests.Session()
    resp = session.get(config['indexUrl'], headers=headers, cookies=cookiejar)
    result = resp.text

    pageHtml = BS(result)
    data_js = pageHtml.body.find('textarea',attrs={'name':'js'}).text


    ctx = execjs.compile(data_js + "\nvar get = function(){return this.p}")
    js_data = ctx.call('get');

    for item in js_data['a']:
        print item['archDate'], ',', item['count']

if __name__ == "__main__":
    sync()
