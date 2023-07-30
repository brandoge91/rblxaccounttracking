"""Command that allows to begin the tracking of peope."""
from roblox import Client
from roblox import UserNotFound
from disnake.ext import commands

import disnake
import dbmanager


robloxClient = Client()


class RegisterUser(commands.Cog):
    """Sets up Register User command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register a user for tracking.")
    async def registeruser(
        self,
        inter: disnake.ApplicationCommandInteraction,
        username: str
    ):
        """Registration logic."""
        await inter.response.defer(ephemeral=True)
        try:
            user = await robloxClient.get_user_by_username(username)
        except UserNotFound:
            await inter.edit_original_message("Invalid username.")
            return
        new_user = dbmanager.Account(user.id)
        start_tracking = new_user.start_tracking()
        await inter.edit_original_message(start_tracking)


def setup(bot):
    """Adds cog to bot."""
    bot.add_cog(RegisterUser(bot))
