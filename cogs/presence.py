import disnake
from disnake.ext import commands


class PresenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_server_count(self):
        return len(self.bot.guilds)

    @commands.Cog.listener()
    async def on_ready(self):
        server_count = self.get_server_count()
        activity_name = f"Account Tracking | {server_count} servers"
        await self.bot.change_presence(
            activity=disnake.Activity(
                name=activity_name
            )
        )


def setup(bot):
    bot.add_cog(PresenceCog(bot))
