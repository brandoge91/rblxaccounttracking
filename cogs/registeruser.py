import disnake
import dbmanager

from roblox import Client
from roblox import UserNotFound
from disnake.ext import commands

robloxClient = Client()

class registeruser(commands.Cog):
    """Register users with the run of a command, not currently role locked."""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register a user for tracking.")
    async def registeruser(
        self,
        inter: disnake.ApplicationCommandInteraction,
        username: str
    ):
        await inter.response.defer(ephemeral=True)
        try:
            user = await robloxClient.get_user_by_username(username)
        except UserNotFound:
            await inter.edit_original_message("Invalid username.")
            return
        NewUser = dbmanager.account(user.id)
        startTracking = NewUser.startTracking()
        await inter.edit_original_message(startTracking)


def setup(bot):
    bot.add_cog(registeruser(bot))
