import random
import discord
from discord.ext import commands

#basic commands class
class BasicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping command function
    @commands.command()
    async def ping(cogs , ctx, member, arg=1):
        messages = [
            'peepee small',
            'thou art gay',
            ]
        converter = commands.MemberConverter()
        try:
            member = await converter.convert(ctx,member)
            for i in range(0,arg):
                channel = discord.utils.get(ctx.guild.channels, name='bot-spam')
                if channel is None:
                    await ctx.channel.send("Make a channel called 'bot-spam' to use the ping command")
                    break
                else:
                    if(i == 25):
                        await channel.send("Ping limit is 25")
                        break
                    await channel.send(messages[random.randint(0,len(messages)-1)]+member.mention)
        except: 
            embed = discord.Embed(color = discord.Color.orange())
            embed=discord.Embed(title="Help",description="`$ping [role/user] [n]`", color=0xff7b00)
            await ctx.channel.send(embed=embed)
        

def setup(bot):
    bot.add_cog(BasicCog(bot))