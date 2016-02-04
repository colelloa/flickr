# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class FlickrMetaItem(Item):
    url = Field()

class PictureItem(Item):
    url = Field() #decent primary key for now
    max_lower_pix = Field() #number of pixels above some threshold  in lower quadrant
    length = Field()
    height = Field()

