from apscheduler.scheduler import Scheduler
from lxml import html
import requests
import json
import os
import urllib2
import time

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def timed_job():
	# Load campaigns json file
	j = urllib2.urlopen('https://s3-eu-west-1.amazonaws.com/wiggysweb/campaigns.json')
	data = json.load(j)

	# Create new campaigns list
	data_update = []

	# Timestamp
	ts = int(time.time())

	# Iterate through campaigns
	for list in data:
		if 'url' in list:
			thisDict = {}

			# Fetch data from url
			page = requests.get(list['url'])
			tree = html.fromstring(page.text)

			# Parse tree
			thisDict['campaignName'] = str(tree.xpath('//h1/text()')[0])
			amountTargetFull = tree.xpath('//span[@class="currency"]/span/text()')
			thisDict['amountTarget'] = str(amountTargetFull[0][1:]).replace(',', '')
			thisDict['currency'] = amountTargetFull[0][0:1]
			amountRaisedFull = tree.xpath('//div[@class="i-balance"]/span/span/text()')
			thisDict['amountRaised'] = str(amountRaisedFull[0][1:]).replace(',', '')
			thisDict['url'] = list['url']
			thisDict['updated'] = ts

			data_update.append(thisDict)

	# AWS lib
	import boto
	import boto.s3.connection
	s3 = boto.connect_s3()
	AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
	AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
	
	conn = boto.connect_s3(
		aws_access_key_id = AWS_ACCESS_KEY,
		aws_secret_access_key = AWS_SECRET_KEY,
		host = 's3-eu-west-1.amazonaws.com',
		#is_secure=False,               # uncommmnt if you are not using ssl
		calling_format = boto.s3.connection.OrdinaryCallingFormat(),
		)

	bucket = conn.get_bucket('wiggysweb')

	key = bucket.new_key('campaigns.json')
	key.set_contents_from_string(json.dumps(data_update, indent=4, sort_keys=True))
	key.set_canned_acl('public-read')

sched.start()

while True:
	pass