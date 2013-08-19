#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import re
import redis
REDISTIMES = 15
PARAMS = { 
        'host':"http://bbs.byr.cn/",
        'board':"board/JobInfo?p=",
        'headers':{"X-Requested-With" : "XMLHttpRequest"},
        'href':r'\"([\w/\d]+)\"'
        }
def spider(host, board, pages, headers, href):
    r = requests.get(host+board+pages, headers=headers)
    soup = BeautifulSoup(r.text)
    info = soup.findAll('a', href=re.compile(r"/article/JobInfo/\d+"), title=None)
    for i in info:
        if i.parent.parent.get("class") == "top":
            continue
        else:
            url = host + re.findall(href, str(i))[0]
            title = re.findall(r'>(.+)<', str(i))[0]
            print url, title
            rd.sadd('url', url+'   '+title)

def main():

    rd.incr('times')
    if rd.get('times') >= REDISTIMES:
        rd.flushall()
    for pages in xrange(3):
        spider(PARAMS['host'], PARAMS['board'], str(pages), PARAMS['headers'], PARAMS['href'])

if __name__ == "__main__":
    rd = redis.StrictRedis('localhost', port = 6379)
    main()
    print ''.join(rd.smembers('url'))
