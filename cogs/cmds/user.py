import discord, keys, random, json, requests
from discord.ext import commands
from util import parser
from bs4 import BeautifulSoup




def to_lower(arg):
    return arg.lower()

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
        gif = random.choice(parser.getJson(link).get("results"))
        url = gif.get("media")[0].get("tinygif").get("url")
        embed = discord.Embed().set_image(url=url)
        embed.add_field(name="HEY!",value="{0} du hast eine Umarmung von {1} bekommen!".format(arg,ctx.author.mention))
        await ctx.send(embed=embed)

    @commands.command(name="dog", aliases=["doggo"])
    async def dog(self,ctx, *args: to_lower):
        """Doggo
        \'!dog\' for a random dog
        \'!dog [breed]\' for a picture of a specific breed
        \'!dog [breed-subbreed]\' for a picture of a specific subbreed
        \'!dog list\' for a list of all breeds
        \'!dog list [breed]\' for a list of all subbreeds (written bold in \'list\')
        """
        if len(args) == 0:
            url = parser.getJson("https://dog.ceo/api/breeds/image/random").get("message")
            breed = url.split("/")[4]
            embed = discord.Embed(title=breed.title()).set_image(url=url)
            return await ctx.send(embed=embed)
        if len(args) == 1:
            if not args[0] == "list":
                breed = args[0].replace("-","/")
                jsonO = parser.getJson("https://dog.ceo/api/breed/{}/images".format(breed))
                if jsonO.get("status") == "error":
                    return await ctx.send("Breed not found")
                doggos = jsonO.get("message")
                url = random.choice(doggos)
                embed = discord.Embed(title=args[0].title()).set_image(url=url)
                return await ctx.send(embed=embed)
            else:
                doggoList = parser.getJson("https://dog.ceo/api/breeds/list/all").get("message")
                embed = discord.Embed(title="All the good boys and girls",colour=0x3311AA)
                breeds = " "
                for doggoBreed, subBreed in doggoList.items():
                    if(len(subBreed) > 0):
                        breeds += "**{}** ".format(doggoBreed.title())
                    else:
                        breeds += "{} ".format(doggoBreed.title())
                embed.add_field(name="\u200b",value=breeds)
                return await ctx.send(embed=embed)
        if len(args) == 2:
            response = parser.getJson("https://dog.ceo/api/breed/{}/list".format(args[1]))
            if response.get("status") == "error":
                    return await ctx.send("Breed not found")
            subBreedList = response.get("message")
            if len(subBreedList) <= 0:
                return await ctx.send("No sub-breed for {}".format(args[1].title()))
            embed = discord.Embed(colour=0x3311AA)
            subBreedString = " "
            for subBreed in subBreedList:
                subBreedString += "{} ".format(subBreed.title())
            embed.add_field(name="Sub-Breed: {}".format(args[1].title()),value=subBreedString)
            return await ctx.send(embed=embed)

    @commands.command()
    async def pun(self,ctx):
        """Get a random pun. Very funny.
        Don't do it."""
        data = BeautifulSoup(parser.getHTML("https://pun.me/random/"), 'html.parser').find("ul",{"class":"puns single"}).find('li')
        punID = data.find('a').getText()
        pun = data.getText().replace(punID,"")
        return await ctx.send(pun)

    @commands.command(name="owl", aliases=["eule"])
    async def owl(self,ctx):
        jsonO = parser.getJson("https://pixabay.com/api/?key={}&q=eule&category=animal&per_page=200&image_type=photo".format(keys.PIXABAY_API))
        url = random.choice(jsonO.get('hits')).get('largeImageURL')
        embed = discord.Embed().set_image(url=url).set_footer(text="Image from Pixabay")
        await ctx.send(embed=embed)

    @commands.command()
    async def xkcd(self,ctx,*args):
        """ Xkcd comics
        \'!xkcd\' for the latest xkcd
        \'!xkcd [r|random]\' for a random xkcd
        \'!xkcd [number]\' for a specific xkcd
        """
        if len(args) == 0:
            jsonO = parser.getJson("https://xkcd.com/info.0.json")
            embed = discord.Embed(color=0x633032)
            embed.set_image(url=jsonO.get("img"))
            embed.add_field(name="{} (Nr. {})".format(jsonO.get("title"),jsonO.get("num")),value=jsonO.get("alt"))
            return await ctx.send(embed=embed)
        if len(args) == 1:
            if args[0] == 'r' or args[0] == 'random':
                maxNumber = parser.getJson("https://xkcd.com/info.0.json").get("num")
                jsonO = parser.getJson("https://xkcd.com/{}/info.0.json".format(random.randint(1,maxNumber)))
                embed = discord.Embed(color=0x633032)
                embed.set_image(url=jsonO.get("img"))
                embed.add_field(name="{} (Nr. {})".format(jsonO.get("title"),jsonO.get("num")),value=jsonO.get("alt"))
                return await ctx.send(embed=embed)
            else:
                try:
                    number = int(args[0])
                except ValueError:
                    return await ctx.send("Enter a valid number or an \"r\" for a random xkcd")
                jsonO = parser.getJson("https://xkcd.com/{}/info.0.json".format(number))
                embed = discord.Embed(color=0x633032)
                embed.set_image(url=jsonO.get("img"))
                embed.add_field(name="{} (Nr. {})".format(jsonO.get("title"),jsonO.get("num")),value=jsonO.get("alt"))
                return await ctx.send(embed=embed)

    @commands.command()
    async def smbc(self,ctx, *args):
        """Smbc comics
        \'!smbc\' for the latest smbc 
        \'!smbc [r|random]\' for a random smbc
        """
        if len(args) == 0:
            data = BeautifulSoup(parser.getHTML("https://www.smbc-comics.com/"), "html.parser").find("script",{"type":"application/ld+json"})
            jsonO = json.loads(str(data).replace("<script type=\"application/ld+json\">","").replace("</script>",""))
            embed= discord.Embed(title=jsonO.get("name"))
            embed.set_image(url=jsonO.get("image"))
            return await ctx.send(embed=embed)
        if len(args) == 1:
            if args[0] == "r" or args[0] == "random":
                name = requests.get("https://smbc-comics.com/rand.php").content.decode("utf-8").replace("\"","")
                data = BeautifulSoup(parser.getHTML("https://www.smbc-comics.com/comic/{}".format(name)), "html.parser").find("script",{"type":"application/ld+json"})
                jsonO = json.loads(str(data).replace("<script type=\"application/ld+json\">","").replace("</script>",""))
                embed= discord.Embed(title=jsonO.get("name"),color=0x3e2979)
                embed.set_image(url=jsonO.get("image"))
                return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(User(bot))