#!/usr/bin/env python
"""
Function that converts SEG-Y data to MSEED trace of PRE

""" 

from obspy.core import read
from glob import glob
import numpy as np
import sys
import os

def segysu2mseed(sismosegy):
	head = 'header'
	metadata = 'metadata.out'
	os.system('segyread tape='+sismosegy+' verbose=1 endian=0 | segyclean > data.su')
	if str(os.path.isfile(head))=='False':
		print "Error: no file "+head
		sys.exit()
	os.system('sugethw < data.su key=tracl,fldr,trid >'+metadata)
	if str(os.path.isfile(metadata))=='False':
		print "Error: no file "+metadata
		sys.exit()
	os.system("awk \'{if (NF == 3) print $1, $2, $3 }\' "+metadata+" > metadata1.out")
	filemetadata = open("metadata1.out", 'r')
	station, channel = [], []
	for line in filemetadata:
		station.append(line.split(" ")[1].split("=")[1].strip())
		channel.append(line.split(" ")[2].split("=")[1].strip())

	st = read(sismosegy, format="SEGY")
	if len(st) != len(station) or len(st) != len(channel):
		print "ERROR: metadata not match with stream number"
		sys.exit()
	for i in range(len(st)):
		st[i].stats.network = 'PR'
		st[i].stats.station = station[i]
		if channel[i] == '15':
			st[i].stats.channel = 'BHZ'
		elif channel[i] == '16':
			st[i].stats.channel = 'BHE'
		elif channel[i] == '17':
			st[i].stats.channel = 'BHN'
	for tr in st:
		tr.data = 1000000000000*tr.data
		tr.data = np.require(tr.data, dtype = "int32")
	st.write(sismosegy.split(".")[0]+".mseed", format="mseed", encoding= 10)	
	st1 = read(sismosegy.split(".")[0]+".mseed")
	return(0)
