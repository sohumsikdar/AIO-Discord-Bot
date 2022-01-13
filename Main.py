from server_pings import server_ping
import discord
import os
from remind import *
from discord.ext import commands

client = discord.Client()

client = commands.Bot(command_prefix= '>')

@client.event
async def on_ready():
    print('{0.user} logged in'.format(client))

@client.command(aliases=['Hello', 'hi', 'Hi'])
async def hello(ctx, user: discord.User = None):
    if(user != None):
        await ctx.channel.send('Hello %s!' %user.display_name)
    else:
        await ctx.channel.send('Hello %s!' %ctx.author.display_name)

@client.command()
async def cb(ctx, *, code):
    await ctx.channel.purge(limit = 1)
    await ctx.channel.send(f'```{code}```') 

@client.command()
async def clear(ctx, amount = 10):
    await ctx.channel.purge(limit = amount+1)
    await ctx.channel.send(f'I have deleted {amount} messages!', delete_after = 1.0)

# @client.command(alisases=['p', 'P', 'Play'])
# async def play()

server_ping()
tok = os.environ['TOKEN']
client.run(tok)
