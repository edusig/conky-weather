# -*- coding: utf-8 -*-
"""
Returns formatted weather from yahoo data api
"""

__author__ = 'Eduardo Ciciliato'
__email__ = 'eduardo.ciciliato@gmail.com'
__license__ = 'GPL 2.0'
__version__ = '1.0.0'

import urllib2
import urllib
import json
import sys
import os

from datetime import datetime
from shutil import copyfile

PATH_BASE = os.path.dirname(os.path.realpath(__file__))

#Config defaults
DEFAULT_LOCATION = None # Choose a default location
DEFAULT_UNIT_CELSIUS = True
CACHE_TIME = 1800 # In seconds (1800 = 30 minutes)


def format_data(data, woeid, use_celsius):
    """"
    Returns a formatted title, weather condition and gif path
    """
    if use_celsius:
        unit = 'C'
    else:
        unit = 'F'
    title = 'Weather for ' + data['location']['city'] + " - " + data['location']['region']
    condition = data['item']['condition']
    cond = ' Temp: ' + condition['temp'] + unit + ' \n ' + condition['text']
    image = 'gif/' + condition['code'] + '.gif'
    # Copy one of the condition gif images to the base path of the script to be used by conky
    copyfile(os.path.join(PATH_BASE, image), os.path.join(PATH_BASE, 'condition_'+woeid+'.gif'))
    return title, cond, image


def weather(woeid, cache_time, use_celsius):
    """
    Call yahoo api for weather data if no cache is available,
    then returns the formatted data
    """
    celsius_arg = ''
    intcelsius = 0
    if use_celsius:
        intcelsius = 1
        celsius_arg = " and u='c'"
    # Look for a cache file for your location and temperature type
    if os.path.isfile(os.path.join(PATH_BASE, 'cache_'+woeid+'_'+str(intcelsius)+'.txt')):
        with open(os.path.join(PATH_BASE, 'cache_'+woeid+'_'+str(intcelsius)+'.txt'), 'r') as cfile:
            date, read_title, cond1, cond2 = cfile.read().splitlines()
            now = datetime.utcnow()
            fdate = datetime.strptime(date[:19], '%Y-%m-%d %H:%M:%S')
            tdelta = now - fdate
            if tdelta.seconds < cache_time:
                return read_title, cond1 + '\n' + cond2

    # If there is no cache file or it expired, get from yahoo
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    # The temperature unit is set to celsius using "u='c'" in the query
    yql_query = "select * from weather.forecast where woeid="+woeid+celsius_arg
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    ftitle, fcond, fimage = format_data(data['query']['results']['channel'], woeid, use_celsius)

    # Saves a new cache file for your location
    with open(os.path.join(PATH_BASE, 'cache_'+woeid+'_'+str(intcelsius)+'.txt'), 'w+') as cfile:
        cfile.write(str(datetime.utcnow())[:19]+'\n')
        cfile.write(ftitle+'\n')
        cfile.write(fcond+'\n')
        cfile.write(fimage+'\n')
    return ftitle, fcond

def main():
    """
    Main function for showing the weather
    """
    location = None
    if DEFAULT_LOCATION is not None:
        location = str(DEFAULT_LOCATION)

    cache = int(CACHE_TIME)
    celsius = DEFAULT_UNIT_CELSIUS

    if len(sys.argv) > 1:
        location = sys.argv[1]
    if len(sys.argv) > 2:
        cache = int(sys.argv[2])
    if len(sys.argv) > 3:
        celsius = int(sys.argv[3])
        if celsius == 1:
            celsius = True
        else:
            celsius = False

    if location is None:
        raise Exception('No location was provided. Pass it as the first argument ' \
                        'or edit the default location at line 13')

    weather_title, weather_cond = weather(location, cache, celsius)
    print weather_title
    conds = weather_cond.split('\n')
    print
    for cond in conds:
        print '\t  '+cond
    # Remove this if you want
    print
    print 'powered by yahoo weather api'

if __name__ == '__main__':
    main()
