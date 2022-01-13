import discord
from discord.ext import commands
import os
import requests


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
		self.fav_subs = []


	# Command Functions
	@commands.command()
	async def search(self,ctx,sub):
		if sub.startswith('r/') == False:
			await ctx.channel.send('Use correct subreddit formats like r/rickroll')

		else:
			url_list = self.fetch_from_sub(sub)
			if url_list == None or len(url_list) < 1:
				if len(url_list) < 1:
					await ctx.channel.send('No hot posts to display')
				else: 
					await ctx.channel.send('Couldn\'t find ' + sub)
			else:
				await ctx.channel.send(url_list[0])

	
	@commands.command()
	async def add_to_fav_subs(self,ctx,sub):
		pass

	@commands.command()
	async def fetch(self,ctx, amount = 5, sub = None):
		pass


	#Helper Functions
	def fetch_from_sub(self,sub):
		url = 'https://oauth.reddit.com/' + sub + '/hot'
		result = requests.get(url, headers = self.headers)
		if result.status_code == 404:
			return None

		print(result)
		res = result.json()
		url_list = []
		for post in res['data']['children']:
			url_list.append('https://www.reddit.com' + post['data']['permalink'])

		return url_list





def setup(client):
	client.add_cog(RedditCommands(client))