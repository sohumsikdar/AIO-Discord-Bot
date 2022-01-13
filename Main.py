from server_pings import server_ping
import discord
import os
from discord.ext import commands

client = discord.Client()

client = commands.Bot(command_prefix= '>')

@client.event
async def on_ready():
    print('{0.user} logged in'.format(client))


@client.command(aliases= ['Hello', 'hi', 'Hi'])
async def hello(ctx, user: discord.User = None):
    if(user != None):
        await ctx.channel.send('Hello <@%s>!' %user.display_name)
    else:
        await ctx.channel.send('Hello <@%s>!' %ctx.author.display_name)


server_ping()
tok = os.environ['TOKEN']
client.run(tok)
