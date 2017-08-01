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
    from BeautifulSoup import BeautifulSoup as BS, Tag
except ImportError:
    from bs4 import BeautifulSoup as BS, Tag

try:
    import json
except ImportError:
    import simplejson as json
from config import config
from bookmaker import bookmaker

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
    
    theBookmaker = bookmaker()
    theBookmaker.writeTitle(u'你好吗')
    theBookmaker.writeCoverImage('cover.jpg')
    theBookmaker.writeTOCTitle(u'目录')
    theBookmaker.writeAuthor(u'四号楼的鱼')
    theBookmaker.writePublisher(u'Dear Peter')

    total = len(urls)
    for i, url in enumerate(reversed(urls)):
        postUrl = url.strip().rstrip('/')
        resp = session.get(postUrl, headers=headers, cookies=cookiejar)
        result = resp.text

        try:
            postDateText, postTitle, postContent = grab(result)
    
            chapter_name = 'ch_' + str(i)
            theBookmaker.writeTOCFileLinkItem(postTitle, chapter_name + '.html', '')
            theBookmaker.writeNavPointFileLinkItem(postTitle, chapter_name + '.html', chapter_name, i+3)
            theBookmaker.writeChapter(chapter_name, postTitle, postContent, postDateText)

            if i > 5:
                break

            print "\n"*100
            print 'Processed %d/%d'%(i,total)
            # outputPath = os.path.join('output', postDateText + '_' + postTitle + '.html')
            # with io.open(outputPath, 'w') as temp:
            #     temp.write(postContent)
        except Exception, e:
            print "Error Occured for URL [%s] with message %s" % (url, e.message)
            print e
 

    theBookmaker.seal()
    #print result
    # with io.open('output/temp.html', 'w', encoding='gbk') as temp:
    #     temp.write(result)

if __name__ == "__main__":
    # from jinja2 import Environment, FileSystemLoader, select_autoescape
    # env = Environment(
    #     loader=FileSystemLoader(searchpath='template')
    # )
    # tpl = env.get_template('chapter.html')
    # print tpl.render(title='my title', content='this is the content <b>bold</b>')
    sync_post()
