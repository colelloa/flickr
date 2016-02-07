from matplotlib import pyplot as plt
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray
from skimage.io import imread

image = imread('https://farm3.staticflickr.com/2598/3753084645_9136798d32.jpg')
print 'image read'
image_gray = rgb2gray(image)
print 'image grey'

blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)
print 'blogs logged'
# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
print 'radii computed in 3rd column'

blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
print 'blob dog computed'

blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)
print 'blob doh computed'

blobs_list = [blobs_log, blobs_dog, blobs_doh]
colors = ['yellow', 'lime', 'red']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
          'Determinant of Hessian']
sequence = zip(blobs_list, colors, titles)
print 'shit zipped'

fig,axes = plt.subplots(1, 3, sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
axes = axes.ravel()
print 'shit plotted'
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
