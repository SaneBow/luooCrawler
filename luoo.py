import requests
import urlparse
import hashlib
import time
from datetime import datetime
import json
import sys
import argparse

def crawl(page, limit=5, sort='fav', echo=False, iterm2img=False):
	secret = 'HV9DNPrchIgcLuoo'
	timestamp = str(int(time.time()))
	nonce = 'yfDZvTvIASmDqTjapikMbCFwKlUPVKYN'

	url = 'https://api.luoo.net/v1/vols?filter=all&sort={}&type=0&limit={}&after={}'.format(sort, limit, page)
	queries = dict(urlparse.parse_qsl(urlparse.urlparse(url).query))
	data = {}
	queries = sorted(queries.items())
	data = sorted(data.items())
	s = ''.join([q[0]+'='+q[1]+'&' for q in queries])
	s += ''.join([d[0]+'='+d[1]+'&' for d in data])
	s += timestamp+'&'+nonce+'&'+secret
	# print s
	signature = hashlib.sha1(s).hexdigest()
	# print 'Signature:', signature

	headers = {'Timestamp': timestamp, 'Nonce': nonce, 'Signature': signature}

	r = requests.get(url, headers=headers, timeout=15)
	content = json.loads(r.content)
	if not 'pager' in content:
		print content
		raise Exception("API response error: "+str(content))
	vols = content['data']
	results = []
	for vol in vols:
		info = {}
		info['link'] = 'http://www.luoo.net/vol/index/%d' % vol['vol_id']
		info['title'] = vol['title']
		info['tags'] = ', '.join([tag['name'] for tag in vol['tags']])
		info['date'] = datetime.fromtimestamp(int(vol['create_time'])).strftime("%Y-%m-%d")
		info['favs'] = vol['favs_count']
		info['comments'] = vol['comments_count']
		info['cover'] = vol['covers']['large']
		results.append(info)
		# display cover image in iterm2
		if iterm2img:
			import iterm2_tools
			img = requests.get(info['cover'], stream=True, timeout=15).content
			print iterm2_tools.images.display_image_bytes(img)
		if echo:
			print info['title'], info['link']
			print 'tags:', info['tags']
			print 'date:', info['date']
			print 'favs:', info['favs'], 'comments:', info['comments']
			print
	return results

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Luoo.net crawler, with support of sorting.')
	parser.add_argument('page', metavar='N', type=int, nargs='?', default=0,
	                    help='page number (default: 0)')
	parser.add_argument('-l', dest='limit', type=int, default=5,
	                    help='vols each page (default: 5)')
	parser.add_argument('-s', dest='sort', choices=['fav', 'new', 'comment'], default='fav',
	                    help='sort by (default: fav)')
	args = parser.parse_args()
	crawl(args.page, limit=args.limit, sort=args.sort, echo=True, iterm2img=True)