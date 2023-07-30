import disnake
import dbmanager
from disnake.ext import commands


class registeruser(commands.Cog):
    """Register users with the run of a command, not currently role locked."""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register a user for tracking.")
    async def registeruser(
        self,
        inter: disnake.ApplicationCommandInteraction,
        userid: int
    ):
        await inter.response.defer(ephemeral=True)
        NewUser = dbmanager.account(userid)
        startTracking = NewUser.startTracking()
        await inter.edit_original_message(NewUser)


def setup(bot):
    bot.add_cog(registeruser(bot))
