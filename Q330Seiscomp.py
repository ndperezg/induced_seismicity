#!/usr/bin/env python
from obspy.core import read, UTCDateTime, Stream
from datetime import timedelta

def trim_tails(tr):
	day = timedelta(days=1)
	second = timedelta(seconds=1)
	t1 = tr.stats.starttime
	t2 = tr.stats.endtime
	t_in =  UTCDateTime((t1+day).year, (t1+day).month, (t1+day).day, 00, 00, 00)
	t_out = UTCDateTime((t2-day).year, (t2-day).month, (t2-day).day, 23, 59, 59.99)
	tr1 = tr.copy()
	tr2 = tr.copy()
	tr3 = tr.copy()
	ST = Stream()
	if t_in == t1:
		tr1.trim(t1, t_out)
		tr2.trim(t_out + second, t2)
		#ST.append(tr1)
		ST.append(tr2)
	elif t_out == t2:
		tr2.trim(t1, t_in) 
		tr1.trim(t_in, t2)
		ST.append(tr2)
		#ST.append(tr1)
	elif t_in == t1 and t_out == t2:
		tr1.trim(t1,t2)
		#ST.append(tr1)
	else:
		tr2.trim(t1, t_in)
		tr3.trim(t_out + second, t2)
		tr1.trim(t_in, t_out)
		#ST.append(tr1)
		ST.append(tr2)
		ST.append(tr3)
	print t1, t2
	print t_in, t_out
	while t_out > t_in:
		tr_cut = tr1.copy()
		tr_cut.trim(t_in + second, t_in + day)
		print tr_cut
		ST.append(tr_cut)
		t_in += day
	return ST

def sc_rename(st):
    for tr in st:
        tr.stats.network = 'CM'
        tr.stats.location = '00'
        if tr.stats.channel == 'SHZ':
                tr.stats.channel = 'EHZ'
                tr.stats.location = '20'
        if tr.stats.channel == 'SHN':
                tr.stats.channel = 'EHN'
                tr.stats.location = '20'
        if tr.stats.channel == 'SHE':
                tr.stats.channel = 'EHE'
                tr.stats.location = '20'
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

###################################################################################

st = read('2014-11-*')
st.merge()

for tr in st:
	st1 = trim_tails(tr)
	print st1
	sc_rename(st1)


