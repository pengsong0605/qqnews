# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

def dbHandle():
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='news',
        user='root',
        passwd='',
        charset='utf8',
    )
    return conn

class TutorialPipeline(object):

    def __init__(self):
        self.dbObject = dbHandle()
        self.cursor = self.dbObject.cursor()
    def process_item(self, item, spider):
        sql = 'insert into article(news_id,url,title,text_content,key_words,has_image,has_classified,should_left) values (%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql,(str(item['news_id']),  item['url'].encode("utf-8"), item['title'],item['text_content'], item['key_words'].encode("utf-8"),str(item['has_image']),"1","1"))
            self.dbObject.commit()
        except Exception as e:
            print (e)
            self.dbObject.rollback()
        return item
    def __del__(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.dbObject.close()
