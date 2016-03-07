#!/usr/bin/env python
#coding: utf-8

import requests
import re
import os
import urllib
import gevent
from gevent import monkey; monkey.patch_socket()
from gevent.pool import Pool


"""
get item name and url from main page

return array of dict
"""
def index_items(html_content):
    page_items = []
    p = re.compile(r'</a><span><a href=\"(.*?)\" target="_blank">(.*?)</a></span>')
    results = p.findall(html_content)
    for item in results:
        dict = {}
        dict['url'] = item[0]
        dict['title'] = item[1]
        page_items.append(dict)
    return page_items

'''
find item's num of page
'''
def total_page(html_content):
    p = re.compile(r'<span>(\d*)</span>')
    results = p.findall(html_content)
    return results[len(results)-1]

'''
download image
'''
def download_mzitu(item, num):
    pic_path = u'mzitu/%s' % item['title']
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
        print '-----> make dir %s ' % pic_path
    target = pic_path + u'/%s.jpg' % num

    url = item['url']+'/%d' % num
    content = requests.get(url)
    r = re.compile(r'<img src=\"(.*?)\" alt=\"(.*?)\" /></a>')
    results = r.findall(content.text)
    for match_item in results:
        print '  download %d ....   ' % num
        try:
            urllib.urlretrieve(match_item[0], target)
        except Exception, e:
            print e

        print 'finish  %d download' % num



print u"""#---------------------------------------
#   程序：mzitu爬虫
#   版本：0.1
#   作者：Phillip Song
#   日期：2016-02-09
#   语言：Python 2.7
#   操作：自动抓取mzitu图片
#   功能：将图片保存至mzitu目录
#---------------------------------------
"""
for page in range(5, 10):
    request_url = 'http://www.mzitu.com/page/%d' % page
    r = requests.get(request_url)
    total_items = index_items(r.text)
    gpool = Pool(40)
    print '===== page %d ======' % page
    for item in total_items:
        item_content = requests.get(item['url'])
        total_pages = total_page(item_content.text)
        print '  ----- %s ----- ' % item['title']
        #task_array = []
        for pic_num in range(1, int(total_pages)+1):
            # task = gevent.spawn(download_mzitu, item, pic_num)
            # task_array.append(task)
            gpool.spawn(download_mzitu, item, pic_num)
        gpool.join()

