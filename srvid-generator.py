#!/usr/bin/python
# -*- coding utf-8 -*-
import sys
import urllib
import re


__version__ = 'oscam.srvid v0.5'

providers = {
	'viasatua': ('Viasat Ukraina', '4AE1', 'viasatua', 'Astra 4A (4.8E)'),
	'hello': ('Hello HD', '0BAA', 'hello', 'Eutelsat 9A (9E)'),
	'cyfra': ('Cyfra+', '0100', 'cyfra', 'Hot Bird 13C (13E)'),
	'nova': ('Nova', '0604', 'nova', 'Hot Bird 13B/13C (13E)'),
	'skyitalia': ('Sky Italia', '093B', 'skyitalia', 'Hot Bird 13A/13B/13C (13E)'),
	'hdplus': ('HD Plus', '1843', 'hdplus', 'Astra 1KR/1L/1M (19.2E)'),
	'skydeutsch': ('Sky Deutschland', '1702', 'skydeutschland', 'Astra 1KR/1L/1M/2C (19.2E)'),
	'ntv': ('NTV+', '0500', 'ntvplus36', 'Eutelsat 36A/36B (36E)'),
	'tricolor': ('Tricolor TV', '4AE1', 'tricolor', 'Eutelsat 36A/36B (36E)'),
	'ntv_vostok': ('NTV+ Vostok', '0500', 'ntvplusbonum1', 'Bonum 1 (56E)'),
	'tricolor_sibir': ('Tricolor TV Sibir', '4AE1', 'tricolorbonum1', 'Bonum 1 (56E)'),
	'aktiv': ('Aktiv TV', '0B00', 'aktiv', 'Eutelsat 904 (60E)'),
	'raduga': ('Raduga TV', '0652', 'raduga', 'ABS 1 (75E)'),
	'kontinent': ('Kontinent TV', '0602', 'kontinent', 'Horizons 2 (85E)') 
}

class InvalidParamException(Exception):
	def __init__(self, *args, **kwargs):
		print '%s: incorret param' % __version__
		print 'Try: `' + sys.argv[0] + ' -h\' or \''+ sys.argv[0] + ' --help\' for more information.'
		sys.exit()

try:
	provider = sys.argv[1]
except IndexError:
    raise InvalidParamException()

if provider == '-h' or provider == '--help':
	print __version__
	print 'Usage: ' + sys.argv[0] + ' [provider] \n\nProviders:'
	for key, provider in providers.iteritems():
		print '%s - %s' % (key, provider[3])
	sys.exit()

if provider in providers:
	name, caid, url, satellite = providers[provider]
	output = open(provider + '.oscam.srvid', 'w')
else:
    raise InvalidParamException()

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