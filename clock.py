from apscheduler.scheduler import Scheduler
from lxml import html
import requests
import json

sched = Scheduler()

@sched.interval_schedule(minutes=10)
def timed_job():
	# Load campaigns pickle file
	data = json.loads(open('campaigns.json').read())

	# Create new campaigns list
	data_update = []

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
			thisDict['amountTarget'] = amountTargetFull[0][1:]
			thisDict['currency'] = amountTargetFull[0][0:1]
			amountRaisedFull = tree.xpath('//div[@class="i-balance"]/span/span/text()')
			thisDict['amountRaised'] = amountRaisedFull[0][1:]
			thisDict['url'] = list['url']

			data_update.append(thisDict)

		# Save new campaign list
		with open('campaigns.json', 'w') as outfile:
			json.dump(data, outfile, indent=4, sort_keys=True)

sched.start()

while True:
    pass