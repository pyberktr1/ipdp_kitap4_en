# This example shows a multi image process application
# which processes multiple images in a parallel fashion

# time performance
from time import perf_counter
# operating system library
import os
# image processing library
from PIL import Image as image, ImageFilter as imf, \
    ImageOps as imops
# multi_porcess library
import multiprocessing as mp

# image files
images = [
    "./image/1.jpg",
    "./image/2.jpg",
    "./image/3.jpg",
    "./image/4.jpg",
    "./image/5.jpg",
]

# image process
def image_process(im_f, im_place ='processed'):
    # im_f image opened from file
    im = image.open(im_f)
    
    # Gaussian blurr filter applied
    im_filt = im.filter(imf.GaussianBlur(16))

    # filtered image mirrored
    im_filt_mirror = im_filt.transpose(method=image.FLIP_TOP_BOTTOM)
    
    # two images are combined into a single image
    (x, y) = im.size
    new_im = image.new('RGB', (x, 2*y), (250,250,250))
    new_im.paste(im, (0,0))
    new_im.paste(im_filt_mirror, (0, y)) 
    new_im = new_im.resize((x//4, y//2))
    
    # final result recorded to disk
    new_im.save(f"{im_place}/{os.path.basename(im_f)}")

    # display a message
    print(f"{im_f} processed ok...")
    
    # close all image handles
    im.close()
    im_filt.close()
    im_filt_mirror.close()
    new_im.close()

# main program block
if __name__ == '__main__':
    
    start = perf_counter()

    # processes created
    processes = [mp.Process(target=image_process, args=[im_f,]) 
                for im_f in images]

    # processes started
    for p in processes:
        p.start()

    # processes waited
    for p in processes:
        p.join()
    
    stop = perf_counter()
    
    print(f" Total execution time {stop - start : 2.5f} seconds")
    
