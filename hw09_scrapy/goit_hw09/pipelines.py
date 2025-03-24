import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


FILE_QUOTES = r'..\output\quotes.json'
FILE_AUTHORS = r'..\output\authors.json'


class DataPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        with open(FILE_QUOTES, mode='w+', encoding='utf-8') as file:
            json.dump(self.quotes, file, ensure_ascii=False, indent=4)
        with open(FILE_AUTHORS, mode='w+', encoding='utf-8') as file:
            json.dump(self.authors, file, ensure_ascii=False, indent=4)
