import json
import scrapy
import sys
from scrapy.crawler import CrawlerProcess

sys.path.append(r'C:\GitHub\pytraining-1\2 - Web\Module 9 - Beautiful Soup + Scrapy\home-work\goit_hw09')
from goit_hw09.items import QuoteItem, AuthorItem
from goit_hw09.pipelines import DataPipeline


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}
    visited_authors = set()

    def parse(self, response):
        for q in response.xpath("/html//div[@class='quote']"):
            author = q.xpath("span/small/text()").get().strip()
            author_url = q.xpath("span/a/@href").get().strip()
            quote = q.xpath("span[@class='text']/text()").get().strip()
            tags = q.xpath("div[@class='tags']/a/text()").extract()

            yield QuoteItem(
                quote=quote,
                author=author,
                tags=[t.strip() for t in tags]
            )

            yield response.follow(
                url=self.start_urls[0] + author_url,
                callback=self.parse_author
            )

        next_page_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_page_link:
            url = self.start_urls[0] + next_page_link
            yield scrapy.Request(url=url)

    @classmethod
    def parse_author(self, response, **kwarg):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = content.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorItem(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description
        )


if __name__ == "__main__":
    # run spider
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
