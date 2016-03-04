from matplotlib import pyplot as plt
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray
from skimage.io import imread

URL = 'https://farm3.staticflickr.com/2598/3753084645_9136798d32.jpg'
URL2 = 'https://farm2.staticflickr.com/1102/5117093816_a9c4c383c9.jpg'
URL3 = 'https://farm3.staticflickr.com/2643/3753861818_662a81c0c6.jpg'
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

create_blobs(URL3, 'log')
