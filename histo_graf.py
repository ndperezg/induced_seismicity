#!/usr/bin/env python2.7
"""
Programa que realiza estadisticas basicas a partir de un select.out 
(formato nordico).

(c) 2014 Nelson Perez <nperez@sgc.gov.co>

v0.1 - 20140312 - N. Perez
v0.2 - 20140904 - V.Dionicio
Histograma por dias de los eventos, lectura del select.inp para los limites de la grafica y el numero de bins

"""

import sys
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, YearLocator, MonthLocator, DayLocator, AutoDateLocator, num2date

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

"""
for i in range(len(ml)):
	print i, type(err_lat[i]), type(ml[i]), gap[i], ml[i]
	if ml[i] == '   ':
		print i, 'ERROR!!!', year[i], MM[i], dd[i]
"""


output=[]
fig=plt.figure(1, figsize=(20,20))

plt.subplot(321)
plt.grid('on')
plt.plot(ml, err_lat, 'bo')
plt.title("Error en latitud vs ML",fontsize=16)
#plt.xlabel('Magnitud Local (Ml)')
plt.ylabel('Error en latitud [km]',fontsize=16)
plt.ylim(0,max(err_lat)+0.1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(322)
plt.grid('on')
plt.plot(ml, err_lon, 'bo')
plt.title("Error en longitud vs ML",fontsize=16)
#plt.xlabel('Magnitud Local (Ml)')
plt.ylabel('Error en longitud [km]',fontsize=16)
plt.ylim(0,max(err_lon)+0.1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(323)
plt.grid('on')
plt.plot(ml, err_dep, 'bo')
plt.title("Error en Profundidad vs ML",fontsize=16)
#plt.xlabel('Magnitud Local (Ml)')
plt.ylabel('Error en profundidad [km]',fontsize=16)
plt.ylim(-0.1,max(err_dep)+0.1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(324)
plt.grid('on')
plt.plot(ml, nsta, 'bo')
plt.title("Numero de estaciones vs Ml",fontsize=16)
plt.xlabel('Magnitud Local (Ml)',fontsize=16)
plt.ylabel('Numero de estaciones',fontsize=16)
plt.ylim(0,max(nsta)+1)
plt.xlim(0,max(ml)+0.1)

plt.subplot(325)
plt.grid('on')
plt.plot(ml, rms, 'bo')
plt.title("RMS vs Ml",fontsize=16)
plt.xlabel('Magnitud Local (Ml)',fontsize=16)
plt.ylabel('RMS')
plt.ylim(-0.03,max(rms)+0.1)
plt.xlim(0,max(ml)+0.1)
#plt.show()
output.append('ErrorDepthVSMl.pdf')
#fig.savefig('figura1.pdf',format='pdf')
fig.savefig(output[0],format='pdf')

"""
##conteo histograma:
bin_gap=[]
ar_gap= np.arange(0,360,5)
for i in range(len(ar_gap)):
	count=0
	for j in range(len(gap)):
		if ar_gap[i]<=gap[j]<ar_gap[i+1]:
			count+=1
	bin_gap.append(count)
print len(ar_gap), len(bin_gap)
print type(ar_gap[0]), type(bin_gap[0])
print ar_gap, bin_gap
"""
#Histogramas
plt.figure(2)
plt.subplot(221)
hist_gap=plt.hist(gap,bins=np.arange(0,360,10))
plt.xlabel('GAP (grados)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(222)
hist_ml=plt.hist(ml,bins=np.arange(0,9,0.5))
plt.xlabel('$M_l$',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(223)
hist_nsta=plt.hist(nsta,bins=np.arange(0,50,1))
plt.xlabel('Numero de estaciones',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)
output.append('StationsVSEvents.pdf')
plt.savefig(output[1])
#plt.savefig('figura2.pdf')

plt.figure(3)
plt.subplot(221)
hist_errlat=plt.hist(err_lat,bins=np.arange(0,100,1))
plt.xlabel('Error en latitud (km)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(222)
hist_errlon=plt.hist(err_lon,bins=np.arange(0,100,1))
plt.xlabel('Error en longitud (km)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)

plt.subplot(223)
hist_errdep=plt.hist(err_dep,bins=np.arange(0,100,1))
plt.xlabel('Error en profundidad (km)',fontsize=8)
plt.ylabel('Numero de sismos',fontsize=8)
#plt.show()
#plt.savefig('figura3.pdf')
output.append('ErrorVSEvents.pdf')
plt.savefig(output[2])

plt.figure(4)
plt.subplot(111)
hist_errdep=plt.hist(dep,bins=np.arange(0,600,5))
plt.xlabel('Profundidad (km)',fontsize=16)
plt.ylabel('Numero de sismos',fontsize=16)
#plt.savefig('figura4.pdf')
output.append('DepthVSEvents.pdf')
plt.savefig(output[3])

plt.figure(5)
plt.subplot(111)
hist_errdep=plt.hist(rms,bins=np.arange(0,2,0.1))
plt.xlabel('RMS',fontsize=16)
plt.ylabel('Numero de sismos',fontsize=16)
#plt.savefig('figura5.pdf')
output.append('RMSVSEvents.pdf')
plt.savefig(output[4])



###HISTOGRAMA POR DIAS

#plt.figure(3, figsize(20,20))

Dates = []

for fec in range(len(year)):
	Dates.append(str(year[fec])+'-'+str(MM[fec])+'-'+str(dd[fec]))
	Dates[fec] = datetime.datetime.strptime(Dates[fec], '%Y-%m-%d')

#Reding from select.inp the start and end time and calculate the bins number
selectINP=open('select.inp')
for line in selectINP:
  if 'Start' in line:
	ini_year=line[32:36]
	ini_month=line[36:38]
	ini_day=line[38:40]
	ini_hour=line[40:42]
	StartTime=ini_year+'-'+ini_month+'-'+ini_day
	numStartTime=date2num(datetime.datetime.strptime(StartTime, '%Y-%m-%d'))
  if 'End' in line:
	end_year=line[32:36]
	end_month=line[36:38]
	end_day=line[38:40]
	end_hour=line[40:42]
	EndTime=end_year+'-'+end_month+'-'+end_day
	numEndTime=date2num(datetime.datetime.strptime(EndTime, '%Y-%m-%d'))
  if 'Minimum latitude' in line:
	minLat=line[39:45]
  if 'Maximum latitude' in line:
	maxLat=line[39:45]
  if 'Minimum longitude' in line:
	minLon=line[39:45]
  if 'Maximum longitude' in line:
	maxLon=line[39:45]
print minLat, maxLat, minLon, maxLon
nBins=numEndTime-numStartTime
selectINP.close()

(hist, bin_edges) = np.histogram(date2num(Dates), nBins)
width = bin_edges[1] - bin_edges[0]
fig = plt.figure(6)
ax = fig.add_subplot(111)
ax.bar(bin_edges[:-1], hist, width=width)
ax.set_xlim(numStartTime, numEndTime)
ax.set_ylabel('Numero de eventos')
ax.set_xlabel('Intervalo de Tiempo '+StartTime+' y '+EndTime)
#ax.set_title('Ocurrencia de eventos diarios entre '+StartTime+' y '+EndTime+'\n Entre las coordenadas '+ minLon+'<Lon<'+maxLon+' y '+ minLat+'<Lat<'+maxLat+'  \n Numero total de eventos '+str(len(Dates)))
ax.set_title('Eventos diarios entre '+ minLon+'<Lon<'+maxLon+' y '+ minLat+'<Lat<'+maxLat+'  \n Numero total de eventos '+str(len(Dates)))
ax.xaxis.set_major_locator(AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax.xaxis.set_minor_locator(MonthLocator())
ax.format_xdata = DateFormatter('%Y-%m-%d')
ax.grid(True)
fig.autofmt_xdate()
#plt.savefig('figura6.pdf')
output.append('FrequencyVSEvents.pdf')
plt.savefig(output[5])
plt.show()

print 'Output: ', output

#for i in range(1,7):
#	print 'Output: figura'+str(i)+'.pdf'
