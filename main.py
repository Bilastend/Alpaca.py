import discord,keys, traceback
from datetime import datetime, date
from discord.ext import commands

prefix = keys.PREFIX
bot = commands.Bot(command_prefix=prefix)

extensions = ['cogs.cmds.user','cogs.cmds.admin','cogs.cmds.music']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            traceback.print_exc()
        else:
            print("Loaded {0}".format(extension))

@bot.event
async def on_ready():
    current_time = "{0} {1}".format(date.today(),datetime.now().strftime("%H:%M:%S"))
    print("Logged in as {0} on {1}".format(bot.user,current_time))

@bot.event
async def on_connect():
      await bot.change_presence(activity=discord.Game(name='Nervt nicht.'), status=discord.Status.online)

bot.run(keys.CLIENT_TOKEN)