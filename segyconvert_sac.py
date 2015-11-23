#!/usr/bin/env python
from segysu2sac import segysu2sac
from obspy.core import UTCDateTime
from obspy.core import read
from datetime import datetime
from glob import glob
import numpy as np
import sys
import os

start = datetime.now()

if len(sys.argv)<2:
	print "No input path"
	sys.exit()

path = sys.argv[1]
log_file=open('log_segyconvert.out','w+')
pathsac = path+'sac_files/'
os.system('mkdir '+pathsac)


files = sorted(glob(path+"*.sgy"))


for segy in files:
	try:
		print segy
		segysu2sac(segy)
                os.system('mv output*.sac '+pathsac)
                Files = glob(pathsac+'output*.sac')
		for sac in Files:
			st = read(sac)
			os.system('mv '+sac+' '+pathsac+str(st[0].stats.starttime).split(".")[0]+'_'+st[0].stats.station+'_'+st[0].stats.channel+'.SAC')
	except:
		print >> log_file, 'error in the file '+segy
	pass

st = read(pathsac+'*.SAC')
st.merge()
print "Stream merged"
for tr in st:
        if isinstance(tr.data, np.ma.masked_array):
                tr.data = tr.data.filled()
st.write(pathsac+'/output1.sac', format='sac')

print "SAC file written"

Files = glob(pathsac+'/output1*.sac')
for sac in Files:
        st = read(sac)
        os.system('mv '+sac+' '+pathsac+'/'+str(st[0].stats.starttime).split(":")[0]+'_'+st[0].stats.station+'_'+st[0].stats.channel+'.sac')

os.system('rm -rf '+pathsac+'*.SAC ')





log_file.close()


end = datetime.now()
os.system('cat '+log_file.name)
print str(start)+'  --  '+str(end)





