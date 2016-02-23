# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class FlickrItem(Item):
    url = Field()
    #types of metadata:
    #    http://librdf.org/flickcurl/api/flickcurl-searching-search-extras.html

class BlobItem(Item):
    url = Field()
    algorithm = Field()  
    x_center = Field()
    y_center = Field()
    mean_px = Field()
    median_px = Field()
    mode_px = Field()
    radius = Field()
    radius_hpct = Field() #ratio of radius to height of pic
    radius_wpct = Field() #ratio of radius to width of pic
    b_class=Field() # ? when scraping data, class when using training set



