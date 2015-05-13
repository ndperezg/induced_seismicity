#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#Calcula energia radiada del catalogo de spectraseis
########################################################################################################################
import numpy as np
import sys
import os 
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, YearLocator, MonthLocator, DayLocator, AutoDateLocator, num2date
########################################################################################################################

#--------------------Lee parametros de entrada y convierte fechas
if len(sys.argv)<2:
	start = datetime.datetime.strptime("2014/01/01",'%Y/%m/%d')
	end = datetime.datetime.strptime("2014/12/31",'%Y/%m/%d')
	print "Se hara el calculo de la energia para todo el catalogo"
else:
	start=datetime.datetime.strptime(sys.argv[1],'%Y/%m/%d')
	end = datetime.datetime.strptime(sys.argv[2], '%Y/%m/%d')
	print "Energia entre", sys.argv[1],'--', sys.argv[2]
#------------------------------------------------------------------

#---Lee archivo de texto y crea arreglos con fecha y magnitud
Caud, presiones,fecha_inyeccion, falta = [], [], [], []
Magnitudes, Fechas = [], []
eventos = ['2014-03-17','2014-03-24','2014-03-27','2014-04-23','2014-05-13','2014-05-25','2014-06-04','2014-06-25','2014-08-09','2014-11-30']
for fec in range(len(eventos)):
	eventos[fec] = datetime.datetime.strptime(eventos[fec], '%Y-%m-%d')
#----------------------------------------------------------------------

#--------------Lee archivos de texto---------------------------------
pacific = open('TablaCaudalesPresiones2014.txt', 'rU')
counter = 0
for line in pacific:
	counter +=1
	if counter > 1:
		 fecha_inyeccion.append(line.split()[0])
		 Caud.append(float(line.split()[1]))
		 presiones.append(float(line.split()[2]))
	         falta.append(line[45:93])		
for fec in range(len(fecha_inyeccion)):
	fecha_inyeccion[fec] = datetime.datetime.strptime(fecha_inyeccion[fec], '%Y-%m-%d')
		
spectraseis = open('catalogo_spectraseis.txt', 'rU')
for line in spectraseis.readlines():
	Magnitudes.append(float(line.split()[5]))
	Fechas.append(line.split()[2]+'/'+line.split()[3]+'/'+line.split()[4])
spectraseis.close()
#------------------------------------------------------------------------------

#-------------Calcula la energía a partir de la magnitud Mw-------------------
mag = np.array(Magnitudes)
E = np.power(10,1.5*mag+11.8)

for fec in range(len(Fechas)):
	Fechas[fec] = datetime.datetime.strptime(Fechas[fec], '%Y/%m/%d')

#----------------------------------------------------------------------------


"""
for date,mag,E in zip(Fechas, mag, E):
	print date, mag, E
"""

#---funcion que calcula energia radiada por dia-------------------------------

def suma_dia_energia(dia, date, E):
	lista_dia = []
	for d, e in zip(date, E):
		if d == dia:
			lista_dia.append(e)
	suma = np.sum(np.array(lista_dia))
	return suma
#-------------------------------------------------
#----Crea listas para histogramas----------------------------------------------
hist_dates, energy, e_acumulada = [], [], []

for fecha in Fechas:
	if fecha in hist_dates:
		pass
	else:
		hist_dates.append(fecha)
		energy.append(suma_dia_energia(fecha,Fechas, E))
e_cum=0
for e in energy:
	e_cum += e
	e_acumulada.append(e_cum)


#------------------------------Figura con frecuencia de sismos--------------------------------
nBins = 361
(hist, bin_edges) = np.histogram(date2num(Fechas), nBins)
width = bin_edges[1] - bin_edges[0]
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.bar(bin_edges[:-1], hist, width=width)
ax.set_xlim(start, end)
ax.set_ylabel('Numero de eventos')
ax.xaxis.set_major_locator(AutoDateLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax.xaxis.set_minor_locator(MonthLocator())
ax.format_xdata = DateFormatter('%Y-%m-%d')
ax.grid(True)
fig.autofmt_xdate()
plt.show()


#----------------------------Figura con energía acumulada-------------------------------------

fig1 = plt.figure(2)
ax1 = fig1.add_subplot(111)
#ax1.bar(Fechas, E, width=width)
ax1.plot(hist_dates, e_acumulada, color='r', linewidth = 2.5, label='Energia acumulada')
ax1.set_xlim(start, end)
ax1.xaxis.set_major_locator(AutoDateLocator())
ax1.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax1.xaxis.set_minor_locator(MonthLocator())
ax1.format_xdata = DateFormatter('%Y-%m-%d')
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_xlabel("Date",fontsize=18)
ax1.grid(True)
ax2 = ax1.twinx()
#ax2.bar(hist_dates, energy, width=width)
ax2.bar(bin_edges[:-1], hist, width=width, alpha = 0.5, label='Numero de sismos')
fig1.autofmt_xdate()

for fec in range(len(hist_dates)):
	if hist_dates[fec] in eventos:
		if hist_dates[fec] == eventos[0]:
			ax2.plot(hist_dates[fec], hist[fec], '*',color='y',markersize=20, label='Evento')
		else:
			ax2.plot(hist_dates[fec], hist[fec], '*',color='y', markersize=20)

for label in ax1.get_yticklabels():
    label.set_color("red")
ax1.set_ylabel('Cummulative Energy (dyn-cm)', fontsize = 18, color = 'r')
for label in ax2.get_yticklabels():
    label.set_color("b")
ax2.set_ylabel('Number of earthquakes/day', fontsize = 18, color = 'b')
ax2.legend(loc=2)
plt.show()

#----------------------------------Energia diaria VS energia acumulada------------------------------------

fig2 = plt.figure(3)
ax1 = fig2.add_subplot(111)
#ax1.bar(Fechas, E, width=width)
ax1.plot(hist_dates, e_acumulada, color='r', linewidth = 2.5)
ax1.set_xlim(start, end)
ax1.xaxis.set_major_locator(AutoDateLocator())
ax1.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax1.xaxis.set_minor_locator(MonthLocator())
ax1.format_xdata = DateFormatter('%Y-%m-%d')
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_xlabel("Date",fontsize=18)
ax1.grid(True)
ax2 = ax1.twinx()
ax2.bar(hist_dates, energy, width=width, alpha = 0.5)
#ax2.bar(bin_edges[:-1], hist, width=width, alpha = 0.5)
fig2.autofmt_xdate()

for fec in range(len(hist_dates)):
	if hist_dates[fec] in eventos:
		ax2.plot(hist_dates[fec], energy[fec], '*',color='y',markersize=30)

for label in ax1.get_yticklabels():
    label.set_color("red")
ax1.set_ylabel('Cummulative Energy (dyn-cm)', fontsize = 18, color = 'r')
for label in ax2.get_yticklabels():
    label.set_color("b")
ax2.set_ylabel('Daily energy (dyn-cm)', fontsize = 18, color = 'b')
plt.show()

#-------------------------------Caudal---------------------------------------

fig3 = plt.figure(3)
ax1 = fig3.add_subplot(111)
#ax1.bar(Fechas, E, width=width)
ax1.plot(fecha_inyeccion, Caud, color='cyan', linewidth = 2.5)
ax1.set_xlim(start, end)
ax1.xaxis.set_major_locator(AutoDateLocator())
ax1.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax1.xaxis.set_minor_locator(MonthLocator())
ax1.format_xdata = DateFormatter('%Y-%m-%d')
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_xlabel("Date",fontsize=18)
ax1.grid(True)
ax2 = ax1.twinx()
#ax2.bar(hist_dates, energy, width=width)
ax2.bar(bin_edges[:-1], hist, width=width, alpha = 0.5)
for num in range(len(fecha_inyeccion)):
	if 'Faltan datos de caudal' in falta[num]:
		ax1.plot(fecha_inyeccion[num], Caud[num]+10000,'ko', marker= r'$\downarrow$', markersize=20, label = 'Faltan datos de caudal')
fig3.autofmt_xdate()

for fec in range(len(hist_dates)):
	if hist_dates[fec] in eventos:
		ax2.plot(hist_dates[fec], hist[fec], '*',color='y',markersize=30)

for label in ax1.get_yticklabels():
    label.set_color("cyan")
ax1.set_ylabel('Caudal (BWPD)', fontsize = 18, color = 'cyan')
for label in ax2.get_yticklabels():
    label.set_color("b")
ax2.set_ylabel('Number of earthquakes/day', fontsize = 18, color = 'b')
plt.show()

#-------------------------------------Presiones----------------------------------

fig4 = plt.figure(3)
ax1 = fig4.add_subplot(111)
#ax1.bar(Fechas, E, width=width)
ax1.plot(fecha_inyeccion, presiones, color='green', linewidth = 1.5)
ax1.set_xlim(start, end)
ax1.xaxis.set_major_locator(AutoDateLocator())
ax1.xaxis.set_major_formatter(DateFormatter('%Y/%m/%d'))
ax1.xaxis.set_minor_locator(MonthLocator())
ax1.format_xdata = DateFormatter('%Y-%m-%d')
ax1.xaxis.set_tick_params(labelsize=12)
ax1.set_xlabel("Date",fontsize=18)
ax1.grid(True)
ax2 = ax1.twinx()
#ax2.bar(hist_dates, energy, width=width)
ax2.bar(bin_edges[:-1], hist, width=width, alpha = 0.5)
for num in range(len(fecha_inyeccion)):
	if 'Faltan datos de presion' in falta[num]:
		ax1.plot(fecha_inyeccion[num],presiones[num],'ko',marker= 's' , markersize=5, label = 'Faltan datos de presion')
fig4.autofmt_xdate()

for fec in range(len(hist_dates)):
	if hist_dates[fec] in eventos:
		ax2.plot(hist_dates[fec], hist[fec], '*',color='y',markersize=30)

for label in ax1.get_yticklabels():
    label.set_color("green")
ax1.set_ylabel('Pressure (PSI)', fontsize = 18, color = 'green')
for label in ax2.get_yticklabels():
    label.set_color("b")
ax2.set_ylabel('Number of earthquakes/day', fontsize = 18, color = 'b')
plt.show()

print len(hist_dates), len(energy), len(bin_edges[:-1]), len(hist), len(falta)

#prueba = suma_dia_energia('2014/12/07', Fechas, E)
#print prueba 


		
			


