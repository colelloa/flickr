from matplotlib import pyplot as plt
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray
from skimage.io import imread

import system_constants as s


URL = 'https://farm3.staticflickr.com/2598/3753084645_9136798d32.jpg'
URL2 = 'https://farm2.staticflickr.com/1102/5117093816_a9c4c383c9.jpg'
URL3 = 'https://farm3.staticflickr.com/2643/3753861818_662a81c0c6.jpg'

URL4='https://farm3.staticflickr.com/2294/1975875218_0610e6e722.jpg'

PATH_CLASSIFIED='/home/andrew/classes/thesis/python/flickr/pictures/train.arff'
PATH_UNCLASSIFIED = '/home/andrew/classes/thesis/python/flickr/pictures/golfballs.arff'
PATH_WRITE='/home/andrew/classes/thesis/python/flickr/pictures/test.arff'

def create_blobs(url, opt='all'):
    image = imread(url)
    return_dict = dict()
    print 'Image read: {}'.format(url)
    image_gray = rgb2gray(image)

    print 'Greyscale applied'

    if opt=='all':
        blobs_log = blob_log(image_gray, min_sigma=15, max_sigma=50, num_sigma=10, threshold=.1, overlap=0.8) 

        print 'Laplacian of Gaussian computed'
        # Compute radii in the 3rd column.
        blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
        return_dict['LoG'] = blobs_log

        blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
        print 'Difference of Gaussian computed'

        blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)
        return_dict['DoG'] = blobs_dog

        blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)
        print 'Determinant of Hessian computed'

        return_dict['DoH'] = blobs_doh

        blobs_list = [blobs_log, blobs_dog, blobs_doh]
        colors = ['yellow', 'lime', 'red']
        titles = ['LoG', 'DoG',
                  'DoH']
        sequence = zip(blobs_list, colors, titles)
        print 'Sequence created'

    elif opt=='doh':
        print 'DoH only'
        blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)
        return_dict['DoH'] = blobs_doh
        sequence = zip([blobs_doh], ['red'], ['DoH'])

    elif opt=='log':
        print 'LoG only'
        blobs_log = blob_log(image_gray, min_sigma=15, max_sigma=50, num_sigma=10, threshold=.1, overlap=0.8) 

        print 'Laplacian of Gaussian computed'
        # Compute radii in the 3rd column.
        blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
        return_dict['LoG'] = blobs_log
        sequence = zip([blobs_log], ['yellow'], ['LoG'])
    print sequence
    
    fig,axes = plt.subplots(1, 3, sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
    axes = axes.ravel()

    print 'Matplot initialized'
    print sequence
    for blobs, color, title in sequence:
        ax = axes[0]
        axes = axes[1:]
        ax.set_title(title)
        ax.imshow(image, interpolation='nearest')
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            ax.add_patch(c)
    plt.show()
    return return_dict


#convert from arff to a list of dicts
def arff_to_dict(path):
    data = False
    all_list = list()
    with open(path) as f:
        for line in f:
            ret = dict()
            if(data):
                l = line.split(',')
                ret['url'] = l[0]
                ret['algorithm'] = l[1]
                ret['xcenter'] = l[2]
                ret['ycenter'] = l[3]
                ret['meanpx']=l[4]
                ret['medianpx']=l[5]
                ret['modepx']=l[6]
                ret['radius']=l[7]
                ret['radiusheightpct']=l[8]
                ret['radiuswidthpct']=l[9]
                ret['class']=l[10]


                all_list.append(ret)
            if '@DATA' in line:
                data = True
            
    return all_list

#write list of dicts to path
def write_array_dict(target, path):
    with open(path,'a') as f:
        f.write(s.ARFF_HEADER)
        for item in target:
            f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(
                        item['url'], item['algorithm'], item['xcenter'], item['ycenter'], item['meanpx'], item['medianpx'],
                        item['modepx'], item['radius'], item['radiusheightpct'], item['radiuswidthpct'], item['class']))  

def find_classified(entry, cla):
    match = None
    q_url = entry['url']
    for e in cla:
        if e['url'] == q_url:
            match = e
    return match

def classify_set(path_unclassified, path_classified, threshold):
    unc = arff_to_dict(path_unclassified)
    cla = arff_to_dict(path_classified)
    count = 0
    for entry in unc:
        match = find_classified(entry, cla)
        if(match):
            count +=1

            if not('?' in entry['xcenter'] or '?' in entry['ycenter']):
                if((abs(int(entry['ycenter']) - int(match['ycenter'])) < threshold) and
                    (abs(int(entry['xcenter']) - int(match['xcenter'])) < threshold)
                    ):
                    entry['class'] = match['class']

            if '?' in entry['class']:
                entry['class'] = 'NEGATIVE'

    write_array_dict(unc, PATH_WRITE)

classify_set(PATH_UNCLASSIFIED, PATH_CLASSIFIED, 50)
# create_blobs(URL4)

