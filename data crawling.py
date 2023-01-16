from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import json
import csv
import time
### 定义爬虫类 ###
class JdSpider():
### 定义初始文件类型 ###
    def open_file(self):
        '''
        self.fm=input("请输入Jd_computer文件保存格式（txt,json,csv）:")
        while self.fm!='txt' and self.fm!='json' and self.fm!='csv':
            self.fm=input("输入错误，请重新输入文件保存格式（txt,json,csv）：")
            self.fm = input("输入错误，请重新输入文件保存格式（txt,json,csv）：")
        if self.fm=='txt':
            self.fd=open('Jd_computer.txt','w',encoding='utf-8')
        elif self.fm=='json':
            self.fd=open('Jd_computer.json','w',encoding='utf-8')
        elif self.fm=='csv':
            self.fd=open('Jd_computer.csv','w',encoding='utf-8',newline='')
        '''
        self.fn=input("请输入Jd_comments文件保存格式（txt,json,csv）:")
        while self.fn!='txt' and self.fn!='json' and self.fn!='csv':
            self.fn=input("输入错误，请重新输入文件保存格式（txt,json,csv）：")
            self.fn = input("输入错误，请重新输入文件保存格式（txt,json,csv）：")

        if self.fn=='txt':
            self.fw=open('Jd_comments.txt','w',encoding='utf-8')
        elif self.fn=='json':
            self.fw=open('Jd_comments.json','w',encoding='utf-8')
        elif self.fn=='csv':
            self.fw=open('Jd_comments.csv','w',encoding='utf-8',newline='')
### 加载页面 ###
    def open_browser(self):
        self.browser=webdriver.Chrome(executable_path="C:\\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        self.browser.implicitly_wait(10)
        self.wait=WebDriverWait(self.browser,10)
### 初始化变量 ###
    def init_variable(self):
        self.data=zip()
        self.isLast=False
        self.data_one = {'callback': 'fetchJSON_comment98',  # 调整页数page参数
                         'productId': '123',
                         'score': 0,
                         'sortType': 5,
                         'page': 0,
                         'pageSize': 10,
                         'isShadowSku': 0,
                         'rid': 0,
                         'fold': 1}

        self.url = 'https://club.jd.com/comment/productPageComments.action?'
        self.num =2    # 评论界面页数，每页10条
        self.commentList = []   # 多页评论列表
        self.num_page=2  #京东电脑界面页数
    def getComment(self):  # 获得一页的评论
        try:
            self.r = requests.get(self.url, params=self.data_one)
            self.r.raise_for_status()
            self.r.encoding = self.r.apparent_encoding
        except:
            print('爬取失败')
        i = json.dumps(self.r.text)  # 将页面内容编码成json数据，（无论什么格式的数据编码后都变成了字符串类型str）
        j = json.loads(i)  # 解码，将json数据解码为Python对象
        # print(type(j))
        comment = re.findall(r'{"productAttr":.*}', j)  # 对网页内容筛选找到我们想要的数据，得到值为字典的字符串即'{a:1,b:2}'
        # print(comment)
        comm_dict = json.loads(comment[0])  # 将json对象obj解码为对应的字典dict
        # print(type(comm_dict))
        commentSummary = comm_dict['comments']  # 得到包含评论的字典组成的列表
        # print(commentSummary)
        for comment in commentSummary:  # 遍历每个包含评论的字典，获得评论
            c_content = ''.join(comment['content'].split())  # 获得评论,由于有的评论有换行，这里用split（）去空格，换行，并用join（）连接起来形成一整段评论，便于存储
            self.commentList.append([c_content])


### 解析网页###
    def parse_page(self):
       try:
    ### 商品 ID ###
        skus=self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//li[@class="gl-item"]')))
        skus=[item.get_attribute('data-sku') for item in skus]
    ### 价格 ###
        prices=self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[2]/strong/i')))
        prices=[item.text for item in prices]
    ### 名称 ###
        names=self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[3]/a/em')))
        names=[item.text for item in names]
    ### 评论数 ###
        comments=self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[4]/strong')))
        comments=[item.text for item in comments]
    ### 打包（商品 ID、链接、价格、评论数）
        self.data=zip(skus, prices,names,comments)
### 异常处理 ###
       except selenium.common.exceptions.TimeoutException: ###
         print('pares_page:TimeoutException')
         self.parse_page()
       except selenium.common.exceptions.StaleElementReferenceException:
         print('parse_page:StaleElementReferenceException') # 数据更新
         self.browser.refresh() # 刷新
### 翻页 ###
    def turn_page(self):
       try:
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="pn-next"]'))).click()
        time.sleep(2)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(4)
### 异常处理 ###
       except selenium.common.exceptions.TimeoutException:
         print('turn_page:TimeoutException')
         self.turn_page()
       except selenium.common.exceptions.StaleElementReferenceException:
         print('turn_page:StaleElementReferenceException')
         self.browser.refresh()
    '''
### 电脑信息数据写入 ###
    def write_to_file1(self):
       if self.fm=='txt':
         for item in self.data:
            self.fd.write('----------------------------------------\n')
            self.fd.write("link:"+str(item[0])+'\n')
            self.fd.write("price:"+str(item[1])+'\n')
            self.fd.write("name:"+str(item[2])+'\n')
            self.fd.write("comment:"+str(item[3])+'\n')
       if self.fm=='json':
            temp=('link','price','name','comment')
            for item in self.data:
               json.dump(dict(zip(temp,item)),self.fd,ensure_ascii=False)
       if self.fm=='csv':
            writer=csv.writer(self.fd)
            header=['link', 'price', 'name', 'comment']
            writer.writerow(header)
            for item in self.data:
                writer.writerow(item)
    '''

### 评论数据写入 ###
    def write_to_file2(self):
       if self.fn=='txt':
         for item in self.commentList:
            self.fw.write("comment:" + str(item[0]) + '\n')
       '''
       if self.fn=='json':
            temp=('comment')
            for item in self.commentList:
               json.dump(dict(zip(temp,item)),self.fw,ensure_ascii=False)
       '''
       if self.fn=='csv':
            writer=csv.writer(self.fw)
            for item in self.commentList:
                writer.writerow(item)
### 关闭文件 ###
    def colse_file(self):
       #self.fd.close()
       self.fw.close()
###
    def close_browser(self):
        self.browser.quit()
###
    def crawl(self):
       self.open_file()
       self.open_browser()
       self.init_variable()
       print('开始爬取')
       self.browser.get('https://search.jd.com/search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V04--12s0%2C20s0%2C38s0&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC&ev=exbrand_Apple%5E&uc=0#J_searchWrap')
       time.sleep(1)
       self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
       time.sleep(2)
       count=1
       while not self.isLast:
         if count>=self.num_page:
            self.isLast=True
         print('正在爬取' + str(count) + '页......')
         count+=1
         self.parse_page()
         for item in self.data:#每个型号代码的评论
             self.commentList = []  # 多页评论列表
             self.data_one['productId']=str(item[0])
             for i in range(self.num):
                 try:  # 防止网页提取失败，使爬取终断，直接跳过失败页，继续爬取
                     self.data_one['page'] = i
                     self.getComment()
                 except:
                     continue
                 time.sleep(2)  # 由于网站反爬虫，所以每爬一页停2秒
             print(self.commentList)
             self.write_to_file2()
         self.turn_page()
       self.colse_file()
       self.close_browser()
       print('结束爬取')


if __name__ == "__main__":
    spider=JdSpider()
    spider.crawl()

