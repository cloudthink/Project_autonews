#encoding=utf-8
import urllib
#编码检测工具
import chardet
import urllib.request
import re
from bs4 import BeautifulSoup
import time,random
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
class baijiahao_spider:
    def __init__(self,url):
        self.url=url
        self.title=""
        self.author=""
        self.content=""
        self.abstract=""
        self.read_number=""
        self.comment_number=0
        self.img_urls=[]
    def imgs_clean(self,imgs):
        new_imgs=[]
        for one in imgs:
            new_imgs.append(str(one).replace("amp;", ""))
        return new_imgs
    def url_to_data(self):

        req = urllib.request.Request(self.url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': USER_AGENT
        })
        try:
            urlop = urllib.request.urlopen(req, timeout=2)
        except:
            time.sleep(random.randint(0,9))
            urlop = urllib.request.urlopen(req, timeout=2)
        # 先获取网页内容
        decode_data = urllib.request.urlopen(req).read()

        # 用编码检测组件chardet进行内容分析,{'confidence': 0.99, 'encoding': 'utf-8'},表示99%的概率认为是utf-8
        chardit = chardet.detect(decode_data)
        # print(chardit)

        content_charset = chardit['encoding']
        # print(content_charset)
        encode_data = urlop.read().decode(content_charset)
        #print(encode_data)
        htmlsoup = BeautifulSoup(encode_data, 'html.parser')

        self.title = htmlsoup.find("h1",attrs={"class":"title"})
        self.title = re.sub("<.*?>","",str(self.title))
        self.author = htmlsoup.find(attrs={"class":"name"})
        self.content = htmlsoup.find(attrs={"class":"news-content"})
        self.content = re.sub("\\n.*\\n", "", str(self.content))

        self.content = re.sub("<.*?>","",str(self.content)[133:])
        self.abstract = htmlsoup.find(attrs={"class":"abstract"})
        self.read_number = htmlsoup.find(attrs={"class":"read"})
        self.comment_number = 0
        img_urls = htmlsoup.find_all("p",attrs={"data-bjh-caption-id":True})
        self.img_urls = self.imgs_clean(img_urls)
        #print(self.content)
        #print(self.title,self.author,self.content,self.abstract,self.read_number,self.comment_number,self.img_urls)
        time.sleep(random.randint(0,3))
        return (str(self.title),self.author,str(self.content),self.abstract,self.read_number,self.comment_number,self.img_urls)
if __name__ == '__main__':
    url="https://baijia.baidu.com/s?id=1588628902337785805&wfr=pc&fr=new_top"
    ll=baijiahao_spider(url)
    ll.url_to_data()
    #https://timg01.bdimg.com/timg?pacompress&imgtype=1&sec=1439619614&autorotate=1&di=6ec19062385e762941f3b3df34fc603e&quality=90&size=b870_10000&src=http%3A%2F%2Fbos.nj.bpc.baidu.com%2Fv1%2Fmediaspot%2F6bc2f010a931d3b5c27857b8a295c7eb.jpeg