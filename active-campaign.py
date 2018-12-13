import requests
import json
import ruamel.yaml as yaml
import argparse
import os
import sys


class Campaign:
	def __init__(self, args):
		self.api_url = args.api_url
		self.api_key = args.api_key
		self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
		
	def getLists(self):
		request_url = '{}/admin/api.php?api_key={}&api_action=list_list&api_output=json&ids=all'.format(self.api_url, self.api_key)
		response = requests.get(request_url, headers=self.headers)
		return response
		
	def printLists(self):
		response = self.getLists().json()
		for k, v in response.items():
			if k.isdigit():
				print(json.dumps(v, indent=2))
		
	def create(self, payload):
		if not payload:
			print("see all required option descriptions here: https://www.activecampaign.com/api/example.php?call=campaign_create")
			payload['type'] = input("type: ")
			payload['name'] = input("name: ")
			payload['public'] = input("public: ")
			payload['tracklinks'] = input("tracklinks: ")
			lists = input("list ids: ")
			payload['p[{}]'.format(lists)] = lists
			messages = input("message ids: ")
			message_pct = input("send message to n% of contacts. n=")
			payload['m[{}]'.format(messages)] = message_pct
			
		payload['status'] = 0
			
		request_url = '{}/admin/api.php?api_key={}&api_action=campaign_create&api_output=json'.format(self.api_url, self.api_key)
		response = requests.post(request_url, headers=self.headers, data=payload)
		return response
		
	def schedule(self, payload):
		if not payload:
			print("see all required option descriptions here: https://www.activecampaign.com/api/example.php?call=campaign_status")
			payload['id'] = input("campaign id: ")
		payload['status'] = 1
		request_url = '{}/admin/api.php?api_key={}&api_action=campaign_status&api_output=json'.format(self.api_url, self.api_key)
		response = requests.post(request_url, headers=self.headers, data=payload)
		return response
		
	def send(self, payload):
		if not payload:
			print("see all required option descriptions here: https://www.activecampaign.com/api/example.php?call=campaign_status")
			payload['email'] = input("email of contact: ")
			payload['campaignid'] = input("campaign id: ")
			payload['messageid'] = input("message id: ")
			payload['type'] = input("type: ")
			payload['action'] = input("action: ")
		request_url = '{}/admin/api.php?api_key={}&api_action=campaign_send&api_output=json'.format(self.api_url, self.api_key)
		response = requests.post(request_url, headers=self.headers, data=payload)
		return response
		




def arg_parse():
	parser = argparse.ArgumentParser(description='Take action against the active campaign api.')
	parser.add_argument('--action', choices=["create","schedule","send","lists"], help='the action you want to take against the api')
	parser.add_argument('--config', type=str, help='yaml formatted config for a new campaign')
	parser.add_argument('--api-url', type=str, help='api url from your settings -> developer')
	parser.add_argument('--api-key', type=str, help='api key from your settings -> developer')

	args = parser.parse_args()

	return args
	

def parsePayload(args):
	if args.config:
		file = open(args.config, 'r')
		payload = yaml.safe_load(file.read())
		return payload
	else:
		return {}
	
	
def main():
	args = arg_parse()
		
	campaign = Campaign(args)
		
	if args.action == "create":
		response = campaign.create(parsePayload(args))
	elif args.action == "schedule":
		response = campaign.schedule(parsePayload(args))
	elif args.action == "send":
		response = campaign.send(parsePayload(args))
	elif args.action == "lists":
		campaign.printLists()
		sys.exit()
		

		
	
	
	print(response.json()['result_message'])

		
	
if __name__ == "__main__":
	main()