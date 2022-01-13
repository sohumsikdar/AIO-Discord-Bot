import discord
from discord.ext import commands
import os
import requests



res = requests.get('https://oauth.reddit.com/r/dankinindia/hot', headers = headers).json()
for post in res['data']['children']:
	print('https://www.reddit.com' + post['data']['permalink'])


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
        self.res = requests.post('https://www.reddit.com/api/v1/access_token', auth = self.auth, data = self.data, headers = self.headers)
        self.reddit_token = res.json()['access_token']
        self.headers['Authorization'] = f'bearer {self.reddit_token}'


    @commands.command()
    async def search(self,ctx,sub):
        pass

    @commands.command()
    async def add(self,ctx,sub):
        pass 

    @commands.command()
    async def fetch(self,ctx, amount = 5, sub = None):
        pass
        # await ctx.channel.send(f'I have deleted {amount} messages!', delete_after = 1.0)


def setup(client):
    client.add_cog(General(client))