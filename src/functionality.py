from src import discord, client
from src.bool_functionality import bool
from src.meme_functionality import meme
from src.misc_functionalities import rainbow, brian, based, palu, angelo, boowomp, whois
from datetime import datetime
from src.misc_functionalities.helper import ping_to_id

import random
import os
import nacl
import ffmpeg
import asyncio
import json
import re


# What happens upon start up
@client.event
async def on_ready():
    game = discord.Game("a dangerous game")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("Booting up...")
    print("Booted! Welcome to Based Bot")

# What happens upon receiving a message


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        # Commands to be performed within a DM
        if(type(message.channel) == discord.channel.DMChannel):
            await bool.bool_RSVP(message)
        # Commands to be performed within a server channel
        else:
            # On every message sent, check to see if it should become a meme
            await meme.roulette(message)

            # Creates a meme from the given text
            if "!shitpost" in message.content:
                await meme.shitpost(message, was_random=False)

            # Randomly give one person in the server a rainbow name (Warning: May get the bot banned for abuse of the API)
            if message.content == "!rr":
                await rainbow.rainbow(message)

            # Generate an emoji of palutena with random height
            if message.content == "!palu":
                await palu.generate_emoji(message)

            # Generate 2 words. One starting with M and one ending with R
            if message.content == "!brian":
                await brian.generate_words(message)

            # Sends the song 'based' in chat any time the word based is said then tries to join a voice call and plays the song
            if "Based" in message.content:
                await based.send(False, message)

            # Joins voice call of message author and plays the whole song 'based'
            if message.content == "!Based":
                await based.send(True, message)

            # Send a RSVP to bool to every member of the 'boolin' role
            if "!bool" in message.content:
                await bool.bool_send(message)

            # List everyone who agreed to bool
            if message.content == "!listbool":
                await bool.bool_list(message)

            # Returns the "chat equity" of a given user
            if message.content[0:7] == "!equity":
                id = ping_to_id(message.content)
                await angelo.angelo(message, id)

            # Returns the chat equity of every user for a channel
            if message.content == "!bigequity":
                await angelo.bigangelo(message)

            # Plays boowomp
            if message.content == "boowomp":
                await boowomp.send(False, message, False)

            # Plays 1 hour of silence broken up by boowomp
            if message.content == "!boowomp":
                await boowomp.send(True, message, False)

            # Plays 1 hour of silence broken up by random sounds
            if message.content == "!random":
                await boowomp.send(False, message, True)

            # Checks for a specific word
            if "!specificword" in message.content:
                await angelo.specificangelo(message, message.content[16::])
                
            # Displays whois info about the user
            if "!whois" in message.content:
                await whois.whois(message, ping_to_id(message.content))

    except Exception as e:
        print(e)
        await client.get_channel(875459781958197318).send(str(e) + " has occured at " + str(datetime.now()))
