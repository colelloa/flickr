#connect to database using psycopg2
from sandbox import run_blob

import shutil#dev
import requests#dev

class FlickrPipeline(object):
    def process_item(self, item, spider):
        print '**********************'
        if item.__class__.__name__ == 'FlickrMetaItem':
            self.add_flickr_meta(item)
        elif item.__class__.__name__ == 'PictureItem':
            self.add_picture_item(item)
        else:
            print 'ERROR'
            print item

    def add_flickr_meta(self, item):

        print item['url']
        print item['id_num']
        #DEV
        response = requests.get(item['url'], stream=True)
        with open('pictures/{}.jpg'.format(item['id_num']), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
         #DEV

        # run_blob(item['url'], 'all') DEV
           

    def add_picture_item(self, item):
        pass
        # print 'PICTURE ITEM YIELDED TO PIPELINE:'
        # print item       