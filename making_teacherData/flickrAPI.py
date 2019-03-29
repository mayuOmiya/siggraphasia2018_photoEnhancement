#!/usr/bin/env python
# -*- coding: utf-8 -*-
from retry import retry
import requests
import xml.dom.minidom as md
import time
import os
import sys

# set your flickr.API_KEY
API_KEY = ''
API_SECRET = ''

class Flickr(object):
	def __init__(self, api_key):
		self.api_url = 'https://api.flickr.com/services/rest/'
		self.api_key = api_key

	def get_interestingness_photos_id(self, date):

		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.interestingness.getList',
										 'date': date ,
										 'per_page': '5'
										 })  

		# xml -> dom object
		dom = md.parseString(r.text.encode('utf-8'))

		# dom object -> photo_id
		result = []
		for elem in dom.getElementsByTagName('photo'):
			result.append(elem.getAttribute('id'))			
		return result

	@retry(tries=4, delay=5, backoff=2)
	def get_url_from_photo_id(self, photo_id):
		
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.photos.getSizes',
										 'photo_id': photo_id
										 })		

		# xml -> dom object
		dom = md.parseString(r.text.encode('utf-8'))
		
		# dom object -> URL
		result = None
		for elem in dom.getElementsByTagName('size'):
			# chooze size(small,large,...)
			if elem.getAttribute('label') == 'Small':
				result = elem.getAttribute('source')
				# other size
				break
			else:
				pass
		return result

	@retry(tries=4, delay=5, backoff=2)
	def check_tags(self, photo_id):
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.tags.getListPhoto',
										 'photo_id': photo_id
										 })	

		dom = md.parseString(r.text.encode('utf-8'))
		result = False
		for elem in dom.getElementsByTagName('tag'):
			# remove monochrome
			if elem.getAttribute('raw') == 'blackandwhite':
				result = True
			elif elem.getAttribute('raw') == 'black and white':
				result = True
			elif elem.getAttribute('raw') == 'b&w':
				result = True
			elif elem.getAttribute('raw') == 'BW':
				result = True
			elif elem.getAttribute('raw') == 'bw':
				result = True
			elif elem.getAttribute('raw') == 'Black & White':
				result = True
			elif elem.getAttribute('raw') == 'B&W':
				result = True
			elif elem.getAttribute('raw') == 'Mono':
				result = True
			elif elem.getAttribute('raw') == 'monochrome':
				result = True
			else:
				pass
		return result		

@retry(tries=4, delay=5, backoff=2)
def download_image(photo_url, photo_id, photo_date):
	savedir = 'flickr-data/'+photo_date+'/'
	if os.path.exists( 'flickr-data/' ):
		if not os.path.exists( savedir ):
			os.mkdir( savedir )
	else:
		os.mkdir( 'flickr-data' )
		os.mkdir( savedir )

	file_name = savedir+photo_date+'-'+photo_id+'.jpg'
	r = requests.get(photo_url)
	#save file
	if r.status_code == 200:
		f = open(file_name, 'w')
		f.write(r.content)
		f.close()


if __name__ == '__main__':

	api_key = API_KEY

	argvs = sys.argv
	photo_date = argvs[1]
	#photo_date = '2019-01-31'

	all_photos_name = ['']

	f = Flickr(api_key)
	
	id_list = f.get_interestingness_photos_id(photo_date)

	size = len(id_list)
	print(size)
	url_list = ['']*size
	for i in range(size):
		url_list[i] = f.get_url_from_photo_id(id_list[i])
		
	print('url list finished')
	
	for i in range(size):
		if not(f.check_tags(id_list[i])):
			print(id_list[i])
			download_image(url_list[i], id_list[i], photo_date)
			all_photos_name.append(photo_date+'-'+id_list[i])
			time.sleep(0.5)
		else:
			print(id_list[i], 'blackwhite: not saved')

	with open( 'flickr-data/'+photo_date+'/all_file_name.txt', 'w' ) as file:
		for f in all_photos_name:
			file.write( f+'\n')