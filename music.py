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
    	
		await ctx.guild.change_voice_state(channel=voice_channel, self_mute=False, self_deaf=True)

		if ctx.voice_client is None:
			await voice_channel.connect()
		else:
			await ctx.voice_client.move_to(voice_channel)
		
		ytdl_format_options = {
        'format': 'bestaudio/best',
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
		
		vc = ctx.voice_client
		with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
			ydl.cache.remove() 
			info = ydl.extract_info(url, download = False)
			url2 = info['formats'][0]['url']
			source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
			vc.play(source)
	
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

def setup(client):
    client.add_cog(Music(client))