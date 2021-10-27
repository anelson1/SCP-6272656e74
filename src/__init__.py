import discord
import os
intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents = intents)
authkey=os.getenv("botkey")
dir = ("src/meme_functionality/images")
CHECK_FOLDER = os.path.isdir(dir)

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(dir)
    os.makedirs(dir+"/output")
else:
    print(dir, "folder already exists.")

from src import functionality

client.run(authkey)
