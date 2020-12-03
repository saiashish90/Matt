import asyncio
import os
import json
import random

import discord
from discord.ext import tasks, commands

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(json.loads(os.getenv('GOOGLE_KEY')))
firebase_admin.initialize_app(cred, {
    'projectId': 'amongus-44241'
}, 'cog')
db = firestore.client()
firebaseListener = {}
# basic commands class


class AmongusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def muter(self, doc):
        guild_id = (doc._reference.parent.parent.id)
        data = doc.to_dict()
        channel = self.bot.get_channel(data['game_channel'])
        print(str(channel))
        if(doc.to_dict()['game_state'] == 'discussion' and data['is_muted']):
            arg = False
            [await member.edit(mute=arg) for member in channel.members]
            db.collection('Mattt').document(guild_id).collection('amongus').document('stats').update({
                "is_muted": arg,
            })
        elif(doc.to_dict()['game_state'] == 'tasks' and not(data['is_muted'])):
            arg = True
            [await member.edit(mute=arg) for member in channel.members]
            db.collection('Mattt').document(guild_id).collection('amongus').document('stats').update({
                "is_muted": arg,
            })

    def on_snapshot(self, doc_snapshot, changes, read_time):
        send_fut = asyncio.run_coroutine_threadsafe(
            self.muter(doc_snapshot[0]), self.bot.loop)
        send_fut.result()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if(str(reaction.emoji) == str('🔇')):
            if(str(reaction.member) != 'Mattt#2230'):
                gamedetails = db.collection('Mattt').document(str(reaction.guild_id)).collection(
                    'amongus').document('stats').get().to_dict()
                if reaction.member.voice:
                    if gamedetails['game_channel'] == reaction.member.voice.channel.id:
                        if gamedetails['message_id'] == reaction.message_id:
                            channel = self.bot.get_channel(
                                gamedetails['game_channel'])
                            [await member.edit(mute=True) for member in channel.members]
        else:
            if(str(reaction.member) != 'Mattt#2230'):
                gamedetails = db.collection('Mattt').document(str(reaction.guild_id)).collection(
                    'amongus').document('stats').get().to_dict()
                if reaction.member.voice:
                    if gamedetails['game_channel'] == reaction.member.voice.channel.id:
                        if gamedetails['message_id'] == reaction.message_id:
                            message = await self.bot.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
                            channel = self.bot.get_channel(
                                gamedetails['game_channel'])
                            [await member.edit(mute=False) for member in channel.members]
                            await message.delete()
                            doc = firebaseListener[str(reaction.guild_id)]
                            doc.unsubscribe()
                            db.collection('Mattt').document(str(reaction.guild_id)).collection('amongus').document('stats').update({
                                "is_playing": False,
                                "is_muted": False,
                                "game_state": 'discussion',
                                'game_code': '',
                                'game_channel': '',
                                'message_id': '',
                            })

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        member = self.bot.get_guild(
            reaction.guild_id).get_member(reaction.user_id)
        if(str(reaction.emoji) == str('🔇')):
            if(str(member) != 'Mattt#2230'):
                gamedetails = db.collection('Mattt').document(str(reaction.guild_id)).collection(
                    'amongus').document('stats').get().to_dict()
                if member.voice:
                    if gamedetails['game_channel'] == member.voice.channel.id:
                        if gamedetails['message_id'] == reaction.message_id:
                            channel = self.bot.get_channel(
                                gamedetails['game_channel'])
                            [await member.edit(mute=False) for member in channel.members]

    @commands.command()
    async def amongus(self, ctx):
        if db.collection('Mattt').document(str(ctx.guild.id)).collection('amongus').document('stats').get().to_dict()['is_playing']:
            embed = discord.Embed(
                title="Among Us", description="A game is already being played", color=0xff7b00)
            await ctx.channel.send(embed=embed)
        else:
            if(ctx.author.voice and ctx.author.voice.channel):
                arg = random.randint(10000,99999)
                embed = discord.Embed(
                    title="Among Us[BETA]", description="Connect token:"+str(arg)+"\nMute/Unmute should happen automatically\nReact to the speaker to mute/unmute.\nReact to the stop to stop the game", color=0xff7b00)
                message = await ctx.channel.send(embed=embed)
                emoji1 = '🔇'
                emoji2 = '🛑'
                await message.add_reaction(emoji1)
                await message.add_reaction(emoji2)
                db.collection('Mattt').document(str(ctx.guild.id)).collection('amongus').document('stats').update({
                    "is_playing": True,
                    "is_muted": False,
                    "game_state": 'discussion',
                    'game_code': str(arg),
                    'game_channel': ctx.author.voice.channel.id,
                    'message_id': message.id,
                })
                firebaseListener[str(ctx.guild.id)] = db.collection('Mattt').document(str(ctx.guild.id)).collection(
                    'amongus').document('stats').on_snapshot(self.on_snapshot)
            else:
                embed = discord.Embed(
                    title="Among Us", description="You must join a voice channel to start a game.", color=0xff7b00)
                await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(AmongusCog(bot))
