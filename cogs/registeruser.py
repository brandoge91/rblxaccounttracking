import disnake
import dbmanager
from disnake.ext import commands


class registeruser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register a user for tracking.")
    async def registeruser(self, inter: disnake.ApplicationCommandInteraction, userid: int):
        await inter.response.defer(ephemeral=True)
        NewUser = dbmanager.user(userid)
        NewUser.writeData(minutes=0, lastOnline="0000-00-00T00:00:00.0Z", lastLocation="Unknown")
        await inter.edit_original_message(f"We're now tracing {userid}!")


def setup(bot):
    bot.add_cog(registeruser(bot))
