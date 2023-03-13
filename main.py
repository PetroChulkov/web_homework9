import scrapy
from scrapy.crawler import CrawlerProcess

from create import create

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        # Follows links to author pages
        for author in response.xpath("/html//div[@class='quote']/span/a/@href"):
            yield response.follow(author, self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        for author in response.xpath("/html//div[@class='author-details']"):
            yield {
                "fullname": author.xpath("h3[@class='author-title']/text()").extract_first().strip(),
                "born_date": author.xpath("p/span[@class='author-born-date']/text()").extract_first().strip(),
                "born_location": author.xpath("p/span[@class='author-born-location']/text()").extract_first().strip(),
                "description": author.xpath("div[@class='author-description']/text()").extract_first().strip()
            }




if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()
    create()