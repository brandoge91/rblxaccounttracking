import dbmanager

from disnake.ext import tasks, commands

class fetchData(commands.Cog):
    def __init__(self):
        self.fetchData.start()

    def cog_unload(self):
        self.fetchData.cancel()

    @tasks.loop(minutes=5.0)
    async def fetchData():
        print("5 minutes")


def setup(bot):
    bot.add_cog(fetchData(bot))
