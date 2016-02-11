from matplotlib import pyplot as plt
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray
from skimage.io import imread

URL = 'https://farm3.staticflickr.com/2598/3753084645_9136798d32.jpg'

def run_blob(url, opt='all'):
    image = imread(url)
    print 'Image read: {}'.format(url)
    image_gray = rgb2gray(image)
    print 'Greyscale applied'

    if opt=='all':
        blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1) 

        print 'Laplacian of Gaussian computed'
        # Compute radii in the 3rd column.
        blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

        blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
        print 'Difference of Gaussian computed'

        blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

        blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)
        print 'Determinant of Hessian computed'

        blobs_list = [blobs_log, blobs_dog, blobs_doh]
        colors = ['yellow', 'lime', 'red']
        titles = ['LoG', 'DoG',
                  'DoH']
        sequence = zip(blobs_list, colors, titles)
        print 'Sequence created'
    elif opt=='doh':
        print 'DoH only'
        blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)

        print blobs_doh
imshow(image, interpolation='nearest')
        sequence = zip([blobs_doh], ['red'], ['DoH'])

    # fig,axes = plt.subplots(1, 1, sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
    # axes = axes.ravel()

    print 'Matplot initialized'

    for blobs, color, title in sequence:
        # ax = axes[0]
        # axes = axes[1:]
        # ax.set_title(title)
        # ax.imshow(image, interpolation='nearest')
        imshow(image, interpolation='nearest')
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
            # ax.add_patch(c)

    plt.show()

run_blob(URL, 'doh')
