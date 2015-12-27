# conky-weather
Show Yahoo Weather info on conky

##Preview
![Conky-weather](https://github.com/edusig/conky-weather/blob/master/conky-weather.png)

##Usage
Find your location code [here](http://woeid.rosselliot.co.nz/). Or just search for your "Yahoo weather woeid".

Change your conky configuration file (usually at `/home/<username>/.config/conky/conky.conf`) and add the weather script and the weather condition .gif

```
${exec python2 /path/to/script/weather.py <location> <cache_time> <use_celsius>}
${image /path/to/script/condition_<location>.git -s 52x52, -p <posx>,<posy>}
```

Where:
- `<location>` is your location code (woeid).
- `<cache_time>` is the time in seconds before expiring the weather information and getting a new one from yahoo weather api.
- `<use_celsius>` when 1 will show temperature as celsius and when 0 in fahrenheit.
- `<posx>` image x position.
- `<posy>` image y position.

To avoid lots of requisition to yahoo api a cache file named `cache_<location>.txt` is created in the first run. The default cache time is 1800s or 30 minutes.

###Optional
Optionally you can change the default values for location, cache time and user_celsius at the top of the [weather.py](https://github.com/edusig/conky-weather/blob/master/weather.py) script.
