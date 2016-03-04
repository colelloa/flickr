# A. Colello 2016
# flickr picture scraper
#   to run:
#       navigate to python/flickr  
#       scrapy crawl picture

import scrapy
import flickrapi
import requests
import numpy

from StringIO import StringIO
from PIL import Image
from scipy.stats import mode

import flickr.system_constants as s
import flickr.training_data as td

from flickr.items import BlobItem
from flickr.sandbox import create_blobs

class PictureSpider(scrapy.Spider):
    name = "picture"
    allowed_domains = ["www.google.com", "www.flickr.com"]
    start_urls = (
        'http://www.google.com/', #placeholder; not actually used because I use the flickr api to query/iterate, but scrapy needs a url to start
    )
    api = flickrapi.FlickrAPI(s.API_KEY, s.API_SECRET, format='parsed-json')

    def parse(self, response):
        if not s.SYS_TRAIN:
            q = self.api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance') #initial query
            if q['stat'] == 'ok': #successful query
                all_photos = q['photos']
                total_pages = all_photos['pages']
                current_page = all_photos['photo'] #get page 1; list of dicts

                for page_num in range(1, total_pages): #iterate through all pages
                    print '*********\nPAGE {0} of {1}'.format(page_num, total_pages) #PAGE 15 AND UP = IRRELEVANT RESULTS
                    for photo in current_page: #iterate through each dict in the list
                        items_to_yield = self.get_blobs(photo, [])

                        for i in items_to_yield:
                            yield i

                    #finally, update current page by getting next page
                    #since range() goes up to but not including the second arg, page_num+1 will be valid on the final page query and thus valid always
                    current_page = self.api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance', page=page_num+1)['photos']['photo']
        else:
            raw= td.RAW_TRAINING_DATA
            data = td.prepare_training_data(raw)
            to_return = list()
            for preproc in data:
                url = preproc[0]
                blob=preproc[1] #[y,x,radius]
                item = self.scan_blob(url, 'MANUAL', blob)
                yield item
            

    def get_blobs(self, photo, to_return):
        url = s.BASE_URL.format(photo['farm'], photo['server'], photo['id'], photo['secret'])
        all_blobs = create_blobs(url, 'log') # returns a dict; key=name of alg, value = corresponding list of blob candidates with [y,x,radius]
                    #DOH = DEV?
        for alg_name in all_blobs: 
            for blob in all_blobs[alg_name]:
                to_return.append(self.scan_blob(url, alg_name, blob))

        return to_return

    #use pillow here to scan the blob by URL, populate blob item, and append to_return
    def scan_blob(self, url, alg, blob):
        b_item = BlobItem()
        print blob
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
        if rad > 0:
            with Image.open(StringIO(requests.get(url).content)) as img:
                orig_width, orig_height = img.size
                b_item['radius_hpct'] =  rad / float(orig_height)
                b_item['radius_wpct'] = rad / float(orig_width)
                left_x = x-rad
                left_y = y-rad

                leng = rad * 2

                x_bound = (leng+left_x) if (leng+left_x < orig_width) else orig_width
                y_bound = (leng+left_y) if (leng+left_y < orig_height) else orig_height 
                

                print 'radius:{}'.format(rad)
                print '(x,y):{0},{1}'.format(x,y)
                print 'length:{}'.format(orig_height)
                print 'width:{}'.format(orig_width)
                box = (left_x, left_y, x_bound, y_bound)
                print 'box:{}'.format(box)

                with img.crop(box) as circ_img:  #select box starting at left corner from x,y center of len/width rad
                    
                    circ_img.load()

                    pix_val = list(circ_img.getdata())
                    
                    pix_val_flat = [x for sets in pix_val for x in sets]
                    
                    b_item['mean_px'] = numpy.mean(pix_val_flat)
                    b_item['median_px'] = numpy.median(pix_val_flat)
                    b_item['mode_px'] = mode(pix_val_flat)[0][0]

        if s.SYS_TRAIN:
            if rad > 0:
                b_item['b_class'] = 'POSITIVE'
            else:
                b_item['b_class'] = 'NEGATIVE'

        return b_item

