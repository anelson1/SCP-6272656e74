import discord
import os
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
authkey=os.getenv("botkey")

from src import functionality

client.run(authkey)
