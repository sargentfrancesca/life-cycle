# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class EolItem(scrapy.Item):
	main_url = scrapy.Field()
	name = scrapy.Field()
	common_name = scrapy.Field()
	image_url = scrapy.Field()
