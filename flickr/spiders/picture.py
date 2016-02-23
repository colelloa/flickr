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

import flickr.system_constants as s

from flickr.items import FlickrItem, BlobItem
from flickr.sandbox import create_blobs

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

            lim = 0 #DEV
            for page_num in range(1, total_pages): #iterate through all pages
                print '*********\nPAGE {0} of {1}'.format(page_num, total_pages) #PAGE 15 AND UP = IRRELEVANT RESULTS
                for photo in current_page: #iterate through each dict in the list
                    items_to_yield = self.get_flickr_items(photo, [])

                    for i in items_to_yield:
                        yield i

                lim += 1 #DEV
                if lim >  1: #DEV
                    break #DEV

                #finally, update current page by getting next page
                #since range() goes up to but not including the second arg, page_num+1 will be valid on the final page query and thus valid always
                current_page = self.api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance', page=page_num+1)['photos']['photo']


    #param: dict of one photo on a page
    def get_flickr_items(self, photo, to_return):
        f_item = FlickrItem()

        f_item['url'] = s.BASE_URL.format(photo['farm'], photo['server'], photo['id'], photo['secret'])
        #https://www.flickr.com/services/api/misc.urls.html

        #(get other flickr metadata here, and put in f_item)

        to_return.append(f_item)

        self.get_blobs(f_item, to_return)

        return to_return

    def get_blobs(self, f_item, to_return):
        url = f_item['url']
        all_blobs = create_blobs(url, 'doh') # returns a dict; key=name of alg, value = corresponding list of blob candidates with [y,x,radius]
                    #DOH = DEV
        for alg_name in all_blobs: 
            for blob in all_blobs[alg_name]:
                to_return.append(self.scan_blob(url, alg_name, blob))

        return to_return

    #use pillow here to scan the blob by URL, populate blob item, and append to_return
    def scan_blob(self, url, alg, blob):
        b_item = BlobItem()
        x = blob[1]
        y = blob[0]
        rad = blob[2]

        b_item['url'] = url
        b_item['algorithm'] = alg
        b_item['y_center'] = y
        b_item['x_center'] = x
        b_item['radius'] = rad

        b_item['mean_px'] = '?'
        b_item['median_px'] = '?'
        b_item['mode_px'] = '?'
        b_item['radius_hpct'] = '?'
        b_item['radius_wpct'] = '?'

        b_item['b_class'] = '?'

        print 'OPENING BLOB'

        with Image.open(StringIO(requests.get(url).content)) as img:
            orig_width, orig_height = img.size
            b_item['radius_hpct'] =  rad / orig_height
            b_item['radius_wpct'] = rad / orig_width
            circ_img = img.crop(x-(rad/2), y-(rad/2), rad, rad) #select box starting at left corner from x,y center of len/width rad
            
            
        return b_item

