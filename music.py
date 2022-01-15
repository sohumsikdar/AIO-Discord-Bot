from distutils import command
import discord
import os
from discord.ext import commands
import youtube_dl
import requests
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
	'extractaudio': True,
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ydl = youtube_dl.YoutubeDL(ytdl_format_options)

class Music(commands.Cog):
	def __init__(self, client):
		super().__init__()
		self.client = client
		self.ytb_api = os.environ['GOOGLE_API_KEY']
		self.song_q = []
		# self.generate()
		
	# def generate(self):
	# 	for guild in self.client.guilds:
	# 		self.song_q[guild.id] = []
	# 		print('hello')
	# 		print(guild.id)
	
	@commands.command()
	async def setup(self, ctx):
		channel = discord.utils.get(ctx.guild.channels, name='aio-music-player')
		if channel is None:
			channel1 = await ctx.guild.create_text_channel('AIO music player')
			await channel1.send('Text in channel')
		else:
			await ctx.send("Music player already exists")
	
	async def check_q(self, ctx):
		if len(self.song_q) > 0:
			ctx.voice_client.stop()
			await self.now_playing(ctx, self.song_q[0])
			self.song_q = self.song_q[1:]

	@commands.command(aliases=['p'])
	async def play(self, ctx, *, url : str):
		if 'youtube.com/' not in url:
			url = self.fetch_url_from_youtube(url)
		else:
			url_lst = url.split()
			if len(url_lst) > 1:
				await ctx.send("Either enter a link or keywords")
				return

		if ctx.author.voice is None:
			await ctx.send("Not connected to a voice channel")

		voice_channel = ctx.author.voice.channel
    	
		if ctx.voice_client is None:
			await voice_channel.connect()
		elif ctx.voice_client.channel != voice_channel:
			await ctx.send("You are not in the same voice channel!")
			return
		
		ydl.cache.remove() 
		info = ydl.extract_info(url, download = False)
		url = info['formats'][0]['url']
		if ctx.voice_client.source is not None:
			queue_len = len(self.song_q)
			self.song_q.append(url)
		await self.now_playing(ctx, url)
		
	async def now_playing(self, ctx, url):
		source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url, **ffmpeg_options))
		ctx.voice_client.play(source, after=lambda error: self.client.loop.create_task(self.check_q(ctx)))
	
	@commands.command()
	async def pause(self, ctx):
		await ctx.voice_client.pause()
		await ctx.channel.send("Paused")

	@commands.command()
	async def resume(self, ctx):
		await ctx.voice_client.resume()
		await ctx.channel.send("Resumed")
	
	@commands.command(aliases = ['dc'])
	async def disconnect(self, ctx):
		await ctx.voice_client.disconnect()
		await ctx.channel.send("Stopped the playlist")


	def fetch_url_from_youtube(self,query):
		query_list = query.split()
		query_string = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key=' + self.ytb_api + '&type=video&q='
		for word in query_list:
			query_string = query_string + word + '%20'


		res = requests.get(query_string).json()
		video_id = str(res['items'][0]['id']['videoId'])

		url = 'https://www.youtube.com/watch?v=' + video_id
		print(query_string)
		print(url)
		return url

def setup(client):
    client.add_cog(Music(client))