import os
from lib.crwaler import Crawler

BASE_URL = "https://bnr.bg/hristobotev/radioteatre/list?forceFullVersion=1"
# BASE_URL = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=qdz61b&f1=1"

if __name__ == '__main__':
	crawler = Crawler(BASE_URL)
	# crawler.run()
