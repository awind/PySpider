# -*- coding: utf-8 -*-

import urllib2
import re
import time
import thread
from bs4 import BeautifulSoup


class SmzdmSpider:

    def __init__(self):
        self.enable = True
        self.page = 1
        self.pages = []

    def get_page(self, page):
        url = 'http://www.smzdm.com/p' + page
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(req)
        page_content = response.read()
        items = self.soup_process(page_content)
        # soup = BeautifulSoup(page_content, 'lxml')
        # list_items = soup.select('h4.itemName')
        # items = []
        # for item in list_items:
        #     dict = {}
        #     dict['price'] = item.a.span.text
        #     dict['url'] = item.a['href']
        #     item.a.span.decompose()
        #     dict['title'] = item.a.text.strip()
        #     items.append(dict)
        return items


    def soup_process(self, page_content):
        soup = BeautifulSoup(page_content, 'lxml')
        list_items = soup.select('div.list')

        items = []
        for item in list_items:
            dict = {}
            title_tag = item.select('h4.itemName')
            title = title_tag[0]
            dict['price'] = title.a.span.text
            dict['article_url'] = title.a['href']
            title.a.span.decompose()
            dict['title'] = title.a.text.strip()
            #dict['img'] = item.a.img['src']

            lr_bot = item.select('div.lrBot')
            if len(lr_bot) != 0:
                foot_item = lr_bot[0]
                scores = foot_item.select('span.scoreTotal')
                if len(scores) > 0:
                    scores[0].b.decompose()
                    dict['worth'] = scores[0].text
                    scores[1].b.decompose()
                    dict['not_worth'] = scores[1].text
                else:
                    dict['worth'] = 0
                    dict['not_worth'] = 0

                buy_btn = foot_item.select('div.buy')
                if len(buy_btn) > 0:
                    dict['original_url'] = buy_btn[0].a['href']
                else:
                    dict['original_url'] = ""
                items.append(dict)
        return items





    def load_page(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.get_page(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except Exception, e:
                    print e
                    print 'Can not connect to SMZDM'
            else:
                time.sleep(1)


    def show_page(self, now_page, page):
        for item in now_page:
            print u'Page %d  %s, price: %s, original url: %s, ' \
                  u'worth: %s, not worth: %s' %(page, item['title'],
                                                item['price'], item['original_url'], item['worth'], item['not_worth'])
            myinput = raw_input()
            if myinput == "quit":
                self.enable = False
                break


    def start(self):
        self.enable = True
        page = self.page

        print u'Loading SMZDM page.....'

        thread.start_new_thread(self.load_page, ())

        while self.enable:
            if self.pages:
                now_page = self.pages[0]
                del self.pages[0]
                self.show_page(now_page, page)
                page += 1




if __name__ == '__main__':
    spider = SmzdmSpider()
    spider.start()



