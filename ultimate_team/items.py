# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    nation = scrapy.Field()
    club = scrapy.Field()
    league = scrapy.Field()
    position = scrapy.Field()
    global_rate = scrapy.Field()
    physical_stats = scrapy.Field()
    traits = scrapy.Field()
    stat_val = scrapy.Field()
    
