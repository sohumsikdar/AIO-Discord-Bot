import discord
from discord.ext import commands
import os
import requests
import random

class RedditCommands(commands.Cog):
	def __init__(self,client):
		super().__init__()
		self.client = client

		self.CLIENT_ID = 'dQ36pUHNsNEs_2o1zJFllw'
		self.secret_id = str(os.environ['SECRET_ID'])
		self.SECRET_ID = self.secret_id
		self.auth = requests.auth.HTTPBasicAuth(self.CLIENT_ID, self.SECRET_ID)
		self.reddit_pass = str(os.environ['reddit_password'])
		self.data = {
		    'grant_type': 'password',
		    'username': 'throwawayDiscordBot1',
		    'password': self.reddit_pass
		}
		self.headers = {'User-Agent': 'RedditApi/0.0.1'}
		self.res = requests.post('https://www.reddit.com/api/v1/access_token', auth = self.auth, data=self.data, headers=self.headers)
		self.reddit_token = self.res.json()['access_token']
		self.headers['Authorization'] = f'bearer {self.reddit_token}'
		self.fav_subs = set()


	# Command Functions
	@commands.command()
	async def search(self,ctx,*,query=''):
		if query == '':
			await ctx.channel.send('I CAN\'T FETCH YOU THE ENTIRETY OF REDDIT!')
			return

		if query.startswith('r/') == False:
			url_list = self.search_in_reddit(query)
			if url_list == None or len(url_list) == 0:
				await ctx.channel.send('Couldn\'t find ' + query)
			else:
				for url_idx in range(0, 5):
					if(url_idx >= len(url_list)):
						break
					await ctx.channel.send(url_list[url_idx])

		else:
			query_list = query.split()
			if len(query_list) == 1:
				url_list = self.fetch_from_sub(query)
				if url_list == None or len(url_list) == 0:
					await ctx.channel.send('Couldn\'t find ' + query)
				else:
					url_idx = random.randint(1, len(url_list))
					await ctx.channel.send(url_list[url_idx - 1])
			else:
				sub = query_list[0]
				query_list.remove(sub)
				url_list = self.search_in_subreddit(sub,query_list)
				if url_list == None or len(url_list) == 0:
					await ctx.channel.send('Couldn\'t find ' + query)
				else:
					for url_idx in range(0, 5):
						if(url_idx >= len(url_list)):
							break
						await ctx.channel.send(url_list[url_idx])


	@commands.command()
	async def fetch(self,ctx,sub=None):
		amount = 1
		if sub==None:
			await ctx.channel.send('Nothing to fetch from')
		else:
			if sub==None:
				url_list = []
				for sub in self.fav_subs:
					res = self.fetch_from_sub(sub,10)
					if res != None:
						url_list.extend(res)

				if len(url_list) == 0:
					await ctx.channel.send('No posts to show!')
				else:
					for _ in range(0, amount):
						url_idx = random.randint(1, len(url_list))
						await ctx.channel.send(url_list[url_idx - 1])

			else:
				if sub.startswith('r/') == False:
					await ctx.channel.send('Use correct subreddit formats like r/rickroll')
					return
					
				else:
					url_list = self.fetch_from_sub(sub)
					if url_list == None or len(url_list) == 0:
						await ctx.channel.send('Couldn\'t find ' + sub)
					else:
						for _ in range(0, amount):
							url_idx = random.randint(1, len(url_list))
							await ctx.channel.send(url_list[url_idx - 1])
		
	#Helper Functions
	def fetch_from_sub(self,sub,limit=100):
		url = 'https://oauth.reddit.com/' + sub + '/?limit=' + str(limit) + '&t=month'
		result = requests.get(url, headers = self.headers)
		if result.status_code == 404:
			return None

		res = result.json()
		url_list = []
		for post in res['data']['children']:
			url_list.append('https://www.reddit.com' + post['data']['permalink'])

		return url_list

	def search_in_reddit(self,query):
		search_string = 'https://oauth.reddit.com/search/?q='
		query_list = query.split()
		for word in query_list:
			search_string = search_string + word + '%20'

		result = requests.get(search_string, headers = self.headers)
		if result.status_code == 404:
			return None
		
		res = result.json()
		url_list = []
		for post in res['data']['children']:
			url_list.append('https://www.reddit.com' + post['data']['permalink'])

		return url_list

	def search_in_subreddit(self, sub, query_list):
		search_string = 'https://oauth.reddit.com/' + sub + '/search/?q=' 
		for word in query_list:
			search_string = search_string + word + '%20'
		
		search_string = search_string + '&restrict_sr=1&sr_nsfw=&include_over_18=1'
		result = requests.get(search_string, headers = self.headers)
		if result.status_code == 404:
			return None
		print(search_string)
		res = result.json()
		url_list = []
		for post in res['data']['children']:
			# print('https://www.reddit.com' + post['data']['permalink'])
			url_list.append('https://www.reddit.com' + post['data']['permalink'])

		return url_list


def setup(client):
	client.add_cog(RedditCommands(client))
