#!/usr/bin/env python

from geopy.geocoders import Nominatim
from tzwhere import tzwhere
from pytz import timezone
import pytz
from countries_list import countries

import random
from datetime import datetime

def logg(text,symbol='^'):
	print "%s\n %s\n %s"%(symbol*10,text,symbol*10)

def time_converter_best(location='india'):
	location = location.lower()
	tz_string = ''
	random.shuffle(countries)

	for item in countries:
		temp_arr = [i.lower() for i in item.values() if type(i) != list]
		temp_arr.append(item['timezones'][0].lower())

		for i in temp_arr:
			if location == i:
				tz_string = item['timezones'][0]
				return get_local_time(tz_string)

			try:
				if location in i:
					tz_string = item['timezones'][0]
					break
			except UnicodeDecodeError:
				pass

	for i in pytz.all_timezones:
		if location in i.lower():
			tz_string = i
			break

	if not tz_string:
		return "cannot find timezone"

	return get_local_time(tz_string)
	 

def time_convertor(location_string='clay street san francisco'):
	lat_c,long_c = get_coordinates(location_string)
	tz_string = get_timezone_string(lat_c,long_c)
	logg(tz_string)
	return get_local_time(tz_string)
def time_convertor_fast(location_string='rohini sector 16'):
	country_name = get_coordinates(location_string,return_country=True)
	logg(country_name,symbol='**')
	tz_string = get_timezone_string_fast(country_name)
	logg(country_name,symbol='**')
	return get_local_time(tz_string)
def get_coordinates(location_string='clay street san francisco',return_country=False):
	geolocator = Nominatim()
	location = geolocator.geocode(location_string)
	if return_country:
		return location.address.split(',')[-1]

	if location:
		print location.address
		print (location.latitude, location.longitude)
		return (location.latitude, location.longitude)
	else:
		print "Location not found"
		return None
def get_timezone_string_fast(country='India'):
	for item in countries:
		if country.lower() in item.values():
			return item['timezones'][0]
def get_timezone_string(lat_c=35.29,long_c=-89.66):
	tz = tzwhere.tzwhere()
	tz_string = tz.tzNameAt(lat_c,long_c)
	print tz_string
	if tz_string:
		return tz_string
	else:
		print "TIMEZONE NOT FOUND"
		return tz_string

def get_local_time(tz_string='Asia/Calcutta'):
	#fmt = '%Y-%m-%d %H:%M:%S %Z%z'
	fmt = '%H:%M %p ,%A %d %b'
	tz_object = timezone(tz_string)
	date_string = datetime.now(tz_object).strftime(fmt)
	return "its %s in timezone %s"%(date_string,tz_string)


if __name__ == '__main__':
	print time_converter_best()

