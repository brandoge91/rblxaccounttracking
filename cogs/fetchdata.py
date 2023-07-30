"""Fetches data periodically and uploads to database."""
import json
import time
import os

from disnake.ext import tasks, commands

import requests
import dotenv
import dbmanager


ENV = dotenv.load_dotenv()


class FetchData(commands.Cog):
    """Sets up fetch data task"""
    def __init__(self, bot):
        self.bot = bot
        self.fetch_data.start()

    def cog_unload(self):
        self.fetch_data.cancel()

    @tasks.loop(minutes=1)
    async def fetch_data(self):
        """Fetches data every minute and performs logic based of that"""
        user_ids = [user["userId"] for user in dbmanager.get_all_trackable_users()]

        session = requests.Session()
        session.cookies[".ROBLOSECURITY"] = os.getenv("botCookie")
        response = session.post(
            "https://presence.roblox.com/v1/presence/users",
            data=json.dumps({"userIds": user_ids}),
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        user_presences_data = response.json()["userPresences"]

        for user_presence in user_presences_data:
            user_id = user_presence["userId"]
            account = dbmanager.Account(user_id)
            current_account_data = account.get_data()
            user_presence_type = user_presence["userPresenceType"]
            if not current_account_data["playing"] and user_presence_type == 2:
                main_data = account.get_data_main()
                minutes = main_data["minutesPlayed"] if main_data else 0
                account.write_data({"playing": True, "startedplaying": time.time()})
            elif current_account_data["playing"] and user_presence_type != 2:
                account.write_data({"playing": False})
                main_data = account.get_data_main()
                minutes = (
                (time.time() - current_account_data["startedplaying"]) / 60
                ) + main_data["minutesPlayed"]
            else:
                main_data = account.get_data_main()
                minutes = main_data["minutesPlayed"] if main_data else 0

            account.write_data_main({
                "lastLocation": user_presence["lastLocation"],
                "lastOnline": user_presence["lastOnline"],
                "userPresenceType": user_presence_type,
                "universeId": user_presence["universeId"],
                "minutesPlayed": minutes
            })


def setup(bot):
    """Adds task as a cog to bot"""
    bot.add_cog(FetchData(bot))
