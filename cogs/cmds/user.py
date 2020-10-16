import discord
from discord.ext import commands
from util import jsonParser
import random
import keys

class User(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def ping(self,ctx):
        """PONG!
        """
        await ctx.send('Pong! {0}ms'.format(round(self.bot.latency,3)))

    @commands.command()
    async def hug(self,ctx,arg):
        """Hug someone you like
        """
        link = "https://api.tenor.com/v1/search?q=peach+hug&key={}&limit=6&contentfilter=high".format(keys.TENOR_API)
        gif = random.choice(jsonParser.getJson(link).get("results"))
        url = gif.get("media")[0].get("tinygif").get("url")
        embed = discord.Embed().set_image(url=url)
        embed.add_field(name="HEY!",value="{0} du hast eine Umarmung von {1} bekommen!".format(arg,ctx.author.nick))
        await ctx.send(embed=embed)

def setup(bot):
   bot.add_cog(User(bot))
    