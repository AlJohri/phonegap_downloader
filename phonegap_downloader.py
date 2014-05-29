#!/usr/bin/env python3

import requests
import lxml.html

from urllib.error import HTTPError
from urllib.request import urlretrieve
from urllib.parse import urlparse, parse_qs
	
for i in range(31):
	if i == 1: response = requests.get('http://phonegap.com/app/android/')
	else: response = requests.get('http://phonegap.com/app/android/page%i/' % i)
	doc = lxml.html.fromstring(response.text)
	apps = doc.cssselect('.app-list')
	if not apps: continue
	apps = apps[0]
	for app in apps.cssselect('a'):
		response2 = requests.get('http://phonegap.com' + app.get('href'))
		doc2 = lxml.html.fromstring(response2.text)
		android_store_link = doc2.cssselect('.store-links .android')
		if not android_store_link: continue
		android_store_link = android_store_link[0]
		url = android_store_link.get('href')
		if not url: continue
		if url.find('play.google.com') == -1: continue
		app_name = parse_qs(urlparse(url).query).get('id')
		if not app_name: continue
		app_name = app_name[0]
		print(app_name.ljust(50), app.text_content().strip())
		dl_url = 'http://apk-dl.com/store/apps/details?id=%s' % app_name
		print("Downloading %s ..." % dl_url)
		try:
			a, b = urlretrieve(dl_url, app_name + ".apk")
			if b.get_content_type() == 'text/html':
				raise Exception("Download limit reached")
		except HTTPError:
			print("Error downloading %s" % app_name)
			continue
