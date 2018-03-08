# -*- coding: UTF-8 -*-
#ctimes新闻
#https://www.ctimes.com.tw
#新闻列表
#https://www.ctimes.com.tw/news/newsindex.asp
import urllib
#编码检测工具
import chardet
import urllib.request
import re,time,math
from bs4 import BeautifulSoup
from code.spider.all_spiders import *
import jieba.analyse
import jieba
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

class get_news_article:
    def __int__(self):
        self.url=""
        self.day_top_url=[]
        self.week_top_url=[]
        #self.category_zh="科技"

    def get_article_top_url(self):
        base_url="https://www.ctimes.com.tw"

        self.url=base_url+"/news/newsindex.asp"
        print(self.url)
        req = urllib.request.Request(self.url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': USER_AGENT
        })
        urlop = urllib.request.urlopen(req, timeout=9)
        # 先获取网页内容
        decode_data = urllib.request.urlopen(req).read()

        # 用编码检测组件chardet进行内容分析,{'confidence': 0.99, 'encoding': 'utf-8'},表示99%的概率认为是utf-8
        chardit = chardet.detect(decode_data)
        # print(chardit)

        content_charset = chardit['encoding']
        # print(content_charset)
        encode_data = urlop.read().decode(content_charset)
        # print(encode_data)
        htmlsoup = BeautifulSoup(encode_data, 'html.parser')

        a = htmlsoup.find_all("a", attrs={"class": "IT"})
        b = htmlsoup.find_all("a", attrs={"class": "hp8"})
        url_line=[]
        print(a,b)
        for one in a:
            url_line.append(base_url+str(one.get("href")))
        for one in b:
            url_line.append(base_url+str(one.get("href")))
        self.day_top_url=url_line
        self.week_top_url=url_line
        print(self.day_top_url,self.week_top_url)
        return(self.day_top_url,self.week_top_url)
    def cut_sentences(self,sentence):
        puns = frozenset(u'。！？!?')
        tmp = []
        rl=[]
        for ch in sentence:
            tmp.append(ch)
            if puns.__contains__(ch):
                rl.append( ''.join(tmp))
                tmp = []
        return rl

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False
    def today_news(self):
        today=time.strftime('%m-%d',time.localtime(time.time()))
        self.title = today+"-今日"+"简报："
        self.title_list=[]
        self.contents = []
        self.img_urls = []
        self.key_tags=[]
        self.part_tags=[]
        day_top_url,week_top_url=self.get_article_top_url()
        title_line=[]

        j=1
        for one in day_top_url[0:2]:
            try:

                baijiahao_sp = baijiahao_spider(one)
                (title, author, content, abstract, read_number, comment_number, img_urls) = baijiahao_sp.url_to_data()
                one_content = [(str(j) + '、')+title+'：']
                self.title_list.append(title)

                keywords=jieba.analyse.extract_tags(content, topK=5, withWeight=False, allowPOS=())
                print(title, author, content, abstract, read_number, comment_number, img_urls)
            except Exception as e:
                print(e)
        return(self.title[0:-1],self.contents,self.key_tags,self.part_tags)
if __name__ == '__main__':

    ll=get_news_article()
    ll.today_news()