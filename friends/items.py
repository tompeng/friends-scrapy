# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EpisodeItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	episode = scrapy.Field()
	season = scrapy.Field()
	link = scrapy.Field()


class LineItem(scrapy.Item):
	character = scrapy.Field()
	season = scrapy.Field()
	episode = scrapy.Field()
	text = scrapy.Field()
