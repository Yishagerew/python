#! /usr/bin/python

import pycurl
import StringIO
import re
import sys
import urlparse
from StringIO import StringIO

def get_links(text):

	href = re.compile(r'''href\s*=\s*["']([^"']+)["']''')
	protocol = re.compile(r'''[a-zA-Z]+:''')
	urls=[]
	for n in href.findall(text):
		if not protocol.match(n):
			continue
		p=n.find('#')
		if p>0:
			n=n[:p]
		if len(n)==0:
			continue
		if n in urls:
			continue
		urls.append(n)
	return urls
	
buffer = StringIO()
def download(url):
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, buffer.write)
	c.perform()
	c.close()
	return buffer.getvalue()
	# Body is a string in some encoding.
	# In Python 2, we can print it without knowing what the encoding is.

url = sys.argv[1]
text = download(url)
urls = get_links(text)

p = urlparse.urlparse(url)
base ='%s://%s' % (p.scheme, p.netloc)

for url in urls:
	print base + url


