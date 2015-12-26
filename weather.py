import urllib2, urllib, json, sys, os
from datetime import datetime, timedelta
from shutil import copyfile
base = os.path.dirname(os.path.realpath(__file__))

#Config defaults
DEFAULT_LOCATION = 'XXXXXX' # Choose a default location
DEFAULT_UNIT_CELSIUS = True
CACHE_TIME = 1800 # In seconds (1800 = 30 minutes)


def extract_data(data, woeid):
	title = 'Weather for ' + data['location']['city'] + " - " + data['location']['region']
	condition = data['item']['condition']
	cond = ' Temp: ' + condition['temp'] + 'C \n ' + condition['text']
	image = 'gif/' + condition['code'] + '.gif'
	# Copy one of the condition gif images to the base path of the script to be used by conky
	copyfile(os.path.join(base, image), os.path.join(base, 'condition_'+woeid+'.gif'))
	return title, cond, image


def weather(woeid, use_celsius):

	# Look for a cache file for your location
	if os.path.isfile(os.path.join(base ,'cache_'+woeid+'.txt')):
		with open(os.path.join(base, 'cache_'+woeid+'.txt'), 'r') as f:
			date, title, cond1, cond2, image = f.read().splitlines()
			now = datetime.utcnow()
			fdate = datetime.strptime(date[:19], '%Y-%m-%d %H:%M:%S')
			tdelta = now - fdate
			if tdelta.seconds < CACHE_TIME:
				return title, cond1 + '\n' + cond2, image

	# If there is no cache file or it expired, get from yahoo
	baseurl = "https://query.yahooapis.com/v1/public/yql?"
	# The temperature unit is set to celsius using "u='c'" in the query
	celsius = ''
	if use_celsius:
		celsius = " and u='c'"
	yql_query = "select * from weather.forecast where woeid="+woeid+celsius
	yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
	result = urllib2.urlopen(yql_url).read()
	data = json.loads(result)
	formated = extract_data(data['query']['results']['channel'], woeid)
	
	# Saves a new cache file for your location
	with open(os.path.join(base, 'cache_'+woeid+'.txt'), 'w+') as f:
		f.write(str(datetime.utcnow())[:19]+'\n')
		f.write(formated[0]+'\n')
		f.write(formated[1]+'\n')
		f.write(formated[2]+'\n')
	return formated


if __name__ == '__main__':
	location = str(DEFAULT_LOCATION)
	celsius = DEFAULT_UNIT_CELSIUS

	if len(sys.argv) > 1:
		location = sys.argv[1]
	if len(sys.argv) > 2:
		celsius = sys.argv[2]

	title, cond, image = weather(location, celsius)
	print(title)
	conds = cond.split('\n')
	print
	for c in conds:
		print('\t  '+c)
	# Remove this if you want
	print
	print('powered by yahoo weather api')
