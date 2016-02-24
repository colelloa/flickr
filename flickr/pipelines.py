
import flickr.system_constants as s

class FlickrPipeline(object):
    def __init__(self):
            with open(s.ARFF_FILE_LOCATION, 'w') as f:
                f.write(s.ARFF_HEADER)

    def process_item(self, item, spider):
        print '**********************'
        if item.__class__.__name__ == 'BlobItem':
            self.add_blob_item(item)
        else:
            print 'ERROR'
            print item
            
    def add_blob_item(self, item):
        print item  
        with open(s.ARFF_FILE_LOCATION, 'a') as f:
                f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(
                    item['url'], item['algorithm'], item['x_center'], item['y_center'], item['mean_px'], 
                    item['median_px'], item['mode_px'], item['radius'], item['radius_hpct'], item['radius_wpct'], item['b_class']))     