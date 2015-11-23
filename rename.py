from obspy.core import read
from glob import glob
import os
import sys

files = glob('*.sac')
for sac in files:
	st = read(sac)
	print st[0]
	os.system('mv '+sac+' 20140327_'+st[0].stats.station+'_'+st[0].stats.channel+'.sac')
