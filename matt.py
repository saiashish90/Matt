import os
import json

import discord
from discord.ext import commands

from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin

# from dotenv import load_dotenv
# load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents().all()
# firebase

cred = credentials.Certificate(json.loads(os.getenv('GOOGLE_KEY')))
firebase_admin.initialize_app(cred, {
    'projectId': 'amongus-44241'
})
db = firestore.client()
# Paths for all the cogs
startup_extensions = ['cogs.basic', 'cogs.amongus']
# initializing bot commands
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command('help')


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Help", description="***Commands***\n\n`$ping [role/user] [n]` \nPings role/user n times.\n\n`$amongus`\nLets you mute members during among us game.", color=0xff7b00)
    await ctx.channel.send(embed=embed)

# Bot on load functions


@bot.event
async def on_guild_join(guild):
    print("joined")
    db.collection('Mattt').document(str(guild.id)).set({
        "id": str(guild.id)
    })
    db.collection('Mattt').document(str(guild.id)).collection('amongus').document('stats').set({
        "is_playing": False,
        "is_muted": False,
        "game_state": 'discussion',
        'game_code': '',
        'game_channel': '',
        'message_id': '',
    })


@bot.event
async def on_guild_remove(guild):
    print("left")
    db.collection('Mattt').document(str(guild.id)).collection(
        'amongus').document('stats').delete()
    db.collection('Mattt').document(str(guild.id)).delete()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Wii Sports'))
    print(f'{bot.user} has connected to Discord!')
    ids = []
    [ids.append(id.to_dict()['id'])for id in db.collection('Mattt').get()]
    for guild in bot.guilds:
        ids.remove(str(guild.id))
        db.collection('Mattt').document(str(guild.id)).set({
            "id": str(guild.id)
        })
        db.collection('Mattt').document(str(guild.id)).collection('amongus').document('stats').set({
            "is_playing": False,
            "is_muted": False,
            "game_state": 'discussion',
            'game_code': '',
            'game_channel': '',
            'message_id': '',
        })
    for id in ids:
        print('trimming')
        db.collection('Mattt').document(id).collection(
            'amongus').document('stats').delete()
        db.collection('Mattt').document(id).delete()

# Importing all the cogs
for extension in startup_extensions:
    bot.load_extension(extension)

bot.run(TOKEN)
