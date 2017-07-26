#coding=utf8
import os
import io

import requests
from urllib import quote,unquote
import cookielib

import json
import execjs
import datetime

import shutil 

try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS

try:
    import json
except ImportError:
    import simplejson as json
from config import config

def grab(result):
    pageHtml = BS(result)

    #print result

    postDateSpan = pageHtml.select('span.pleft span.blogsep')[0]
    #print postDateSpan.text

    postTitleSpan = pageHtml.select('h3.title span.tcnt')[0]
    #print postTitleSpan.text

    postContentDiv = pageHtml.select('div.nbw-blog')[0]
    #print postContentDiv.prettify()

    return postDateSpan.text, postTitleSpan.text, postContentDiv.prettify()

def read_urls():
    urlList = []
    with open('urls.txt') as urlsFile:
        urlList = urlsFile.readlines()
    
    return urlList

def sync_post():
    urls = read_urls()

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
    
    shutil.rmtree('output')
    os.mkdir('output')
    
    for url in urls:
        postUrl = url.strip().rstrip('/')
        resp = session.get(postUrl, headers=headers, cookies=cookiejar)
        result = resp.text
        postDateText, postTitle, postContent = grab(result)
  
        outputPath = os.path.join('output', postDateText + '_' + postTitle + '.html')
        with io.open(outputPath, 'w') as temp:
            temp.write(postContent)
 


    #print result
    # with io.open('output/temp.html', 'w', encoding='gbk') as temp:
    #     temp.write(result)

if __name__ == "__main__":
    sync_post()
