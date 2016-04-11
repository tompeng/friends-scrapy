import scrapy
from friends.items import EpisodeItem, LineItem

import urlparse


class EpisodeSpider(scrapy.Spider):
	name = 'get_episodes'
	allowed_domains = ["livesinabox.com"]
	start_urls = [
		"http://www.livesinabox.com/friends/scripts.shtml",
	]

	def parse(self, response):

		# season 1 - season 8,  season 10 episode 15 - 18
		for sel in response.xpath('//ul/li/a'):
			episode_item = EpisodeItem()
			episode_item['season'] = sel.re('season(\d)') or sel.re('(\d+)\d{2}:')
			episode_item['episode'] = sel.re('Episode \d+?(\d{2}):')
			episode_item['link'] = sel.xpath('@href').extract()
			# yield episode_item
			if len(episode_item['link']) > 0 and episode_item['link'][0]:
				url = urlparse.urljoin('http://www.livesinabox.com/friends/', episode_item['link'][0])
				print url
				yield scrapy.Request(url, callback=self.parse_script_content)

		# season 9
		for sel in response.xpath('//ul/li/font/a'):
			episode_item = EpisodeItem()
			episode_item['season'] = sel.re('season(\d)')
			episode_item['episode'] = sel.re('9(\d{2}):')
			episode_item['link'] = sel.xpath('@href').extract()
			if len(episode_item['link']) > 0 and episode_item['link'][0]:
				url = urlparse.urljoin('http://www.livesinabox.com/friends/', episode_item['link'][0])
				yield scrapy.Request(url, callback=self.parse_script_content)

		# season 10 episode 1 - 14
		for sel in response.xpath('//ul/li/div'):
			episode_item = EpisodeItem()
			episode_item['season'] = '10'
			episode_item['episode'] = sel.re('10(\d{2}):')
			episode_item['link'] = sel.xpath('a/@href').extract() or sel.xpath('font/a/@href').extract()
			if len(episode_item['link']) > 0 and episode_item['link'][0]:
				url = urlparse.urljoin('http://www.livesinabox.com/friends/', episode_item['link'][0])
				yield scrapy.Request(url, callback=self.parse_script_content)

	def parse_script_content(self, response):

		# Not suitable for season 10
		if 'season' not in response.url:
			return
		i = response.url.find('season')
		season = response.url[i + 6]
		episode = response.url[i + 9:i + 11]
		# TODO:
		# S9E22, S9E23-24 missing

		for p in response.xpath('//p[descendant::b]'):

			character = p.re('<b>(\w+):<\/b>')
			text = p.xpath('font/text()').extract() or p.xpath('text()').extract() or p.xpath('font/font/text()').extract()
			if character and text:
				# TODO:
				# Need to consider the text with length < 25
				if len(text[0]) - (text[0].find(')') - text[0].find('(')) >= 20 and 'Scene:' not in text[0] and character[0] != 'All':
					# TODO:
					# There are a lot of lines that contain bold words, which will break the line
					# Need to deal with this later
					if len(text) == 1:
						line_item = LineItem()
						line_item['episode'] = episode
						line_item['season'] = season
						line_item['character'] = character[0]
						line_item['text'] = text[0]
						yield line_item


# Need another parser for season 10, since the character is no longer bold
class LineSpider(scrapy.Spider):
	name = 'get_lines'
	allowed_domains = 'livesinabox.com'
	start_urls = ['http://www.livesinabox.com/friends/season1/101pilot.htm']

	def parse(self, response):
		for p in response.xpath('//p[descendant::b]'):

			character = p.re('<b>(\w+):<\/b>')
			text = p.xpath('font/text()').extract() or p.xpath('text()').extract() or p.xpath('font/font/text()').extract()
			if character and text: 
				if len(text[0]) >= 20 and 'Scene:' not in text[0] and character[0] != 'All':
					line_item = LineItem()
					line_item['episode'] = '01'
					line_item['season'] = '1'
					line_item['character'] = character[0]
					line_item['text'] = text
					yield line_item
