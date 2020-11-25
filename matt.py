import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# Paths for all the cogs
startup_extensions = ['cogs.basic']
# initializing bot commands
bot = commands.Bot(command_prefix="$")
bot.remove_command('help')
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        color = discord.Color.orange()
    )
    embed=discord.Embed(title="Help",description="***Commands***\n\n`$ping [role/user] [n]` \nPings role/user n times ", color=0xff7b00)
    await ctx.channel.send(embed=embed)

# Bot on load functions
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game('Wii Sports'))
    print(f'{bot.user} has connected to Discord!')

# Importing all the cogs
for extension in startup_extensions:
    bot.load_extension(extension)

bot.run(str(os.environ.get('BOT_TOKEN')))
