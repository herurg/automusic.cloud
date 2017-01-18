# -*- coding: utf-8 -*-
import urllib, urllib2, json, os
query_args = { 'Authorization':'AQAAAAAS71gtAAP8G0w0rf1-b0gQhihSqHUHwPE' }
ondevice = os.listdir('/home/pi/music')
oncloud = []

url = 'https://cloud-api.yandex.net:443/v1/disk/resources?path=disk%3A%2Fmusic'
request = urllib2.Request(url, None, query_args)
paths = {}
response = urllib2.urlopen(request)
html = json.loads(response.read())
for item in html['_embedded']['items']:
	paths.update({item['name']: item['path']})
	oncloud.append(item['name'])
upgrade = []
for item in oncloud:
	if unicode(item).encode('utf8') in ondevice:
		pass
	else:
		upgrade.append(item)

delete = []
oncloudconvert= []
for item in oncloud:
	oncloudconvert.append(unicode(item).encode('utf8'))
for item in ondevice:
	if item in oncloudconvert:
		pass
	else:
		delete.append(item)

if len(upgrade)>0:
	apiurl = 'https://cloud-api.yandex.net:443/v1/disk/resources/download?path='	
	for key in upgrade:
		downloadurl = unicode(apiurl+paths[key]).encode('utf8')
		request = urllib2.Request(downloadurl, None, query_args)
		response = urllib2.urlopen(request)
		f = open("/home/pi/music/"+key, "wb")
		request = urllib2.Request(json.loads(response.read())['href'],None,query_args)
		f.write(urllib2.urlopen(request).read())		

if len(delete)>0:
	for item in delete:
		os.remove('/home/pi/music/'+item)
