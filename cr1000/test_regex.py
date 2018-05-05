#!/usr/bin/env python3

# this will test that what we get back from the database is the same as what we put in

import psycopg2 as pg
import pytz
import re
import datetime

UTC = pytz.utc

db = 'sanae54test'
dbuser = 'steve'
dbpass = 'frub*jub'
dbhost = 'localhost'
dbport = '5432'
conn = pg.connect(database=db, user=dbuser, password=dbpass, host=dbhost, port=dbport)
cur = conn.cursor()
cur.execute('set timezone to utc')
conn.commit()

results = ({'id': 1,\
	    'time': datetime.datetime(2015,1,19,28,46,tzinfo=UTC),\
	    'windspeed': 2.02\
	    'winddirection': 47.8\
	    'windelevation'

# we prefer not to say "select * from cr1000" because then we're not sure of the order
# that we're going to get our data back in, so we specify, which is tedious but better:
select = 'select id,time,windspeed,winddirection,windelevation,speedofsound,sonictemperature,\
		latitude,longitude,speed,course,magvariation,fixquality,nmbr_sat,\
		cncounter from cr1000_l0'

cur.execute(select)

# this should get us the first line of the table
line = cur.fetchone()
assert type(line[0]) == int  # record number 
#assert line[0] == 1  # assigned by postgres, we don't know what it's value should be so it's commented out
assert line[1] == datetime.datetime(2015,1,1,9,28,46,tzinfo=UTC) # timestamp, we don't need the
# assertion, because if we compare a datetime to something that isn't a datetime we will raise an
# AssertionError in any case
assert type(line[2]) == float  # windspeed 
assert line[2] == 2.02
assert type(line[3]) == float  # winddirection
assert line[3] == 47.8
assert type(line[4]) == float  # windelevation
assert line[4] == 33.5
assert type(line[5]) == float  # speedofsound
assert line[5] == 341.64
assert type(line[6]) == float  # sonictemperature
assert line[6] == 16.48
assert type(line[7]) == float  # latitude 
assert line[7] == -41.2212066666667
assert type(line[8]) == float  # longitude 
assert line[8] == 9.59630666666667
assert type(line[9]) == float  # speed 
assert line[9] == 2.9
assert type(line[10]) == float  # speed 
assert line[10] == 2.9



conn.close()
