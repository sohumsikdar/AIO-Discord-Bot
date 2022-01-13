from datetime import date
import discord
import re
from discord.ext import commands
import dateutil.parser

client = discord.Client()
client = commands.Bot(command_prefix= '>')

class Remind(commands.Cog):
	def __init__(self,client):
		super().__init__()
		self.client = client

	@commands.command()
    #Usage: <title> (optional) by <date> on <time>
    # (can be anyone of these but at least one) for <details> (optional)
	async def remind(self,ctx, *, details = ''):
		dparam = []
		if(details.find('at-') == -1 and details.find('by-') == -1):
			await ctx.send('Need a due date/time!')
			return
		else:
			dparam = re.split('by-|at-|for-', details)
			dparam = [i.strip() for i in dparam]
			if(dparam[0] == ''):
				dparam[0] = 'No Title'

			if(len(dparam) == 2):
				if(details.find('by-')== -1):
					dparam.insert(1,str(date.today()))
				else:
					dparam.append('2359')

			if(len(dparam) == 3):
				if(details.find('for-') == -1):
					dparam.append('No Description')
				elif(details.find('by-') == -1):
					dparam.insert(1,str(date.today())) 
				else:
					dparam.append(dparam[2])
					dparam[2] = '2359'
		
		if(dparam[1] == ''):
			await ctx.send('Incorrect Usage!')
			return
		
		formatted_date = dateutil.parser.parse(dparam[1]+" "+dparam[2],fuzzy_with_tokens=False)
		dparam[1] = str(formatted_date.date())
		dparam[2] = str(formatted_date.time())

		embed = discord.Embed(title = dparam[0].title(), description=dparam[3], color = discord.Color.blue())
		embed.add_field(name = 'Due on: ', value = f'{dparam[1]} at {dparam[2]}', inline=False)
		embed.add_field(name = 'Time left: ', value = '0s')
		embed.add_field(name = 'Next alert in: ', value = '0s')
		await ctx.send(embed = embed)

		

def setup(client):
    client.add_cog(Remind(client))