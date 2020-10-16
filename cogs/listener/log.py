from discord.ext import commands
import keys

class Log(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content.startswith(keys.PREFIX) and not message.author.bot:
            print("{}: {}".format(message.author,message.content))

def setup(bot):
    bot.add_cog(Log(bot))