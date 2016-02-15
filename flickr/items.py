# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class FlickrMetaItem(Item):
    url = Field()
    #types of metadata:
    #    http://librdf.org/flickcurl/api/flickcurl-searching-search-extras.html

class PictureItem(Item):
    url = Field() #decent primary key for now
    max_lower_pix = Field() #number of pixels above SOME threshold  in lower quadrant
    length = Field() #might want to move len/hei to flickrmetaitem level, because it is faster(?) to get it from that
    height = Field()

