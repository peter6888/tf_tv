import os, sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from os import listdir
from os.path import isfile, join

def save_thumbnails(infiles, infolder, outfolder, size, appendname = '', verbose=False):
    outsize = size, size
    for infile in infiles:
        if appendname:
            outfilename = join(outfolder, "{}.{}.jpg".format(os.path.splitext(infile)[0], appendname))
        else:
            outfilename = join(outfolder, infile)
        im = Image.open(join(infolder, infile)).convert('L')
        im.thumbnail(outsize, Image.ANTIALIAS)
        im.save(outfilename, "JPEG")
        if verbose:
            print(outfilename)
            print(np.asarray(im).shape)
            imshow(np.asarray(im), cmap = plt.get_cmap('gray'))
            plt.show()