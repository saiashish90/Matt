import random
import discord
from discord.ext import commands

#basic commands class
class AmongusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.vc = None
    
    # Ping command function
    @commands.command()
    async def amongus(self,ctx):
        if(ctx.author.voice and ctx.author.voice.channel):
            self.vc = ctx.author.voice.channel
            embed = discord.Embed(title="Among Us",description="React to the speaker to mute/unmute.\nReact to the stop to stop the game", color=0xff7b00)
            self.message = await ctx.channel.send(embed=embed)
            emoji1 = '🔇'
            emoji2 = '🛑'
            await self.message.add_reaction(emoji1)
            await self.message.add_reaction(emoji2)
        else:
            embed = discord.Embed(title="Among Us",description="You must join a voice channel to start a game.", color=0xff7b00)
            self.message = await ctx.channel.send(embed=embed) 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,reaction):
        if(str(reaction.emoji) == str('🔇')):
            if(str(reaction.member)!='Mattt#2230'):
                if(reaction.message_id == self.message.id):
                    channel = self.bot.get_channel(reaction.channel_id)
                    [await member.edit(mute=True) for member in self.vc.members]
        else:
            if(str(reaction.member)!='Mattt#2230'):
                if(reaction.message_id == self.message.id):
                    await self.message.delete()
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,reaction):
        if(str(reaction.member)!='Mattt#2230'):
            if(reaction.message_id == self.message.id):
                channel = self.bot.get_channel(reaction.channel_id)
                [await member.edit(mute=False) for member in self.vc.members]

def setup(bot):
    bot.add_cog(AmongusCog(bot))