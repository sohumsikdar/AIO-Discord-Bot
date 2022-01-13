import discord
import re
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix= '>')

class Remind(commands.Cog):
	def __init__(self,client):
		super().__init__()
		self.client = client

	@commands.command()
	#Usage: remind <title> due <date> by <time>(opt) <note>(opt)
	async def remind(self,ctx, *, details = ''):
		chk = details.find('on')

		if(chk == -1):
			await ctx.send('Need a due date/time!')
			return

		else:
			dparam = re.split('on|by|note', details)
			dparam = [i.strip() for i in dparam]
			print(dparam)
			if(dparam[0] == ''):
				dparam[0] = 'No Title'
	
		if(len(dparam) == 2):
			dparam.append('2359')
			dparam.append('No Description')
		
		if(len(dparam) == 3):
			if(details.find('note') == -1):
				dparam.append('No Description')
			else:
				dparam.append(dparam[2])
				dparam[2] = '2359'
		
		if(dparam[1] == ''):
			await ctx.send('Incorrect Usage!')
			return
		
		embed = discord.Embed(title = dparam[0].title(), description=dparam[3], color = discord.Color.blue())
		embed.add_field(name = 'Due on: ', value = f'{dparam[1]} at {dparam[2]}', inline=False)
		embed.add_field(name = 'Time left: ', value = '0s')
		embed.add_field(name = 'Next alert in: ', value = '0s')
		await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Remind(client))