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
https://farm3.staticflickr.com/2659/3753867028_73931a286d.jpg

https://farm3.staticflickr.com/2032/3527881656_f0be589676.jpg
https://farm3.staticflickr.com/2452/3753076605_65a1fb419d.jpg
https://farm6.staticflickr.com/5213/5499702132_af85b3c4f6.jpg
https://farm7.staticflickr.com/6238/6269694594_1ffdb581f3.jpg
https://farm6.staticflickr.com/5490/9279832145_ab3387f586.jpg
https://farm4.staticflickr.com/3131/2618131351_3829c92635.jpg
https://farm7.staticflickr.com/6178/6269618452_e4a3411dc7.jpg
https://farm8.staticflickr.com/7205/6850895027_2403bc6999.jpg
https://farm2.staticflickr.com/1292/1391640704_23c231f31b.jpg

https://farm2.staticflickr.com/1051/5140569497_63602dc0a0.jpg
https://farm3.staticflickr.com/2551/3753091335_e5cb47c11f.jpg
https://farm4.staticflickr.com/3206/3001332120_ed81b77c94.jpg
https://farm5.staticflickr.com/4058/4692491212_87d9cdc99c.jpg
https://farm4.staticflickr.com/3206/3001332120_ed81b77c94.jpg
https://farm8.staticflickr.com/7043/6861487717_a51f8705c9.jpg
https://farm9.staticflickr.com/8243/8654383681_da0bbc2b0f.jpg
https://farm7.staticflickr.com/6129/6000443501_631dd97fa5.jpg
https://farm7.staticflickr.com/6071/6084527296_75c2c8301c.jpg


https://farm7.staticflickr.com/6060/5911123057_037043d895.jpg
https://farm8.staticflickr.com/7023/6845379305_bf03af9f36.jpg
https://farm4.staticflickr.com/3106/2459586784_843dc652df.jpg
https://farm3.staticflickr.com/2257/2469289672_25e70ae282.jpg
https://farm8.staticflickr.com/7023/6845379305_bf03af9f36.jpg
https://farm9.staticflickr.com/8287/7736076572_cc8b28969b.jpg
https://farm8.staticflickr.com/7174/6845379565_bb828dc7f1.jpg
https://farm1.staticflickr.com/323/18790636003_6828318059.jpg
https://farm4.staticflickr.com/3106/2459586784_843dc652df.jpg

https://farm7.staticflickr.com/6020/5952464709_197365a797.jpg
https://farm2.staticflickr.com/1321/602728336_1698ba605d.jpg
https://farm5.staticflickr.com/4048/4236808552_da55477e04.jpg
https://farm8.staticflickr.com/7333/10467602134_90cfcb304e.jpg
https://farm4.staticflickr.com/3477/3747546776_7ca1cedf14.jpg
https://farm7.staticflickr.com/6123/5952461529_f838a76e1d.jpg
https://farm7.staticflickr.com/6020/5952464709_197365a797.jpg
https://farm4.staticflickr.com/3165/2983731035_23cf655a26.jpg
https://farm1.staticflickr.com/669/22976842711_26cae62ca0.jpg

'''.split('\n')


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
            id_num = 1#DEV_REMOVE
            for page_num in range(1, total_pages): #iterate through all pages
                for photo in current_page: #iterate through each dict in the list
                    items_to_yield = self.get_flickr_items(photo, id_num, [])

                    if not (items_to_yield[0]['url']  in URLS_VISITED):#dev
                        id_num += 1#DEV_REMOVE
                        if id_num > 10: #DEV_REMOVE
                            break #DEV_REMOVE

                        for i in items_to_yield:
                            yield i
                if id_num > 10: #DEV_REMOVE
                    break #DEV_REMOVE
                #finally, update current page by getting next page
                #since range() goes up to but not including the second arg, page_num+1 will be valid on the final page query and thus valid always
                current_page = self.api.photos.search(text=s.QUERY, per_page=5, extras=s.EXTRAS, sort='relevance', page=page_num+1)['photos']['photo']

        print '*********\nPAGE {0} of {1}'.format(page_num, total_pages)

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

