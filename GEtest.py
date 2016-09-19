import os
import os.path
import sys
import numpy as np
import math
import time
import glob
from itertools import imap



#to get different color texts
def prRed(prt): 
	print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): 
	print("\033[92m {}\033[00m" .format(prt))



# Finds how many pixels are above a certain saturation in an image
def NreadGE(filename, frameno, thresh):
	buffer = 8192
	fp = open(filename, 'rn')
	dims = 2048*2048
	offset  = buffer + (frameno-1)*dims*2
	fp.seek(offset) 
	img = np.fromfile(fp, 'uint16', dims)	
	return np.count_nonzero(img > thresh)
	#return sum(i >= thresh for i in img)
	#tot = reduce(lambda count, i: count + my_condition(i, thresh), img, 0)
	#return tot


#loads all frames at once and return number of saturated pixels
def T3readGE(filename, thresh):
	buffer = 8192
	fp = open(filename, 'rn')
	offset  = buffer
	dims = 2048*2048
	frames = (os.stat(filename).st_size - 8192)/ 8000000
	fp.seek(offset) 
	#img = np.fromfile(fp, 'uint16', 2048*2048*(os.stat(filename).st_size - 8192)/ 8000000)
	img = np.fromfile(fp, 'uint16', dims * frames)
	#return len([i for i in img if float(i) >= thresh])
	tot = np.count_nonzero(img > thresh)
	return tot
 

# automatically retreive new images uploaded to a directory and runs the code
def AreadGE(path, thresh, numpix, ext):
	# if the provided threshold is too large
	thresh = int(thresh)
	numpix = int(numpix)
	now = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and os.path.join(path,f).endswith(ext)])
	previous = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and os.path.join(path,f).endswith(ext)])
	while 1:
		time.sleep(5)
		#allfiles = []
		#for fily in os.listdir(path):
		#	if fily.endswith('.ge3'):
		#		allfiles.append(fily)
		#if len(allfiles)>0:
		#newest = max([f for f in os.listdir(path) if f.lower().endswith('.ge3')], lambda k: int(os.path.getctime(os.path.join(path,k))))
		maxt = 0
		newest = None
		now = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and os.path.join(path,f).endswith(ext)])
		for f in os.listdir(path):
			if os.path.isfile(os.path.join(path,f)) and os.path.join(path,f).endswith(ext):
				if os.path.getctime(os.path.join(path,f)) > maxt:
					maxt = os.path.getctime(os.path.join(path,f))
					newest = f
		#print newest
		#print newest[len(newest) - 1]
			#print newest1
			#print newest[1]
		if now > previous:
	#		if newest.lower().endswith('.ge3'):
	#	newest = max([f for f in os.listdir(path) if f.lower().endswith('.ge3')], key=os.path.getctime)
	#		print newest
			t1 = time.time()
			tot = T3readGE(os.path.join(path, newest), thresh)
	#		print tot
			t2 = time.time()		
			if tot > numpix:		
				prRed(newest + " has " + str(tot) + " saturated pixels above the threshold of " + str(thresh))
			else:
				prGreen(newest + " has " + str(tot) + " saturated pixels above the threshold of " + str(thresh))
			print "Program took " + str(t2 - t1) + " seconds"
			previous = now
		newest = None



	

			
try:
	path = sys.argv[1]
	thresh = int(sys.argv[2])
	numpix = int(sys.argv[3])
	ext = sys.argv[4]
	if thresh > 16383 or thresh <= 0:
		thresh = 16000
		print "The provided threshold is too large. The threshold has been reset to " + str(thresh)
	if os.path.exists(path) == False:
		print "The given path is not a valid path to a directory. Try providing an absolute path to the directory."
	AreadGE(path,thresh,numpix,ext)
except:
	print '\n' + "The function requires 4 inputs. First input is the directory to be monitored. Second input is the intensity threshold. Third input is the number of saturated pixels before a warning is given (warning will print in red). Fourth input is the file extension." + '\n' + "Format: python GEtest.py 'directory' threshold pixels 'extension' " + '\n' + "Example: python GEtest.py 'directory' 10000 120000 '.ge3' " + '\n' + '\n'


