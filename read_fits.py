
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS

#---text properties---#
bold = '\033[1m'
normal ='\033[0;0m'
#---------------------#


#####This script reads fits files individually######
####################################################
'''
#image = raw_input('Enter the path of the fits file: ')	#input of fits file

#fits_image_hdul = fits.open(image)
fits_image_hdul = fits.open('./spectrums/G192.6005-00.0479_ga20111026_57_spec.fits')

print('\n '+bold+'fits info:'+normal+'\n')
fits_image_hdul.info()


print('\n '+bold+'fits hdul[0] data:'+normal+'\n')
dat = fits_image_hdul[0].data
print(dat)

data = open('dataSpec.txt','w')
#data = open('dataSpecCut.txt','w')

i=0
for i in range(len(dat)):
	print (dat[i])


	data.write('%.13f\n'%(dat[i]))
data.close()


'''

#####This script reads fits files from a list######
###################################################

fitslist = 'spectrums.cut.txt'				# name list of fits files 

fitsimage = np.loadtxt(fitslist, dtype="string", usecols=(0,), unpack=True)

data = open('dataSpecCut.txt','w')

counter=range(len(fitsimage))
for element in counter:
   # print '------------------------------------------------'
   # print fitsimage[element]

    fits_image_hdul = fits.open('./spectrums/'+fitsimage[element])

    dat = fits_image_hdul[0].data
   # print dat
    
    data.write(dat)
data.close()

	

#'''
