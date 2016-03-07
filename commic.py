#!/usr/bin/env python
#coding: utf-8
import os
import urllib
from tornado_fetcher import Fetcher
from bs4 import BeautifulSoup

BASE_URL = 'http://jj.xxdm.org/manhua/jjdjrmh/%d.shtml?%d'
# BASE_URL = 'http://www.xxdm.org/mh/qzlrmh/339.shtml?%d'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"

fetcher = Fetcher(
    user_agent=USER_AGENT,
    phantomjs_proxy='http://localhost:12306',
    pool_size=10,
    async=False
)

def get_total_page(content):
    html = content['content']
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find_all("font", attrs={"color" : "red"})
    totalNum = 0
    for page in pages:
        totalNum = page.get_text()
        break
    return totalNum

def get_img_url(content):
    html = content['content']
    soup = BeautifulSoup(html, "lxml")
    imgLink = ''
    imgs = soup.find_all("img", attrs={"id" : "imgPic"})
    for img in imgs:
        imgLink = img.get('src')
    return imgLink


def download_img(url, num, pic_path):
    if not os.path.exists(pic_path):
        os.makedirs(pic_path)
        print '-----> make dir %s <------' % pic_path
    target = pic_path + u'/%s.png' % num
    urllib.urlretrieve(url, target)

def get_and_download(page, chapter):
    request_url = BASE_URL % (chapter, page)
    html = fetcher.phantomjs_fetch(request_url)
    img_url = get_img_url(html)
    print img_url
    download_img(img_url, page, 'jjdjr/chapter' + str(chapter))


if __name__ == '__main__':
    print u"""#---------------------------------------
#   程序：Commic Spider
#   版本：0.1
#   作者：Phillip Song
#   日期：2016-03-06
#   语言：Python 2.7
#   操作：自动抓取xxdm漫画章节
#   功能：将漫画按章节保存在本地
#   注意: 有的章节可能因为版权原因无法下载
#---------------------------------------
"""
    while True:
        start_chapter = int(raw_input(u'Please input start chapter: '))
        end_chapter = int(raw_input(u'Please input end chapter: '))
        if (start_chapter < 0) or (end_chapter < 0) or (start_chapter > end_chapter):
            print 'Wrong chapters! Input them again.'
        else:
            break

    for chapter in range(start_chapter, end_chapter + 1):
        url = BASE_URL %(chapter, 1)
        content = fetcher.phantomjs_fetch(url)
        total_page = get_total_page(content)
        print 'Start downloading chapter %d' % chapter
        for page in range(1, int(total_page) + 1):
            try:
                get_and_download(page, chapter)
            except:
                print '!!!! Catch Exption when download chapter %d page %d !!!!' %(chapter, page)
