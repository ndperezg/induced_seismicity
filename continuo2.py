#!/usr/bin/env python
"""
Script para convertir backup de 2 horas a formas de onda de 1 dia
(c) Nelson David Perez nperez@sgc.gov.co

"""
from obspy.core import read, UTCDateTime, Stream
from datetime import timedelta
import progressbar
import sys
import os

p = progressbar.ProgressBar()

def list_dates(start, end):
	path_dates = []
	day = timedelta(days=1)
	while start <= end:
		if len(str(start.day))==1:
			dia = '0'+str(start.day)
		else:
			dia = str(start.day)
		if len(str(start.month))==1:
			path = '/mnt/continuo2/'+str(start.year)+'/0'+str(start.month)+'/'+str(start.year)+'-0'+str(start.month)+'-'+dia+'-*'
		else:
			path = '/mnt/continuo2/'+str(start.year)+'/'+str(start.month)+'/'+str(start.year)+'-'+str(start.month)+'-'+dia+'-*'
		path_dates.append(path)
		start += day
	return path_dates

def sc_rename(st):
    for tr in st:
        t = tr.stats.starttime
        if t.julday < 10:
            julday = '00'+str(t.julday)
        elif 10 <= t.julday < 100:
            julday = '0'+str(t.julday)
        else:
            julday = str(t.julday)
        tr_name = tr.stats.network+'.'+tr.stats.station+'.'+tr.stats.location+'.'+tr.stats.channel+'.'+'D'+'.'+str(t.year)+'.'+julday
        tr.write(tr_name, format='MSEED')
        print tr_name, '--->   written',  (tr.stats.endtime - tr.stats.starttime)/3600
###################################################################################

streams_path = list_dates(UTCDateTime(2014,01,01), UTCDateTime(2014,12,31))
#print streams_path

for path in p(streams_path):
	st = read(path)
	st.merge(method=0, fill_value='interpolate', interpolation_samples=0)
	#print(st.__str__(extended=True))
	sc_rename(st)
	os.system('mv *2014* /backup/2014_seiscomp/')
