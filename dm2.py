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

def BackupQ(path1, path2, experiment):
	path1files = []
	path2files = []
	
	for root, dirs, files in os.walk(path1):
		for name in files:
			time = os.path.getctime(os.path.join(root, name))
			with open(os.path.join(root, name), 'r+') as f:
				fp = f.read()
			num = hashlib.md5(fp).hexdigest()
			relname = os.path.relpath(os.path.join(root, name), path1)
			path1files.append(relname + " md5checksum value is " + str(num))
	for root, dirs, files in os.walk(path2):
		for name in files:
			time = os.path.getctime(os.path.join(root, name))
			with open(os.path.join(root, name), 'r+') as f:
				fp = f.read()
			num = hashlib.md5(fp).hexdigest()
			relname = os.path.relpath(os.path.join(root, name), os.path.join(path2, experiment))
			path2files.append(relname + " md5checksum value is " + str(num)) 
	a = np.setdiff1d(path1files, path2files)
	b = np.setdiff1d(path2files, path1files)
	if len(a) == 0 and len(b) == 0:
		prGreen("All files exist and are exactly the same in both folders")
	else:	
		if len(a) != 0:		
			print '\n' + path1 + " contains the following files that " + path2 + " does not: "
			for things in a:
				prRed(path1 + '/' + things + ", ")
		if len(b) != 0:		
			print '\n' + path2 + " contains the following files that " + path1 + " does not: "
			for things in b:
				prRed(os.path.join(path2, experiment) + "/" + things + ", ")


experiment = sys.argv[3]
path1 = sys.argv[1]
path2 = sys.argv[2]

BackupQ(path1, path2, experiment)
