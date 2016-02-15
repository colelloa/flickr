
class FlickrPipeline(object):
    def process_item(self, item, spider):
        print '**********************'
        if item.__class__.__name__ == 'FlickrItem':
            self.add_flickr_meta(item)
        elif item.__class__.__name__ == 'BlobItem':
            self.add_blob_item(item)
        else:
            print 'ERROR'
            print item

    def add_flickr_item(self, item):
        print item           

    def add_blob_item(self, item):
        print item
        # print 'PICTURE ITEM YIELDED TO PIPELINE:'
        # print item       