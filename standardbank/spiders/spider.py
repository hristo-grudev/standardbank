import scrapy

from scrapy.loader import ItemLoader

from ..items import StandardbankItem
from itemloaders.processors import TakeFirst


class StandardbankSpider(scrapy.Spider):
	name = 'standardbank'
	start_urls = ['https://www.standardbank.com/services/search/ArticleSearch.jsp?channelID=dff02383c59dd610VgnVCM2000008811960a____&articleCTA=Read%20More&topic=&keyword=&startIndex=0&endIndex=999999&pageSize=999999']

	def parse(self, response):
		post_links = response.xpath('//a[@class="link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="title title--page"]/text()').get()
		description = response.xpath('//div[@class="component text"]//text()[normalize-space()]|//p[@class="title title--entrance"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="page-intro-article__subtitle-date"]/text()').get()

		item = ItemLoader(item=StandardbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
