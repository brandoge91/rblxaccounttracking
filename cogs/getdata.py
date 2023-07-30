import disnake
import dbmanager

from roblox import Client
from roblox import UserNotFound
from disnake.ext import commands

robloxClient = Client()

class getdata(commands.Cog):
    """Gets and returns data"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register a user for tracking.")
    async def getdata(
        self,
        inter: disnake.ApplicationCommandInteraction,
        username: str
    ):
        await inter.response.defer()
        try:
            user = await robloxClient.get_user_by_username(username)
        except UserNotFound:
            await inter.edit_original_message("Invalid username.")
            return
        NewUser = dbmanager.account(user.id)
        data = NewUser.getData()
        if data is None:
            await inter.edit_original_message("This user has no data recorded.")
            return
        embed = disnake.Embed(
            title="Users Recorded Data",
            description="Here is all of the users recorded data."
        )
        embed.add_field("Total Hours", data["hoursPlayed"])
        embed.add_field("Last location", data["lastLocation"])
        embed.add_field("Last Online", data["lastOnline"])
        embed.set_thumbnail(url=f"https://thumbs.metrik.app/headshot/{user.id}")
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(getdata(bot))
