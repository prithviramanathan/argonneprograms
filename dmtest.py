import os
import os.path
import sys
import numpy as np
import math
import time
import timeit
import glob
from itertools import imap
import hashlib
from dm.cat_web_service.api.fileRestApi import FileRestApi

def prRed(prt): 
	print("\033[91m {}\033[00m" .format(prt))

def prGreen(prt): 
	print("\033[92m {}\033[00m" .format(prt))



f1 = time.time()
experiment = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]






def Backup2(experiment, path2, textfile):
	path1files = []
	path2files = []


	api = FileRestApi(username='USERNAME', password='PASSWORD', host='HOST', port=PORT, protocol='https')
	files = api.getExperimentFiles(experiment)
	for x in xrange(0, len(files)):
		path = files[x]['experimentFilePath']
		name = files[x]['fileName']
		if not files[x].has_key('md5Sum'):
		    print name + " does not have an md5sum"
		    with open(textfile, "a") as f:
			    f.write(name + ' does not have md5Sum' + '\n')
		else:
		    num = files[x]['md5Sum']
		    if name != 'core':
			    path1files.append(path + " md5checksum value is " + str(num))
	for root, dirs, files in os.walk(path2):
		for name in files:
			with open(os.path.join(root, name), 'r+') as f:
				fp = f.read()
			num = hashlib.md5(fp).hexdigest()
			relname = os.path.relpath(os.path.join(root, name), os.path.join(path2, experiment))
			if name != 'core':	
				path2files.append(relname + " md5checksum value is " + str(num))
	#print "hi"
	a = np.setdiff1d(path1files, path2files)
	b = np.setdiff1d(path2files, path1files)
	if len(a) == 0 and len(b) == 0:
		prGreen("All files match")
		with open(textfile, "a") as f:
			f.write("All files match")
	else:
		if len(a) != 0:		
			print '\n' + experiment + " contains the following files that " + path2 + " does not: "
			with open(textfile, "a") as f:
				f.write('\n' + experiment + " contains the following files that " + path2 + " does not:" + '\n')
			for things in a:
				prRed(experiment + '/' + things + ", ")
				with open(textfile, "a") as f:
					f.write(experiment + "/" + things + ", " + '\n')
		if len(b) != 0:		
			print '\n' + path2 + " contains the following files that " + experiment + " does not, or these files were not properly cataloged by globus: "
			with open(textfile, "a") as f:
				f.write('\n' + path2 + " contains the following files that " + experiment + " does not, or these files were not properly cataloged by globus: " + '\n')	
			for things in b:
				prRed(os.path.join(path2, experiment) + "/" + things + ", ")
				with open(textfile, "a") as f:
					f.write(os.path.join(path2, experiment) + "/" + things + ", " + '\n')
				


Backup2(experiment, path2, path3)
f2 = time.time()
print str(f2 - f1) + " seconds"
