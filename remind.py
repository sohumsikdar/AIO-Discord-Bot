from datetime import date, timedelta, datetime
import discord, asyncio, pytz
import re
from discord.ext import commands
import dateutil.parser
from pytimeparse import parse

IST = pytz.timezone('Asia/Kolkata')
client = discord.Client()
client = commands.Bot(command_prefix= '>')

val = "You will be notified when it ends. Other users can also be notified by reacting as ⏰. Users can also be notified in dm by reacting as 🗨️"

class Remind(commands.Cog):
	def __init__(self,client):
		super().__init__()
		self.client = client

	@commands.command()
	async def timer(self,ctx,*,dur):
		try:
			dur = parse(dur)
			if(dur < 0):
				await ctx.send("Cannot go back in time!")
				return
			
			elif(dur > 86400):
				await ctx.send("Cannot set a timer for more than a day! Use `>remind`.")
				return

			desc = str(timedelta(seconds=dur))
			embed = discord.Embed(title = "Timer Added!", color = discord.Color.red())
			embed.add_field(name= desc,value= val)
			embed.set_thumbnail(url='https://previews.123rf.com/images/djvstock/djvstock1801/djvstock180109568/94114510-red-clock-with-yellow-background-vector-ilustration.jpg?fj=1')
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
			msg = await ctx.send(embed = embed)
			await msg.add_reaction("⏰")
			await msg.add_reaction("🗨️")
		
			while True:
				await asyncio.sleep(1)
				dur -= 1
				if(dur == 0):
					msg = await msg.channel.fetch_message(msg.id)

					users_to_mention = set()
					users_to_dm = set()

					for reaction in msg.reactions:
						if(reaction.emoji == "⏰"):
							async for user in reaction.users():
								if (user.bot == False):
									users_to_mention.add(user.mention)
							
						elif (reaction.emoji == "🗨️"):
							async for user in reaction.users():
								if (user.bot == False):
									users_to_dm.add(user)

					users_to_mention.add(ctx.author.mention)
					mentions = ""
					for user in users_to_mention:
						mentions += str(user)+" "
					await ctx.send(f"{mentions} Time's up!")

					for user in users_to_dm:
						await user.send(f"One of your timer for duration `{desc}` elapsed!")

					break

		except:
			await ctx.send("Cannot understand the time you have given!")
			return
			
				

	@commands.command()
    #Usage: <title> (optional) by <date> <time>
    # (can be anyone of these but at least one) for <details> (optional)
	async def remind(self,ctx, *, details = ''):
		dparam = []
		durations = [86400,3600,600,0]
		if(details.find('by-') == -1):
			await ctx.send('Dude! When do you want me to remind you?')
			return

		dparam = re.split('by-|for-', details)
		dparam = [i.strip() for i in dparam]

		reminder = Reminder()

		if(dparam[0] != ''):
			reminder.set_title(dparam[0])

		try:
			if(details.find('for-') != -1):
				if (details.find('for-') > details.find('by-')):
					reminder.set_desc(dparam[2])
					reminder.set_datetime(dparam[1])
				else:
					reminder.set_desc(dparam[1])
					reminder.set_datetime(dparam[2])

			else:
				reminder.set_datetime(dparam[1])

		except:
			await ctx.send("Cannot understand the date or time you have given!")
			return

		deadline_datetime = IST.localize(reminder.get_datetime())
		dur = (deadline_datetime - datetime.now(IST)).total_seconds()
		idx = 0
		for idx in range(4):
			if(dur > durations[idx]):
				break

		if(idx < 3):
			next_alert = int(dur-durations[idx+1])
		else:
			next_alert = int(dur)
		
		if(next_alert < 0):
			await ctx.send("Cannot go back in time!")
			return

		elif(next_alert > (86400*366)):
			await ctx.send("Cannot set a reminder for more than a year!")
			return

		embed = reminder.get_embed(next_alert)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		msg = await ctx.send(embed = embed)
		await msg.add_reaction("⏰")
		await msg.add_reaction("🗨️")
		await msg.add_reaction("❌")

		while(idx < 4):
			if(dur == 0):
				idx = 3
				continue

			await asyncio.sleep(dur-durations[idx])
			dur = durations[idx]
			if(idx < 3):
				next_alert = int(dur-durations[idx+1])
			else:
				next_alert = ""
			embed = reminder.get_embed(next_alert)

			msg = await msg.channel.fetch_message(msg.id)
			users_to_mention = set()
			users_to_dm = set()
			for reaction in msg.reactions:
				if(reaction.emoji == "⏰"):
					async for user in reaction.users():
						if (user.bot == False):
							users_to_mention.add(user.mention)
					
				elif (reaction.emoji == "🗨️"):
					async for user in reaction.users():
						if (user.bot == False):
							users_to_dm.add(user)

			users_to_mention.add(ctx.author.mention)
			mentions = ""
			for user in users_to_mention:
				mentions += str(user)+" "
			await ctx.send(f"{mentions}",embed = embed)

			for user in users_to_dm:
				await user.send(embed = embed)

			idx += 1	

	@commands.Cog.listener()
	async def on_raw_reaction_add(self,payload):
		msg_id = payload.message_id
		emoji = payload.emoji.name
		channel = self.client.get_channel(payload.channel_id)
		user = await self.client.fetch_user(payload.user_id)
		if(emoji == "❌" and user.bot == False):
			await channel.send(f"{user.name} pressed {emoji} on message")
			

def setup(client):
    client.add_cog(Remind(client))


class Reminder():
	def __init__(self):
		self.title = "No Title"
		self.due_datetime = None
		self.description = "No Description"
		self.active = True
		self.list_of_msg_id = []

	def inactivate(self):
		self.active = False

	def is_active(self):
		return self.active

	def __str__(self):
		return self.title + " by- " + str(self.due_datetime) + " for- "+ self.description

	def set_title(self,title_str):
		self.title = title_str
	
	def set_desc(self,desc_str):
		self.description = desc_str
	
	def set_datetime(self,datetime_str):
		try:
			formatted_date = dateutil.parser.parse(datetime_str,fuzzy_with_tokens=False)
			try:
				formatted_date2 = dateutil.parser.parse(datetime_str+" 1 jan 1979",fuzzy_with_tokens=False)
				if(formatted_date.date() != formatted_date2.date()):
					self.due_datetime = datetime.combine(datetime.now(IST).date(),formatted_date.time())

			except:
				self.due_datetime = formatted_date
		except:
			raise Exception()
	
	def get_datetime(self):
		return self.due_datetime

	def get_embed(self,next_alert):
		embed = discord.Embed(title = "Reminder: "+self.title.title(), description=self.description, color = discord.Color.blue())
		embed.add_field(name = 'Due on: ', value = f'{str(self.due_datetime.date())} at {str(self.due_datetime.time())}', inline=False)
		embed.add_field(name = 'Next alert in: ', value = self.get_formatted(next_alert))
		embed.set_footer(text = val)
		embed.set_thumbnail(url='https://previews.123rf.com/images/djvstock/djvstock1801/djvstock180109568/94114510-red-clock-with-yellow-background-vector-ilustration.jpg?fj=1')
		return embed

	def get_formatted(self,next_alert):
		if(next_alert == ""):
			return "Deadline's up!"
		day = next_alert // (24 * 3600)
		next_alert = next_alert % (24 * 3600)
		hour = next_alert // 3600
		next_alert %= 3600
		minutes = next_alert // 60
		next_alert %= 60
		seconds = next_alert
		return str(day)+"d "+str(hour)+"h "+str(minutes)+"m "+str(seconds)+"s "