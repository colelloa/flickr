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
#dev
URLS_VISITED = '''https://farm2.staticflickr.com/1102/5117093816_a9c4c383c9.jpg
https://farm4.staticflickr.com/3521/3753864330_fc3d36755a.jpg
https://farm3.staticflickr.com/2643/3753861818_662a81c0c6.jpg
https://farm4.staticflickr.com/3489/3753869790_4956e5478c.jpg
https://farm4.staticflickr.com/3429/3753074355_dea84d53b2.jpg
https://farm4.staticflickr.com/3001/2519474886_4c4dd87d5f.jpg
https://farm3.staticflickr.com/2489/3753094819_3b182acf02.jpg
https://farm3.staticflickr.com/2636/3753886656_7697149ebe.jpg
https://farm4.staticflickr.com/3499/3753884788_b7ec790071.jpg
https://farm3.staticflickr.com/2506/3753877062_f07660f945.jpg
https://farm3.staticflickr.com/2427/3753880016_e731144ebd.jpg
https://farm3.staticflickr.com/2294/1975875218_0610e6e722.jpg
https://farm3.staticflickr.com/2598/3753084645_9136798d32.jpg
https://farm6.staticflickr.com/5028/5690773693_bbd9520e4f.jpg
https://farm6.staticflickr.com/5540/9656873877_c8a4b9849f.jpg
https://farm9.staticflickr.com/8432/7811952096_4178084a54.jpg
https://farm9.staticflickr.com/8738/16580900700_37478070f3.jpg
https://farm5.staticflickr.com/4152/5013096054_8f233bfee3.jpg
https://farm3.staticflickr.com/2601/3753093167_d9f9a8fa55.jpg
https://farm3.staticflickr.com/2659/3753867028_73931a286d.jpg'''.split('\n')


class PictureSpider(scrapy.Spider):
    name = "picture"
    allowed_domains = ["www.google.com", "www.flickr.com"]
    start_urls = (
        'http://www.google.com/', #placeholder; not actually used because I use the flickr api to query/iterate, but scrapy needs a url to start
    )
    api = flickrapi.FlickrAPI(s.API_KEY, s.API_SECRET, format='parsed-json')

    def parse(self, response):
        q = self.api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance') #initial query
        if q['stat'] == 'ok': #successful query
            all_photos = q['photos']
            total_pages = all_photos['pages']
            current_page = all_photos['photo'] #get page 1; list of dicts

            count = 0 #DEV_REMOVE
            id_num = 1#DEV_REMOVE
            for page_num in range(1, total_pages): #iterate through all pages
                for photo in current_page: #iterate through each dict in the list
                    items_to_yield = self.get_flickr_items(photo, id_num, [])
                    if not (items_to_yield[0]['url']  in URLS_VISITED):#dev
                        for i in items_to_yield:
                            yield i
                        id_num += 1#DEV_REMOVE

                count += 1 #DEV_REMOVE
                if count > 10: #DEV_REMOVE
                    break #DEV_REMOVE

                #finally, update current page by getting next page
                #since range() goes up to but not including the second arg, page_num+1 will be valid on the final page query and thus valid always
                current_page = self.api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance', page=page_num+1)['photos']['photo']

    #param: dict of one photo on a page
    def get_flickr_items(self, photo, id_num, to_return):
        f_item = FlickrMetaItem()

        f_item['url'] = s.BASE_URL.format(photo['farm'], photo['server'], photo['id'], photo['secret'])
        #https://www.flickr.com/services/api/misc.urls.html

        #(get other flickr metadata here, and put in f_item)

        f_item['id_num'] = id_num #DEV_REMOVE

        to_return.append(f_item)

        # self.scan_picture(f_item['url'], to_return) DEV_REMOVE

        return to_return

    #use pillow here to scan the picture by URL and populate the other item, and append to to_return
    #ASK TOM ABOUT GARBAGE COLLECTION
    #PIL.Image, StringIO, requests.get()
    #could cause problems with VM if memory gets overloaded
    def scan_picture(self, url, to_return):
        p_item = PictureItem()

        #attempt to prevent memory leak: with statement
        with Image.open(StringIO(requests.get(url).content)) as img:
            length,height = img.size #see comments in items.PictureItem

            p_item['max_lower_pix'] = s.UPPER_PIXEL_THRESHOLD #DEV_REMOVE

            #(get other picture metadata here, ande put in p_item)

            p_item['url'] = url
            p_item['length'] = length
            p_item['height'] = height

        to_return.append(p_item)

