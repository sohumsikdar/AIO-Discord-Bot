from datetime import date, timedelta, datetime
import discord, asyncio, pytz
import re
from discord.ext import commands
import dateutil.parser
from pytimeparse import parse

IST = pytz.timezone('Asia/Kolkata')
client = discord.Client()
client = commands.Bot(command_prefix= '>')

class Remind(commands.Cog):
	def __init__(self,client):
		super().__init__()
		self.client = client

	@commands.command()
	async def timer(self,ctx,*,dur):
		val = 'You will be notified when timer ends. Other users can also be notified by reacting as ⏰. Users can also be notified in dm by reacting as 🗨️'
		dur = parse(dur)
		desc = str(timedelta(seconds=dur))
		embed = discord.Embed(title = "Timer Added!", color = discord.Color.red())
		embed.add_field(name= desc,value= val)
		embed.set_thumbnail(url='https://previews.123rf.com/images/djvstock/djvstock1801/djvstock180109568/94114510-red-clock-with-yellow-background-vector-ilustration.jpg?fj=1')
		msg = await ctx.send(embed = embed)
		await msg.add_reaction("⏰")
		users = set()
    
		while True:
			await asyncio.sleep(1)
			dur -= 1
			if(dur == 0):
				msg = await msg.channel.fetch_message(msg.id)
				for reaction in msg.reactions:
					async for user in reaction.users():
						if (user.bot == False):
							users.add(user.mention)
				users.add(ctx.author.mention)
				mentions = ""
				for user in users:
					mentions += str(user)+" "
				await ctx.send(f"{mentions} Time's up!")
				break
			

	@commands.command()
    #Usage: <title> (optional) by <date> on <time>
    # (can be anyone of these but at least one) for <details> (optional)
	async def remind(self,ctx, *, details = ''):
		dparam = []
		durations = [86400,3600,600,0]
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
					dparam.append('23:59:59')

			if(len(dparam) == 3):
				if(details.find('for-') == -1):
					dparam.append('No Description')
				elif(details.find('by-') == -1):
					dparam.insert(1,str(date.today())) 
				else:
					dparam.append(dparam[2])
					dparam[2] = '23:59:59'
		
		if(dparam[1] == ''):
			await ctx.send('Incorrect Usage!')
			return
		formatted_date = dateutil.parser.parse(dparam[1],fuzzy_with_tokens=False)
		dparam[1] = str(formatted_date.date())
		formatted_date = dateutil.parser.parse(dparam[1]+" "+dparam[2],fuzzy_with_tokens=False)
		dparam[2] = str(formatted_date.time())

		deadline_datetime = IST.localize(formatted_date)

		dur = (deadline_datetime - datetime.now(IST)).total_seconds()
		idx = 0
		for idx in range(4):
			if(dur > durations[idx]):
				break

		if(idx < 3):
			next_alert = int(dur-durations[idx+1])
		else:
			next_alert = int(dur)

		embed = self.get_embed(dparam,next_alert)
		msg = await ctx.send(embed = embed)
		await msg.add_reaction("⏰")

		while(idx < 4):
			await asyncio.sleep(dur-durations[idx])
			dur = durations[idx]
			if(idx < 3):
				next_alert = int(dur-durations[idx+1])
			else:
				next_alert = "Deadline Up!"
			embed = self.get_embed(dparam,next_alert)
			users = set()
			msg = await msg.channel.fetch_message(msg.id)
			for reaction in msg.reactions:
				async for user in reaction.users():
					if (user.bot == False):
						users.add(user.mention)
			users.add(ctx.author.mention)
			mentions = ""
			for user in users:
				mentions += str(user)+" "
			await ctx.send(f"{mentions}",embed = embed)
			idx += 1	

	def get_embed(self,dparam,next_alert):
		embed = discord.Embed(title = "Reminder: "+dparam[0].title(), description=dparam[3], color = discord.Color.blue())
		embed.add_field(name = 'Due on: ', value = f'{dparam[1]} at {dparam[2]}', inline=False)
		embed.add_field(name = 'Next alert in: ', value = self.get_formatted(next_alert))
		return embed

	def get_formatted(self,next_alert):
		day = next_alert // (24 * 3600)
		next_alert = next_alert % (24 * 3600)
		hour = next_alert // 3600
		next_alert %= 3600
		minutes = next_alert // 60
		next_alert %= 60
		seconds = next_alert
		return str(day)+"d "+str(hour)+"h "+str(minutes)+"m "+str(seconds)+"s "
		

def setup(client):
    client.add_cog(Remind(client))