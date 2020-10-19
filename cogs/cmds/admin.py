from discord import Permissions
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True, read_messages=True)
    async def bulk_delete(self,ctx,messageID: int):
        targetMessage = await ctx.channel.fetch_message(messageID)
        messages = await ctx.channel.history(after=targetMessage).flatten()
        await ctx.channel.delete_messages(messages)

def setup(bot):
    bot.add_cog(Admin(bot))