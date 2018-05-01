create table cr1000_l0 (id serial, time timestamp with time zone, windspeed float, winddirection float, windelevation float, speedofsound float, sonictemperature float, latitude float, longitude float, speed float, course float, magvariation float, fixquality integer, nmbr_sat integer, cncounter float);

create table aethalometer_l0 (id serial, time timestamp with time zone, conc880 float, conc370 float, flow float, sz880 float, sb880 float, rz880 float, rb880 float, fraction880 float, attenuation880 float, sz370 float, sb370 float, rz370 float, rb370 float, fraction370 float, attenuation370 float);