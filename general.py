from distutils import command
from pydoc import cli
import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self,client):
        super().__init__()
        self.client = client

    @commands.command(aliases=['Hello', 'hi', 'Hi'])
    async def hello(ctx, user: discord.User = None):
        if(user != None):
            await ctx.channel.send('Hello %s!' %user.display_name)
        else:
            await ctx.channel.send('Hello %s!' %ctx.author.display_name)


    @commands.command()
    async def cb(ctx, *, code):
        await ctx.channel.purge(limit = 1)
        await ctx.channel.send(f'```{code}```') 

    @commands.command()
    async def clear(ctx, amount = 10):
        await ctx.channel.purge(limit = amount+1)
        await ctx.channel.send(f'I have deleted {amount} messages!', delete_after = 1.0)


def setup(client):
    client.add_cog(General(client))