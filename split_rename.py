#!/usr/bin/env python
"""
Script to rename and split mseed data downloaded from a Taurus digitizer.
The data renamed have network field CM and D flag for Seiscomp archive
v(1) 20/10/2015 
Nelson David Perez -- nperez@sgc.gov.co
 
"""
from obspy.core import UTCDateTime
from obspy.core import read
import numpy as np
from glob import glob
import sys
import os

if len(sys.argv)<2:
	print "No input path"
	sys.exit()

#print sys.argv[1:]

for file in sys.argv[1:]:
    st = read(file)
    if len(st)>3:
        stZ = st.select(channel='*Z')
        stZ.merge()
        print stZ
        stE = st.select(channel='*E')
        stE.merge()
        print stE
        stN = st.select(channel='*N')
        stN.merge()
        print stN
        st1 = stZ+stE+stN
        print st1
        for tr in st1:
            if isinstance(tr.data, np.ma.masked_array):
                tr.data = tr.data.filled()
    else:
        st1 = st.copy()


    for tr in st1:
        tr.stats.network = 'CM'
        t = tr.stats.starttime
        if t.julday < 10:
            julday = '00'+str(t.julday)
        elif 10 <= t.julday < 100:
            julday = '0'+str(t.julday)
        else:
            julday = str(t.julday)
        tr_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location+'.'+tr.stats.channel+'.'+'D'+'.'+str(t.year)+'.'+julday
        tr.write(tr_name, format='MSEED')
        print tr_name, '--->   written'
#    st= []        
