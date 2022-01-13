from server_pings import server_ping
import discord
import os
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix= '>')


cog_files = ['general', 'music', 'remind', 'reddit_commands']

for cog_file in cog_files: 
    client.load_extension(cog_file) 
    print("%s has loaded." % cog_file)


@client.event
async def on_ready():
    print('{0.user} logged in'.format(client))


server_ping()
tok = os.environ['TOKEN']
client.run(tok)
