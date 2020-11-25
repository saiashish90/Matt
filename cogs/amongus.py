import random
import discord
from discord.ext import commands

#basic commands class
class AmongusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message = None
    
    # Ping command function
    @commands.command()
    async def amongus(self,ctx):
        embed = discord.Embed(title="Among Us",description="React to the message to mute/unmute.", color=0xff7b00)
        self.message = await ctx.channel.send(embed=embed)
        emoji = '🔇'
        await self.message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,reaction):
        if(reaction.message_id == self.message.id):
            channel = self.bot.get_channel(reaction.channel_id)
            await channel.send("reacted")
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,reaction):
        if(reaction.message_id == self.message.id):
            channel = self.bot.get_channel(reaction.channel_id)
            await channel.send("cleared")

def setup(bot):
    bot.add_cog(AmongusCog(bot))