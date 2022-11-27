import requests
import os
from bs4 import BeautifulSoup
import re


try:
	# when run 'crawler.py':
	from constants import DATA_PATH
except:
	# when run 'app.py'
	from lib.constants import DATA_PATH



class Crawler():
	def __init__(self, base_url):
		self.seed = [base_url]

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
		r = requests.get(url)

		# print(f'#####: {r.apparent_encoding}')

		if r.ok:
			return r.text;

	def scrape_links(self, html):
		links = list()

		soup = BeautifulSoup(html,'html.parser')
		module_1_1 = soup.find(id='module_1_1')
		divs = module_1_1.find_all('div',class_="row-fluid")
		for div in divs:
			date = div.find('div', class_="date")
			# print(date.text)
			a = div.find('a')
			# print(a['href'])
			links.append(a['href'])

		return links

	def get_page_data(self, urls):
		print(urls)

	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""
		for url in self.seed:
			html = self.get_html(url)
			# self.write_to_file('bnr.bg.html', html)
			links = self.scrape_links(html)
			main_url = 'https://bnr.bg/'
			urls = [ main_url+el  for el in links]
			print(urls)


		print('Crowler finish its job!')

