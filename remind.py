import discord
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix= '>')


@client.command()
async def remind(ctx, user: discord.User = None):
    if(user != None):
        await ctx.channel.send('Hello %s!' %user.display_name)
    else:
        await ctx.channel.send('Hello %s!' %ctx.author.display_name)