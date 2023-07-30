import disnake
from disnake.ext import commands, tasks

class PresenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_presence.start()

    def get_server_count(self):
        return len(self.bot.guilds)

    @tasks.loop(minutes=10)
    async def update_presence(self):
        server_count = self.get_server_count()
        activity_name = f"Account Tracking | {server_count} servers"
        await self.bot.change_presence(activity=disnake.Activity(name=activity_name))

    @update_presence.before_loop
    async def before_update_presence(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(PresenceCog(bot))
