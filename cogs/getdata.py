"""Gets tracking data"""
from datetime import datetime
from roblox import Client
from roblox import UserNotFound
from disnake.ext import commands

import disnake
import dbmanager


robloxClient = Client()


class GetData(commands.Cog):
    """Sets up get data command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Register a user for tracking.")
    async def get_data(
        self,
        inter: disnake.ApplicationCommandInteraction,
        username: str
    ):
        """Get Data command logic"""
        await inter.response.defer()
        try:
            user = await robloxClient.get_user_by_username(username)
        except UserNotFound:
            await inter.edit_original_message("Invalid username.")
            return
        new_user = dbmanager.Account(user.id)
        data = new_user.get_data_main()
        if data is None:
            await inter.edit_original_message("This user has no data recorded.")
            return
        embed = disnake.Embed(
            title="Users Recorded Data",
            description="Here is all of the users recorded data."
        )
        embed.add_field("Total Minutes", round(data["minutesPlayed"]))
        embed.add_field("Last location", data["lastLocation"])
        embed.add_field(
            "Last Online",
            datetime.strptime(data["lastOnline"],
            "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y/%m/%d %H:%M UTC"))
        user_presence_type = data["userPresenceType"]
        if user_presence_type == 2 and data["universeId"] is not None:
            universe = await robloxClient.get_universe(data["universeId"])
            started_playing = new_user.get_data()["startedplaying"]
            embed.add_field(name="Currently Playing", value=universe.name)
            embed.add_field(name="Started Playing", value=f"<t:{int(started_playing)}:R>")
        embed.set_thumbnail(url=f"https://thumbs.metrik.app/headshot/{user.id}")
        await inter.edit_original_message(embed=embed)


def setup(bot):
    """Adds cog to bot."""
    bot.add_cog(GetData(bot))
