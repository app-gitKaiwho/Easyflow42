import discord, json, os
from discord.ext import commands
from SRC.cog import Easyflow

DISCORD_SERVER_ID  = os.getenv("DISCORD_SERVER_ID")
param = json.load(open('config.json', 'r'))
if DISCORD_SERVER_ID  is None:
    DISCORD_SERVER_ID  = param.get('guild_id')
channel_id = param.get('channel_id')

bot = discord.Bot()
bot.add_cog(Easyflow(bot, DISCORD_SERVER_ID, channel_id))
bot.run(param.get('token'))