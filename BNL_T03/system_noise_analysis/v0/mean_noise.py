import pyfits
import lsst.afw.display.ds9 as ds9
import os
from os import listdir
import numpy as np
ignored_states = np.seterr(all='ignore')
from random import randint

class getCol:
    matrix = []
    def __init__(self, file, delim=" "):
        with open(file, 'rU') as f:
            getCol.matrix =  [filter(None, l.split(delim)) for l in f]
    
    def __getitem__ (self, key):
        column = []
        for row in getCol.matrix:
            try:
                column.append(row[key])
            except IndexError:
                # pass
                column.append("")
        return column   

def arrayBox(m, r_number, c_number):
    result_array=[]
    for row in range(r_number, r_number+100):
        for column in range(c_number, c_number+100):
            f_on_pix=m[column][row]
            result_array=np.append(result_array,[f_on_pix])
    return result_array
def sumBox(m, r_number, c_number):
    total = 0
    for row in range(r_number,r_number+100):
        for column in range(c_number,c_number+100):
            total += m[column][row]
    return total
        
save_mean='/mnt/hgfs/VMShared/2016MAY/101/noise_final.txt'
g=open(save_mean,'w')
dir = '/mnt/hgfs/VMShared/2016MAY/101/segments/'
savedir='/mnt/hgfs/VMShared/2016MAY/101/sum/'
filenames = listdir(dir)
seg=0
for name in filenames:
    filename=dir+name
    print filename

    save_file= savedir+ os.path.splitext(os.path.split(filename)[1])[0]+ '.txt'
    f=open(save_file,'w')       

    hdulist=pyfits.open(filename)

    xsum,ysum=[],[]

    #data=hdulist[0].data
    data=pyfits.getdata(filename)
    head=hdulist[0].header
    for k in range(0, 500):
        i=randint(10,422)
        j=randint(0,1902)
        boxstd=np.std(arrayBox(data, i, j))
        string="%s %s %s \n" %(i, j,boxstd)
        f.write(string)
    f.close()

    seg+=1
    flux=getCol(save_file)[2]
    medstdflux=np.median(np.asanyarray(flux,float))
    string2="%s %s \n" %(seg, medstdflux)
    print string2
    g.write(string2)
g.close()    
print "done"
exit()