# A. Colello 2016
# flickr picture scraper
#   to run:
#       navigate to python/flickr  
#       scrapy crawl picture

import scrapy
import flickrapi
import requests

from StringIO import StringIO
from PIL import Image

from flickr.items import FlickrMetaItem, PictureItem
import flickr.system_constants as s

class PictureSpider(scrapy.Spider):
    name = "picture"
    allowed_domains = ["www.flickr.com"]
    start_urls = (
        'http://www.flickr.com/', #placeholder; not actually used because I use the flickr api to query/iterate, but scrapy needs it to run
    )
    flickr_api = flickrapi.FlickrAPI(s.API_KEY, s.API_SECRET,format='parsed-json')

    def parse(self, response):
        q = self.flickr_api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance') #initial query
        #q.keys = 'photos' (metadata i care about), 'stat' -(ok query or not)
        if q['stat'] == 'ok': #successful query
            all_photos = q['photos']
            total_pages = all_photos['pages']
            current_page = all_photos['photo'] #get page 1; list of dicts

            for page_num in range(1, total_pages): #iterate through all pages
                for photo in current_page: #iterate through each dict in the list
                    items_to_yield = self.get_flickr_items(photo, [])
                    for i in items_to_yield:
                        yield i

                break #DEV_REMOVE

                #finally, update current page by getting next page
                #since range() goes up to but not including the second arg, page_num+1 will be valid on the final page query and thus valid always
                current_page = self.flickr_api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, page=page_num+1)['photos']['photo']

    #param: dict of one photo on a page
    def get_flickr_items(self, photo, to_return):
        f_item = FlickrMetaItem()

        f_item['url'] = s.BASE_URL.format(photo['farm'], photo['server'], photo['id'], photo['secret'])
        #https://www.flickr.com/services/api/misc.urls.html

        #(get other flickr metadata here, and put in f_item)

        to_return.append(f_item)

        self.scan_picture(f_item['url'], to_return)

        return to_return

    #use pillow here to scan the picture by URL and populate the other item, and append to to_return
    def scan_picture(self, url, to_return):
        p_item = PictureItem()

        #ASK TOM ABOUT GARBAGE COLLECTION
        #PIL.Image, StringIO, requests.get()
        #could cause problems with VM if memory gets overloaded

        #attempt to prevent memory leak: with statement
        with Image.open(StringIO(requests.get(url).content)) as img:
            length,height = img.size #see comments in items.PictureItem

            p_item['max_lower_pix'] = s.UPPER_PIXEL_THRESHOLD #DEV_REMOVE

            #(get other picture metadata here, ande put in p_item)

            p_item['url'] = url
            p_item['length'] = length
            p_item['height'] = height

        to_return.append(p_item)

