import requests
import os
from bs4 import BeautifulSoup
import re


BASE_URL = "https://bnr.bg"


try:
	# when run 'crawler.py':
	from constants import DATA_PATH
except:
	# when run 'app.py'
	from lib.constants import DATA_PATH



class Crawler():
	def __init__(self):
		self.current_page = 1
		self.url = "https://hristobotev/radioteatre/list?forceFullVersion=1&page_1_1="
		self.seed = []


	def write_to_file(self,filename, content):
		""" Write string to given filename
				:param filename: string
				:param content: sring
		"""

		with open(DATA_PATH+filename, 'w') as f:
			f.write(content)

	def get_html(self, url):
		""" Make GET request and save content to file
			First try with SSL verification (default),
			if error => disable SSL verification

			:param url: string
		"""
		# GET request without SSL verification:
		try:
			r = requests.get(url)
		except requests.RequestException:
			# try with SSL verification disabled.
			# this is just a dirty workaraound
			# check https://levelup.gitconnected.com/solve-the-dreadful-certificate-issues-in-python-requests-module-2020d922c72f
			r = requests.get(url,verify=False)
		except Exception as e:
			print(f'Can not get url: {url}: {str(e)}!')
			exit(-1)

		# set content encoding explicitely
		r.encoding="utf-8"

		if r.ok:
			return r.text
		else:
			print('The server did not return success response. Bye...')
			exit

	def get_seed(self):
		page_links = []
		page_url = self.url + str(self.current_page)
		print(page_url)
		html = self.get_html(page_url)

		soup = BeautifulSoup(html,'html.parser')
		module_1_1 = soup.find(id='module_1_1')
		divs = module_1_1.find_all('div',class_="row-fluid")

		for div in divs:
			date = div.find('div', class_="date")

			# check if date is in last days
			a = div.find('a')

			page_links.append( urljoin(BASE_URL,a['href']))

		if page_links:
			self.seed = [ *self.seed, *page_links]
			self.current_page+=1
			self.get_seed()


	def get_page_data(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		module_1_2 = soup.find('div', id = 'module_1_2')

		title = module_1_2.find('h1').getText(strip=True)
		pub_date = module_1_2.find('span', itemprop="datePublished")
		article = module_1_2.find('span', itemprop="articleBody")

		return {
			'title':title,
			'pub_date':pub_date,
			'article':article
		}



	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""
		### get seed (get pages for radiotheater publiched in last 10 days)

		# self.get_seed()
		# print(self.seed)

		### process page data
		for url in [1]:
			page_html = self.get_html('https://bnr.bg/hristobotev/post/101610367')

			data = self.get_page_data(page_html)
			print(data)

			# write data to db


		print('Crowler finish its job!')

