import discord
from discord.ext import commands

class Music(commands.Cog):
  pass


def setup(client):
    client.add_cog(Music(client))