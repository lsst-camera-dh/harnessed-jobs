#from AssembleImage import AssembleImage
import lsst.afw.display.ds9 as ds9
import lsst.afw.image as afwImage 
from os import listdir
import numpy as np


file_dir = '/mnt/hgfs/VMShared/2016MAY/113-03/sflat_acq/v0/15008/fits/'

for i in range(2,18):
    hdu=i
    if i>9: segnumber=hdu
    else: segnumber='0%s'%hdu
    filenames = listdir(file_dir)
    print 'Found %s files'%len(filenames)
        
    example_image = afwImage.ImageF(file_dir+filenames[0],hdu)
    x_size = example_image.getWidth()
    y_size = example_image.getHeight()
       
    image = afwImage.ImageF(x_size, y_size, 0.0)
    image_array = image.getArray()
    
    for filename in filenames:
        image_array += (afwImage.ImageF(file_dir + filename,hdu).getArray())
    image_array /= len(filenames)
    image.writeFits('noise_%s.fits'%segnumber)

    print 'segment number is' , hdu
 
print 'done'
exit()






