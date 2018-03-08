# -*- coding: UTF-8 -*-
#百家号文章总排行榜
#https://baijia.baidu.com/
#单独分类排行
#https://baijia.baidu.com/channel?cat=[1,2,3,4,5]
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

class get_one_type_article:
    def __init__(self, category):
        zh_list={"science":"科技","finance":"财经","sports":"体育"}
        self.category = category
        self.category_zh = zh_list[category]
        self.url=""
        self.day_top_url=[]
        self.week_top_url=[]
    def get_article_top_url(self):
        base_url="https://baijia.baidu.com/channel?cat="
        category_url={"science":base_url+"1","entertainment":base_url+"2","finance":base_url+"3","sports":base_url+"4","culture":base_url+"5"}
        self.url=category_url[self.category]
        print(self.url)
        req = urllib.request.Request(self.url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': USER_AGENT
        })
        urlop = urllib.request.urlopen(req, timeout=2)
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

        aa = htmlsoup.find_all("p", attrs={"class": "art-title"})
        url_line=[]
        for one in aa[0:9]:
            url_line.append("https://baijia.baidu.com"+str(one.find("a").get("href")))
        self.day_top_url=url_line[:9]
        self.week_top_url=url_line[9:]

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
        self.title = today+"-今日"+self.category_zh+"简报："
        self.title_list=[]
        self.contents = []
        self.img_urls = []
        self.key_tags=[]
        self.part_tags=[]
        day_top_url,week_top_url=self.get_article_top_url()
        title_line=[]

        j=1
        for one in day_top_url[0:5]:
            try:

                baijiahao_sp = baijiahao_spider(one)
                (title, author, content, abstract, read_number, comment_number, img_urls) = baijiahao_sp.url_to_data()
                one_content = [(str(j) + '、')+title+'：']
                self.title_list.append(title)

                keywords=jieba.analyse.extract_tags(content, topK=5, withWeight=False, allowPOS=())
                #print(keywords)
                self.part_tags.append(keywords[0])
                rank_line=[]
                content_line=self.cut_sentences(content)
                for one_line in content_line:
                    rank=0
                    for one_key in keywords:
                        if one_key in one_line:
                            rank=rank+1
                    rank_line.append(rank)
                rank_mean=sum(rank_line)/len(rank_line)
                rank_sort=sorted(rank_line,reverse = True)
                i=0
                print(rank_sort)
                for one_line in content_line[:-3]:
                    if (rank_line[i]>=rank_sort[int(len(rank_line)/2)] and len(one_line)>3) or random.random()>0.4:
                        one_content.append(one_line)
                    if len(one_content)>6:
                        break
                    #if len(one_content)>3:
                    #    one_content.append('#')
                #one_content.append("\n")
                #print(one_content)
                if len(str(one_content))>50:
                    j=j+1
                    self.content=self.contents.extend([one_content])
                self.img_urls.append(img_urls)

            except:
                pass
        self.key_tags=jieba.analyse.extract_tags(str(self.contents), topK=5, withWeight=False, allowPOS=())
        #if (len(title)) <= 18 and self.title == today + "今日科技简报:":
        #self.title = today + "-今日"+self.category_zh+"简报："
        for th in self.key_tags:
            if len(self.title)<29 and self.is_number(th)==False :
                self.title=self.title+ str(th)+"，"
        #print (self.title, self.contents, self.key_tags)
        #for one in self.title_list:
        #    if len(one)<19:
        #        self.title = today + "-今日" + self.category_zh + "简报：" + one
        #    else:
        #        self.title = today + "-今日" + self.category_zh + "简报：" + title[0:19]
        return(self.title[0:-1],self.contents,self.key_tags,self.part_tags)
if __name__ == '__main__':

    ll=get_one_type_article("science")
    print(ll.today_news())