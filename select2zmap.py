#!/usr/bin/env python
import sys
import datetime
import os
import numpy as np

reportINP=open('report.inp','w')
print >> reportINP, "Date TimeE L E LatE LonE Dep E F Aga Nsta Rms Gap McA MlA MbA MsA MwA Fp Spec"
print >> reportINP, "X    X         X  X X  X X   X       X    X   X       X           X"
reportINP.close()

os.system('report select.out report.inp')

namereport='report.out'

if str(os.path.isfile(namereport))=='False':
        print "No Input file: "+namereport
        sys.exit()

report = open('report.out','r')

year, MM, dd, hh, mm, sec, lat, lon, dep, err_lat, err_lon, err_dep,  ml, rms, gap, nsta, mw  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

counter=0
for line in report:
        counter+=1
        if counter>1:
                year.append(int(line[1:5]))
                MM.append(int(line[6:8]))
                dd.append(int(line[8:10]))
                hh.append(int(line[10:13]))
                mm.append(int(line[13:15]))
                sec.append(float(line[16:18]))
                lat.append(float(line[20:28]))
                lon.append(float(line[34:43]))
                dep.append(float(line[49:55]))
                err_lat.append(float(line[29:34]))
                err_lon.append(float(line[44:49]))
                err_dep.append(float(line[56:61]))
                nsta.append(int(line[63:66]))
                rms.append(float(line[68:71]))
                gap.append(int(line[70:74]))
                if line[76:79] == '   ':
                        ml.append(0)
                else:
                        ml.append(float(line[76:79]))
                if line[81:84] == '   ':
                        mw.append(0)
                else:
                        mw.append(float(line[81:84]))


zmap = open('zmap.cat','w')

for i in range(len(year)):
	print lon[i], lat[i], year[i], MM[i], dd[i], ml[i], dep[i], hh[i], mm[i]
	print >> zmap, lon[i], lat[i], year[i], MM[i], dd[i], ml[i], dep[i], hh[i], mm[i]

report.close()
zmap.close() 

