#!/usr/bin/env python
from segysu2mseed import segysu2mseed
from obspy.core import UTCDateTime
from obspy.core import read
from datetime import datetime
from glob import glob
import sys
import os

start = datetime.now()

if len(sys.argv)<2:
	print "No input path"
	sys.exit()

path = sys.argv[1]
log_file=open(path+'log_segyconvert.out','w+')
os.system('mkdir '+path+'mseed_files')

files = sorted(glob(path+"*.sgy"))

for segy in files:
	try:
		print segy
		segysu2mseed(segy)
		#os.system('mv '+path+'*.mseed '+path+'mseed_files')
	except:
		print >> log_file, 'error in the file '+segy
	pass


log_file.close()

#os.system('mkdir '+path+'mseed_files/conts')
st = read(path+'*.mseed')
st.merge(method=1, fill_value='interpolate')
st.write(path+str(st[0].stats.starttime).split(':')[0]+'.mseed',format='mseed')
os.system('mv '+path+'*.mseed '+path+'mseed_files')
"""
####code implemented for arch data
for tr in st:
	t = tr.stats.starttime
	if t.julday < 10:
		julday = '00'+str(t.julday)
	elif 10 <= t.julday < 100:
		julday = '0'+str(t.julday)
	else:
		julday = str(t.julday)
	tr.write(path+tr.stats.station+'.'+tr.stats.network+'..'+tr.stats.channel+'.'+str(t.year)+'.'+julday, format='MSEED')
"""
end = datetime.now()
os.system('cat '+log_file.name)
print str(start)+'  --  '+str(end)

