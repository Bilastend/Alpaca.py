import keys
from discord.ext import commands
from discord.utils import get

class Manage(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = member.guild.get_role(keys.USER_ROLE_ID)
        await member.add_roles(role)

def setup(bot):
    bot.add_cog(Manage(bot))