import discord
from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
	def __init__(self, client):
		super().__init__()
		self.client = client

	@commands.command(aliases=['p'])
	async def play(self, ctx, url : str):
		if ctx.author.voice is None:
			await ctx.send("Not connected to a voice channel")
		voice_channel = ctx.author.voice.channel
		if ctx.voice_client is None:
		  await voice_channel.connect()
		else:
			await ctx.voice_client.move_to(voice_channel)
		
		ydl_opts = {'format': 'bestaudio'}
		# FFMPEG_OPTIONS = {'before_options' : "reconnect 1 - reconnect_streamed 1 -reconnect_delay_max 5", 'options' : "-vn"}
		
		vc = ctx.voice_client
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url, download = False)
			url2 = info['formats'][0]['url']
			source = await discord.FFmpegOpusAudio.from_probe(url2)
			vc.play(source)
	
	@commands.command()
	async def pause(self, ctx):
		await ctx.voice_client.pause()
		await ctx.send("Paused")

	@commands.command()
	async def resume(self, ctx):
		await ctx.voice_client.resume()
		await ctx.send("Resumed")
	
	@commands.command()
	async def stop(self, ctx):
		await ctx.voice_client.stop()
		await ctx.send("Stopped the playlist")

def setup(client):
    client.add_cog(Music(client))