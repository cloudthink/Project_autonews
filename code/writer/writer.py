# -*- coding: UTF-8 -*-
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from code.spider.all_spiders import *
from code.spider.get_article_baijiahao import *


class writer_baijiahao:
    def __init__(self):
        self.driver = (webdriver.Chrome())
        self.driver.maximize_window()  # 浏览器全屏显示
        self.tongyici = {}
        rfile = open("../../data/jinyici_1.data", 'rb')
        storedlist = pickle.load(rfile)
        self.tongyici=storedlist
        #print(storedlist)
        #print(storedlist["失陪"])
        rfile.close()
    def login(self):
        self.driver.get("http://baijiahao.baidu.com")
        # 自动填写保持登录状态cookies
        password_cookies = [
            ]
        for one in password_cookies:
            self.driver.add_cookie(one)
        time.sleep(random.randint(1,3))
        # 打开写文章页面
        self.driver.get("http://baijiahao.baidu.com/builder/article/edit?type=news&return_version1=1")
        time.sleep(1)
    def write_title(self,title):
        # 添加标题
        self.driver.find_element_by_id("article-title").send_keys(title)
    def write_category(self,category):
        # 分类选择
        s1 = Select(self.driver.find_element_by_id('cate-level-1'))  # 实例化Select
        s1.select_by_visible_text(category)
    def write_tags(self,key_tags):
        # 标签添加
        for one_tag in key_tags:
            self.driver.find_element_by_class_name("input-tag").send_keys(one_tag)
            self.driver.find_element_by_class_name("input-tag").send_keys(Keys.ENTER)
    def write_cover(self):
        # 自动封面
        js = "var q=document.documentElement.scrollTop=5000"
        self.driver.execute_script(js)
        radios = self.driver.find_elements_by_css_selector('span[class="radio-item"]')
        print(radios)
        for radio in radios:
            radio.click()
            time.sleep(0.5)
        js = "var q=document.documentElement.scrollTop=50"
        self.driver.execute_script(js)
        #time.sleep(20)
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
    def write_img(self,img_keywords):
        # 添加图片
        self.driver.find_element_by_id("edui9_body").click()
        self.driver.switch_to.frame('edui3_iframe')
        time.sleep(1)
        self.driver.find_element_by_css_selector('li[class="legal-img-wrap"]').click()
        self.driver.find_element_by_class_name("search").send_keys(img_keywords)
        self.driver.find_element_by_class_name("search").send_keys(Keys.ENTER)
        time.sleep(5)
        img = self.driver.find_elements_by_tag_name("img")
        print(img)
        try:
            random.choice(img[5:-1]).click()
        except Exception as e:
            print('img',e)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_id("edui8").click()
        time.sleep(5)
    def write_part_content(self,part_content_str):
        # 添加正文
        self.driver.switch_to.frame('ueditor_0')  # 注意，这种editor一定有frame，一定要切frame
        #body_string = ""
        #for one in part_content:
        #    body_string = body_string + str(one)
        #body_string = change_words(body_string)
        #print(body_string)
        print(part_content_str)
        for one in part_content_str:
            # print(one)
            # body_string = body_string+str(one)
            # print(body_string)
            if  (one==":") or (one=="："):
                self.driver.find_element_by_tag_name('body').send_keys(one)  # 直接往frame里的body里填内容，是不是很简单粗暴
                self.driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
                time.sleep(1)
            else:
                self.driver.find_element_by_tag_name('body').send_keys(one)  # 直接往frame里的body里填内容，是不是很简单粗暴
                time.sleep(0.1)

            time.sleep(0.001)


        #self.driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
        self.driver.switch_to.default_content()
        time.sleep(5)
    def change_words(self,a_sentence,p):
        seg_list = jieba.cut(a_sentence)
        new_sentence=""
        for one in seg_list:
            if random.random() <p and len(one)>=2 and self.is_number(one)==False:
                try:
                    schange=random.choice(self.tongyici[one])
                    if len(schange)>1 and (len(schange)==len(self.tongyici[one])):
                        new_sentence=new_sentence+schange
                    else:
                        new_sentence=new_sentence+one
                except Exception as e:
                    #print("chang error:",e)
                    new_sentence = new_sentence + one
                    pass
            else:
                new_sentence=new_sentence+one
        return new_sentence
    def do(self,category):
        zh_list = {"science": "科技", "finance": "财经", "sports": "体育"}
        self.category=category
        self.category_zh=zh_list[self.category]
        news = get_one_type_article(category)

        self.login()
        self.write_cover()
        title, content, key_tags, part_tags = news.today_news()
        self.write_title(self.change_words(title,0.3))

        self.write_category(category=self.category_zh)
        self.write_tags(key_tags)
        #self.write_part_content("大家好，我是人工智能机器人【数据猪】，下面由我来为大家播报今日"+self.category_zh+"要文：")
        self.write_img(part_tags[0])
        time.sleep(3)
        print(content)
        for one_sentence in content:

            str_sentence = ""
            for one in one_sentence:
                str_sentence=str_sentence+one
            str_sentence=self.change_words(str_sentence,0.6)
            self.write_part_content(str_sentence)
            img_keywords=part_tags[content.index(one_sentence)]
            #js = "var q=document.documentElement.scrollTop=3000"
            #self.driver.execute_script(js)
            try:
                if random.random()<0.9:
                    self.write_img(img_keywords)
            except Exception as e:
                print(e)
            time.sleep(3)
        # 保存草稿
        self.driver.find_element_by_xpath("//button[@id='editor-draft']").click()  # cg->fb fabiao
        print(time.time(), "保存草稿成功...", title)

if __name__ == '__main__':
    aa=writer_baijiahao()
    aa.do("science")