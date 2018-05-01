#!/usr/bin/python

import fileinput
import re
import datetime
import psycopg2 as pg
import pytz


UTC = pytz.utc

db = 'sanae54'
dbuser = 'steve'
dbpass = 'frub*jub'
conn = pg.connect(database=db, user=dbuser, password=dbpass)
cur = conn.cursor()
cur.execute("set timezone to utc")
conn.commit()


# we want to get cr1000/rmyoung81000/CPC data (half hertz)
# and insert it into a postgis database. 

# data looks like:
#"TIMESTAMP","RECORD","windspeed","winddirection","windelevation","speedofsound","sonictemperature","latitude_a","latitude_b","longitude_a","longitude_b","speed","course","magnetic_var","fix_quality","nmbr_satellites","CPC"
#"TS","RN","m/s","degrees","degrees","m/s","celcius","degrees","minutes","degrees","minutes","m/s","degrees","unitless","unitless","unitless","unitless"
#  "2013-09-18 10:24:24",554908,5.4,44.1,-8.2,332.76,1.62,-40,-19.2844,-9,-53.2637,0.4,89.9,-22.5,2,10,"NAN"
#  "2013-09-18 10:24:26",554909,5.32,18.6,-3.3,332.8,1.69,-40,-19.2845,-9,-53.264,0.5,89.9,-22.5,2,10,2242.519

p = re.compile(r"""^"
                   (?P<year>\d{4})-
                   (?P<month>\d{2})-
                   (?P<day>\d{2})\s
                   (?P<hour>\d{2}):
                   (?P<minute>\d{2}):
                   (?P<second>\d{2})",
                   \d{4,8},
                   (?P<windspeed>\d{1,2}[.]\d{1,2}),
                   (?P<winddirection>\d{1,3}[.]?\d{0,1}),
                   (?P<windelevation>-?\d{1,2}[.]?\d{0,2}),
                   (?P<speedofsound>\d{3}[.]\d{1,2}),
                   (?P<sonictemperature>-?\d{1,2}[.]\d{1,2}),
		   (?P<latitudeA>-?\d{1,2}),
		   (?P<latitudeB>-?\d{1,3}[.]?\d{2,4}),
		   (?P<longitudeA>-?\d{1,3}),
		   (?P<longitudeB>-?\d{1,3}[.]?\d{2,4}),
		   (?P<speed>\d{1,2}[.]?\d{0,1}),
		   (?P<course>\d{1,3}[.]?\d{0,2}),
		   (?P<magvar>-?\d{0,2}[.]?\d{0,2}),
		   (?P<fixquality>\d),
		   (?P<numsats>\d{1,2}),
		   (?P<CPC>-?\d{1,4}[.]?\d{2,5}|"NAN")
                   .*
                   """, re.VERBOSE)

for line in fileinput.input():

        m = p.match(line)

        if m:
                try:
                        day=int(m.group('day'))
                        month=int(m.group('month'))
                        year=int(m.group('year'))
                        hour=int(m.group('hour'))
                        minute=int(m.group('minute'))
                        second=int(m.group('second'))
			time = datetime.datetime(year,month,day,hour,minute,second,tzinfo=UTC)

                        windspeed=float(m.group('windspeed'))
                        winddirection=float(m.group('winddirection'))
                        windelevation=float(m.group('windelevation'))
			speedofsound=float(m.group('speedofsound'))
			sonictemperature=float(m.group('sonictemperature'))
			latitudeA=float(m.group('latitudeA'))
			latitudeB=float(m.group('latitudeB'))
			latitude= latitudeA + latitudeB/60.0
			longitudeA=float(m.group('longitudeA'))
			longitudeB=float(m.group('longitudeB'))
			longitude = longitudeA + longitudeB/60.0
			speed = float(m.group('speed'))
			course = float(m.group('course'))
			magvar = float(m.group('magvar'))
			fixquality = int(m.group('fixquality'))
			numsats = int(m.group('numsats'))
			if (m.group('CPC') == '"NAN"'):
				CPC = 9999.9
			else:
				CPC = float(m.group('CPC'))



                except (ValueError):
			print "ValueError!"
                        continue
	
		#print "%d %d %d %f %f %f %f" % (hour, minute, second, latitude, longitude, windspeed, windelevation)

		sql = "insert into cr1000 (time, windspeed, winddirection, windelevation, speedofsound, sonictemperature, latitude, longitude, speed, magvariation, fixquality, nmbr_sat, cncounter, course) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
		data = (time, windspeed, winddirection, windelevation, speedofsound, sonictemperature, latitude, longitude, speed, magvar, fixquality, numsats, CPC, course)

		print "inserting data %s %s" % (time.isoformat(), CPC)
		cur.execute(sql, data)

conn.commit()

conn.close()
