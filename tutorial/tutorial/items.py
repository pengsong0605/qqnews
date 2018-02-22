# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    news_id=scrapy.Field()
    url=scrapy.Field()
    title = scrapy.Field()
    text_content = scrapy.Field()
    key_words = scrapy.Field()
    has_image=scrapy.Field()
