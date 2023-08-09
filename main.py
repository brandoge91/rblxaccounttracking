"""Starts discord bot."""
import os
import disnake
from disnake.ext import commands


intent = disnake.Intents.default()
bot = commands.InteractionBot(intents=intent)
bot.persistent_views_added = False

bot.load_extensions("./cogs")


bot.run(os.getenv("botToken"))
