from server_pings import server_ping
import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print('{0.user} logged in'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello {}!'.format(
            message.author.display_name))


server_ping()
tok = os.environ['TOKEN']
client.run(tok)
