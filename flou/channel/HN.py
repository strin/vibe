from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector

from flou.webpage import extract_text
from flou.channel.db import add_entry

class __YCSpider(Spider):
    name 		= "ycombinator"
    allowed_domains	= ["news.ycombinator.com"]
    start_urls	= ["https://news.ycombinator.com"]

    def parse(self, response):
        hrefs = response.xpath('//td[@class="title"]/a')
        for href in hrefs:
            try:
                link = href.xpath('@href').extract()[0]
                title = href.xpath('text()').extract()[0]
                text = extract_text(link)
                add_entry(link, title, text)
                print text
            except Exception as e:
                print 'error: ', e

