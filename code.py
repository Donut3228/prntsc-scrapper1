import urllib.request
from io import BytesIO
from PIL import Image
from html.parser import HTMLParser
import random
from pathlib import Path, PosixPath, PurePath
import os
import sys
from datetime import datetime
import asyncio
import re
import threading

startTime = datetime.now()

# generating random link for request(long) or file name(short)
def randomLink(x):
	random_seq = []

	for i in range(97,123):
		random_seq.append(chr(i))

	for i in range(0,10):
		random_seq.append(str(i))
	parce_link = []

	for i in range(random.choice([5,6])):
		parce_link.append(random.choice(random_seq))

	str_link = ''

	for each in parce_link:
		str_link += str(each)
	if x == 'long':
		return 'https://prnt.sc/' + str_link
	elif x == 'short':
		return str_link

# returns readed page file
def readPage(link):
	return urllib.request.urlopen(urllib.request.Request(
		link,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)).read()


# return image link after parsing html
def getImgLink(htmlObj):
	data = []

	class MyHTMLParser(HTMLParser):
		def handle_starttag(self, tag, attrs):
			#print("Encountered a start tag:", tag)
			#print("Data:", attrs)
			for each in attrs:
				match = re.compile(r"^https.*png").match(str(each[1]))
				if match is not None:
					data.append(each[1])

	parser = MyHTMLParser()
	parser.feed(htmlObj)

	return data[-1]


# getting picture from random link and saving it to folder
def getPic():
	link_for_req = randomLink('long')
	print(link_for_req)

	htmlForParse = str(readPage(link_for_req))

	try:
		img_link = getImgLink(htmlForParse)
		img_page = readPage(img_link)
		img = Image.open(BytesIO(img_page))
		img.save(Path().resolve().joinpath('images').joinpath(randomLink('short') + '.png'))
		return(True)
	except:
		return(False)


def getPictures(amount):
	count_success = 0
	count_failed = 0

	while(count_success < amount):
		if(getPic()):
			count_success += 1
			print(count_success, '/', amount)
		else:
			count_failed += 1

	return print('Successfully downloaded: ', count_success)

getPictures(int(sys.argv[1]))

print(datetime.now() - startTime)


