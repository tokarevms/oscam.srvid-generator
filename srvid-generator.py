#!/usr/bin/python
# -*- coding utf-8 -*-
import sys, urllib, re

try:
	provider = sys.argv[1]
except:
	print 'oscam.srvid v0.3: no param specified \
	\nUsage: `' + sys.argv[0] + ' (viasatua | hello | cyfra | nova | skyitalia | skydeutsch | ntv | ntv_vostok | tricolor | tricolor_sibir | aktiv | raduga | kontinent)`'
	sys.exit()

if provider == 'viasatua':
	name = 'Viasat Ukraina'; caid = '4AE1'; url = 'viasatua'; satellite = 'Astra 4A (4.8E)'
elif provider == 'hello':
	name = 'Hello HD'; caid = '0BAA'; url = 'hello'; satellite = 'Eutelsat 9A (9E)'
elif provider == 'cyfra':
	name = 'Cyfra+'; caid = '0100'; url = 'cyfra'; satellite = 'Hot Bird 13C (13E)'
elif provider == 'nova':
	name = 'Nova'; caid = '0604'; url = 'nova'; satellite = 'Hot Bird 13B/13C (13E)'
elif provider == 'skyitalia':
	name = 'Sky Italia'; caid = '093B'; url = 'skyitalia'; satellite = 'Hot Bird 13A/13B/13C (13E)'
elif provider == 'skydeutsch':
	name = 'Sky Deutschland'; caid = '1702'; url = 'skydeutschland'; satellite = 'Astra 1KR/1L/1M/2C (19.2E)'
elif provider == 'ntv':
	name = 'NTV+'; caid = '0500'; url = 'ntvplus36'; satellite = 'Eutelsat 36A/36B (36E)'
elif provider == 'tricolor':
	name = 'Tricolor TV'; caid = '4AE1'; url = 'tricolor'; satellite = 'Eutelsat 36A/36B (36E)'
elif provider == 'ntv_vostok':
	name = 'NTV+ Vostok'; caid = '0500'; url = 'ntvplusbonum1'; satellite = 'Bonum 1 (56E)'
elif provider == 'tricolor_sibir':
	name = 'Tricolor TV Sibir'; caid = '4AE1'; url = 'tricolorbonum1'; satellite = 'Bonum 1 (56E)'
elif provider == 'aktiv':
	name = 'Aktiv TV'; caid = '0B00'; url = 'aktiv'; satellite = 'Eutelsat 904 (60E)'
elif provider == 'raduga':
	name = 'Raduga TV'; caid = '0652'; url = 'raduga'; satellite = 'ABS 1 (75E)'
elif provider == 'kontinent':
	name = 'Kontinent TV'; caid = '0602'; url = 'kontinent'; satellite = 'Horizons 2 (85E)' 
else:
	print 'oscam.srvid v0.3: wrong param \
	\nUsage: `' + sys.argv[0] + ' (viasatua | hello | cyfra | nova | skyitalia | skydeutsch | ntv | ntv_vostok | tricolor | tricolor_sibir | aktiv | raduga | kontinent)`' 
	sys.exit()

output = open(provider + '.oscam.srvid', 'w')

if url:
	url = 'http://www.lyngsat.com/packages/' + url + '_sid.html'
	html = urllib.urlopen(url).read();
	head = html.find('>SID<'); footer = html.find('>SID<', head + 10)
	html = html[head:footer]

	if html:
		p1 = re.compile(r'(?:<font size[^>]+><b>|<b><a[^>]+>)([\w\d\s\.+-=\$\%\'\"\(\)\[\]\&\!\@\*]+)(?:</a>)?</b>', re.M | re.U)
		p2 = re.compile(r'><b>([\d\s]+)</b></td>', re.M)
		channels = p1.findall(html)
		sids = p2.findall(html)

		if sids and channels:
			for sid, channel in zip(sids, channels):
				output.write("%s:%04X|%s|%s|%s\n" % (caid, int(sid), name, channel, satellite))