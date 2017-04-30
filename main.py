#coding=utf8
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


def get_archive_list(session, ts, count):
    # callCount=1
    # scriptSessionId=${scriptSessionId}187
    # c0-scriptName=BlogBeanNew
    # c0-methodName=getBlogsByArchive
    # c0-id=0
    # c0-param0=number:32617477
    # c0-param1=number:1280592000000
    # c0-param2=number:0
    # c0-param3=number:14
    # batchId=522470

    payload = [
        'callCount=1',
        'scriptSessionId=${scriptSessionId}187',
        'c0-scriptName=BlogBeanNew',
        'c0-methodName=getBlogsByArchive',
        'c0-id=0',
        'c0-param0=number:32617477',
        'c0-param1=number:%s' % ts ,
        'c0-param2=number:0',
        'c0-param3=number:%d' % count,
        'batchId=522470'
    ]

    headers = {
        'content-type': 'text/plain',
        'Origin': 'http://api.blog.163.com',
        'Refer': 'http://api.blog.163.com/crossdomain.html',
        'Host': 'api.blog.163.com',
        'User-Agent': config['userAgent'],
        'Connection': 'Keep-Alive',
        'Accept': "*/*",
        'Accept-Encoding': "gzip, deflate"
    }

    print "\n".join(payload)
    resp = session.post(config['archiveAPIUrl'], "\n".join(payload), headers=headers)
    print resp.text

def sync():
    cookieFile = 'cookie'
    cookiejar = cookielib.MozillaCookieJar(cookieFile)
    headers = {
        'Referer': config['referUrl'],
        'Accept-Language': 'zh-CN',
        'Host': config['host'],
        'User-Agent': config['userAgent'],
        'Connection': 'Keep-Alive'
    }

    session = requests.Session()
    resp = session.get(config['indexUrl'], headers=headers, cookies=cookiejar)
    result = resp.text

    pageHtml = BS(result)
    data_js = pageHtml.body.find('textarea',attrs={'name':'js'}).text


    ctx = execjs.compile(data_js + "\nvar get = function(){return this.p}")
    js_data = ctx.call('get');

    for item in js_data['a'][0:2]:
        print item['archDate'], ',', item['count']
        get_archive_list(session, item['archDate'], item['count'])

def sync_post():
    cookieFile = 'cookie'
    cookiejar = cookielib.MozillaCookieJar(cookieFile)
    headers = {
        'Referer': config['referUrl'],
        'Accept-Language': 'zh-CN',
        'Host': config['host'],
        'User-Agent': config['userAgent'],
        'Connection': 'Keep-Alive'
    }

    session = requests.Session()
    postUrl = "http://winniedezhu.blog.163.com/blog/static/32617477201072583247570/"
    resp = session.get(postUrl, headers=headers, cookies=cookiejar)
    result = resp.text

    pageHtml = BS(result)
    #print result
    with open('temp.html', 'w') as temp:
        temp.write(result.encode('gbk'))

if __name__ == "__main__":
    sync_post()
