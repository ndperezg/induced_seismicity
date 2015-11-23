from obspy.core import read, UTCDateTime, Stream
from glob import glob
import numpy as np
import os
import sys

def cut_traces(sfile):
    s_dict = {}
    infile = open(sfile, 'rU').readlines()
    year = int(infile[0][1:5])
    mm = int(infile[0][6:8])
    dd = int(infile[0][8:10])
    for line in infile:
        if line[79] == '6':
            wave = line.split(' ')[1]
            print wave
            break
    for line in infile:
        if line[9:11] == 'ES' or line[9:11] == 'IS':
            station_name = line[1:6].split(' ')[0]
            s_time = UTCDateTime(year, mm, dd, int(line[18:20]), int(line[20:22]), float(line[23:28]))
            s_dict[station_name]= s_time
            
    st = read(wave)
    st_new = Stream()
    for tr in st:
        if s_dict.has_key(tr.stats.station) == True : 
            tr.trim(s_dict[tr.stats.station]-5,s_dict[tr.stats.station]+15)
            print tr
            st_new.append(tr)
            
    return s_dict, st_new        


    
r, st = cut_traces('06-0503-41L.S201506')

for sta in r:
    print sta, r[sta]
for tr in st:
    tr.plot()
