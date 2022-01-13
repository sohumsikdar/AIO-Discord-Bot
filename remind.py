import discord
import re
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix= '>')


@client.command()
async def remind(self,ctx, *, details = ''):
    chk = details.find('due on')
    if(chk == -1 or details[:chk].strip() == ''):
        await ctx.send('Incorrect Usage!')
        return

    else:
        dparam = re.split('due on|by|note', details)
        dparam = [i.strip() for i in dparam]

    if(len(dparam) == 2):
        dparam.append('2359')
        dparam.append('None')
    
    if(len(dparam) == 3):
        if(details.find('note') == -1):
            dparam.append('None')
        else:
            dparam.append(dparam[2])
            dparam[2] = '2359'
    
    if(dparam[1] == ''):
        await ctx.send('Incorrect Usage!')
        return
    
    embed = discord.Embed(title = dparam[0].title(), description=dparam[3], color = discord.Color.blue())
    embed.add_field(name = 'Due on: ', value = f'{dparam[1]} at {dparam[2]}', inline=False)
    embed.add_field(name = 'Time left: ', value = '0s')
    embed.add_field(name = 'Next alert in: ', value = '0s')
    await ctx.send(embed = embed)