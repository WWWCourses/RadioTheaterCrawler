import os
import re
import requests
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin



BASE_URL = "https://bnr.bg"


try:
	# when run 'crawler.py':
	from constants import DATA_PATH
	from db import DB
except:
	# when run 'app.py'
	from lib.constants import DATA_PATH
	from lib.db import DB



class Crawler():
	def __init__(self):
		self.current_page = 1

		# starting url, to which self.current_page wil be appended
		self.url = "https://bnr.bg/hristobotev/knowledge/list?page_1_1="

		# list of urls to be scraped
		self.seed = []

		# indicates that crwler is not finished it's job. We'll set it to 1 after sucessfull crawl.
		self.status = 0

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

	def get_pub_date(self,date_string):
		date_rx = re.compile(r'(\d{2}\.\d{2}\.\d{2})')


		# extract date from date_string
		m = date_rx.search(date_string)
		if m:
			pub_date = m[1]
			pub_date = datetime.datetime.strptime(pub_date, '%d.%m.%y')

			return pub_date
		else:
			return datetime.datetime.strptime('30.01.1990', '%d.%m.%y')

	def get_seed(self):
		page_links = []

		page_url = self.url + str(self.current_page)
		html = self.get_html(page_url)

		soup = BeautifulSoup(html,'html.parser')
		module_1_1 = soup.find(id='module_1_1')
		divs = module_1_1.find_all('div',class_="row-fluid")

		for div in divs:
			date_string = div.find('div', class_="date").getText()

			###  check if date is in last days
			pub_date = self.get_pub_date(date_string)

			now = datetime.datetime.now()
			date_diff = relativedelta(now, pub_date)

			if date_diff.days<10:
				a = div.find('a')
				page_links.append( urljoin(BASE_URL,a['href']))

		if page_links:
			self.seed = [ *self.seed, *page_links]
			self.current_page+=1
			self.get_seed()

	def get_page_data(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		module_1_2 = soup.find('div', id = 'module_1_2')

		# get title:
		title = module_1_2.find('h1').getText(strip=True)

		# get publication date as MySQL formated string:
		pub_date_span = module_1_2.find('span', itemprop="datePublished")
		pub_date = self.get_pub_date(pub_date_span.getText())
		pub_date_str = pub_date.strftime('%Y-%m-%d')

		# get article text:
		article = module_1_2.find('span', itemprop="articleBody").getText()

		return {
			'title':title,
			'pub_date':pub_date_str,
			'article':article
		}


	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""
		db = DB()
		# db.truncate_radiotheaters_table()

		### get seed (get pages for radiotheater publiched in last 10 days)
		self.get_seed()

		### process page data
		for url in self.seed:
			print(f'Process page: {url}')
			page_html = self.get_html(url)

			data = self.get_page_data(page_html)

			###  write data to db
			db.insert_row( tuple(data.values()) )

		self.status = 1
		print('Crowler finish its job!')


if __name__ == "__main__":
	crawler = Crawler()
	crawler.run()

