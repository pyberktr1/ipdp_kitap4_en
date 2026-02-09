# This example shows a sample image process application

# time performance
from time import perf_counter
# operating system library
import os
# image processing library
from PIL import Image as image, ImageFilter as imf, \
    ImageOps as imops

# image files
images = [
    "./image/1.jpg",
    "./image/2.jpg",
    "./image/3.jpg",
    "./image/4.jpg",
    "./image/5.jpg",
]

# image process
def image_process(im_f, im_place ='./'):
    # image file opened
    im = image.open(im_f)

    # image processed
    new_im = imops.invert(im)
    new_im.show("NEGATIVE")

    new_im = imops.posterize(im, 2)
    new_im.show("POSTER")

    new_im = imops.solarize(im, 80)
    new_im.show("SOLARIZE")

    new_im = imops.grayscale(im)
    new_im.show("GRAY SCALE")

    # Gauss blurr filter
    new_im = im.filter(imf.GaussianBlur(16))
    new_im.show("BLURR EFFECT")
    
    # image mirrored
    new_im = im.transpose(method=image.FLIP_TOP_BOTTOM)
    new_im.show("MIRROR")

    # final result recorded to disk
    new_im.save(f"{im_place}/{os.path.basename(im_f)}")
    
    # display a message
    print(f"{im_f} process ok...")
    
    # close image handles
    im.close()
    new_im.close()

# main program block
if __name__ == '__main__':
    
    image_process(images[0])    
