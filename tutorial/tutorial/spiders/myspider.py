# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
from scrapy.http.request import Request
from tutorial.items import TutorialItem
class DmozSpider(scrapy.Spider):
    allowed_domains = ["html5.qq.com"]
    name = "qqnews"
    keywords = ["起薪","薪金","兵役","社保卡","村官","信息安全","户籍","环境保护","互联网+","创业","租房补贴"]
    headers1 = {
        "Host": "smartbox.html5.qq.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }
    headers2 = {
        "Host":"news.html5.qq.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    def start_requests(self):
        for t in self.keywords:
            yield Request("http://smartbox.html5.qq.com/search?t=1&ch=001411&q="+t, headers=self.headers1,meta={'key':t},callback=self.parse)
            

    def parse(self, response):   
        body=response.xpath('//*[@id="wrapper"]/div[1]/div[2]/div/ul/li').extract()
        if body:
            for b in body:        
                urlnum =re.findall(r'yid=(\d+)&',b)
                if urlnum:
                    yield Request("https://news.html5.qq.com/share/"+str(urlnum[0]), headers=self.headers2,meta={'news_id':urlnum[0]},callback=self.parse2)
                t=response.meta['key']
                yield Request("http://smartbox.html5.qq.com/more?t=1&q="+t+"&ch=001411&search=", headers=self.headers1,meta={'key':t},callback=self.parse1)    

    def parse1(self, response):   
        body=response.xpath('/html/body').extract()
        if body:
            urlnum =re.findall(r'yid=(\d+)&',body[0])
            if urlnum:
                for t in urlnum:
                    yield Request("https://news.html5.qq.com/share/"+str(t), headers=self.headers2,meta={'news_id':t},callback=self.parse2)
                key=response.meta['key']
                yield Request("http://smartbox.html5.qq.com/more?t=1&q="+key+"&ch=001411&search=", headers=self.headers1,meta={'key':key},callback=self.parse1,dont_filter=True)

    def parse2(self, response):
        qqnewsitem = TutorialItem()
        title = response.xpath('//*[@id="react-root"]/div/div[1]/div[1]/section/header/h1/text()').extract()
        if title:
            qqnewsitem['title'] = title[0].encode("utf-8")

        text_content1 = response.xpath('//*[@id="react-root"]/div/div[1]/div[1]/section/article/p')
        qqnewsitem['text_content'] = ""
        for text_content in text_content1.xpath('./span/text()').extract():
            if text_content:
                for x in range(len(text_content)):
                    qqnewsitem['text_content'] += text_content[x].encode("utf-8")

        qqnewsitem['url'] = response.url
        qqnewsitem['news_id'] = response.meta['news_id']
        qqnewsitem['key_words'] = "无"

        imgnum = re.findall(r'"type":"image"', response.body)
        qqnewsitem['has_image'] = len(imgnum)

        yield qqnewsitem


