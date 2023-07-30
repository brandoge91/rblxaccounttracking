import requests
import time
import os
import dotenv
import json
import dbmanager

from disnake.ext import tasks, commands

env = dotenv.load_dotenv()


class fetchData(commands.Cog):
    """Fetches data perodically."""

    def __init__(self, bot):
        self.bot = bot
        self.fetchData.start()

    def cog_unload(self):
        self.fetchData.cancel()

    @tasks.loop(minutes=1)
    async def fetchData(self):
        userIds = [user["userId"] for user in dbmanager.getAllTrackableUsers()]

        session = requests.Session()
        session.cookies[".ROBLOSECURITY"] = os.getenv("botCookie")
        response = session.post(
            "https://presence.roblox.com/v1/presence/users",
            data=json.dumps({"userIds": userIds}),
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        userPresencesData = response.json()["userPresences"]

        for userPresence in userPresencesData:
            userId = userPresence["userId"]
            account = dbmanager.account(userId)
            currentAccountData = account.getData()
            userPresenceType = userPresence["userPresenceType"]
            if not currentAccountData["playing"] and userPresenceType == 2:
                MainData = account.getDataMain()
                minutes = MainData["minutesPlayed"] if MainData else 0
                account.writeData({"playing": True, "startedplaying": time.time()})
            elif currentAccountData["playing"] and userPresenceType != 2:
                account.writeData({"playing": False})
                MainData = account.getDataMain()
                minutes = ((time.time() - currentAccountData["startedplaying"]) / 60) + MainData["minutesPlayed"]
            else:
                MainData = account.getDataMain()
                minutes = MainData["minutesPlayed"] if MainData else 0

            account.writeDataMain({
                "lastLocation": userPresence["lastLocation"],
                "lastOnline": userPresence["lastOnline"],
                "userPresenceType": userPresenceType,
                "universeId": userPresence["universeId"],
                "minutesPlayed": minutes
            })


def setup(bot):
    bot.add_cog(fetchData(bot))
