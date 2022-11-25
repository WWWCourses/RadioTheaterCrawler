import requests
import os

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
			# TODO: check encoding problem
			# r.encoding = 'windows-1251'
			print(r.text)
			return r.text;


	def run(self):
		""" run the crawler for each url in seed
			Use multithreading for each GET request

		"""
		for url in self.seed:
			html = self.get_html(url)
			self.write_to_file('bnr.bg.html', html)


		print('Crowler finish its job!')

if __name__ == '__main__':
	crawler = Crawler("https://bnr.bg/hristobotev/radioteatre/list?forceFullVersion=1")
	crawler.run()
