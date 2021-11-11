"""
Based Bot for meme generation and bool RSVP handeling.
"""
import os
import asyncio
import logging
import discord
from discord.ext import commands

from src.meme_functionality import meme
from src.bool_functionality import boolin_package
from src.misc_functionalities import equity_package

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
DESC = "A bot to rival The All Powerful"
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                   description=DESC,
                   intents=intents)

authkey = os.getenv("botkey")
IMGDIR = ("src/meme_functionality/images")
CHECK_FOLDER = os.path.isdir(IMGDIR)

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(IMGDIR)
    os.makedirs(IMGDIR+"/output")
else:
    print(IMGDIR, "folder already exists.")


# What happens upon start up
@bot.event
async def on_ready():
    """
    What happens upon booting up the bot
    """
    print("Booting up...")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("Booted! Welcome to Based Bot")
    await bot.change_presence(activity=discord.Game(name="with fate | use !help to get started"))

@bot.command()
async def shitpost(ctx, *, caption: str):
    """
    Creates a meme from the given text
    """
    await meme.shitpost(ctx, caption)

@shitpost.error
async def shitpost_error(ctx, error):
    """
    Error handler for the shitposting function
    """
    await ctx.send(error)

@bot.command(name='bool')
async def boolin(ctx, dateofbool):
    """
    Send a RSVP to bool to every member of the 'boolin' role
    """
    await boolin_package.bool_send(ctx, dateofbool)

@boolin.error
async def boolin_error(ctx, error):
    """
    error handler for bool function
    """
    await ctx.send(error)

@bot.command()
async def listbool(ctx):
    """
    List everyone who agreed to bool
    """
    await boolin_package.bool_list(ctx)

@bot.command(name="whois")
async def whois(ctx, user: discord.Member):
    """
    Function to look up a user and display their info
    """
    embed = discord.Embed(title = user.display_name, color=user.color)
    embed.add_field(name="Full Tag:", value=user)
    embed.add_field(name="Currently Playing:", value=user.activity)
    embed.add_field(name="Status:", value=user.status.value)
    embed.add_field(name="Joined on:", value=user.joined_at.strftime('%m/%d/%y'))
    embed.add_field(name="Top Role:", value=user.top_role)
    embed.add_field(name="ID:", value=str(user.id))
    embed.add_field(name="Account created on:", value=user.created_at.strftime('%m/%d/%y'))
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text=ctx.guild.name + " | Copywrite Nelson Net 2021")
    await ctx.send(embed=embed)

@whois.error
async def whois_error(ctx, error):
    """
    Error handler for whois function
    """
    await ctx.send(error)

@bot.command()
async def equity(ctx, user: discord.Member):
    """
    Returns the users 'chat equity'
    """
    await equity_package.equity(ctx, user)

@equity.error
async def equity_error(ctx, error):
    """
    Error handler for equity function
    """
    await ctx.send(error)

@bot.command()
async def totalequity(ctx):
    """
    Returns the equity for every user in the channel
    """
    await equity_package.bigangelo(ctx)

@bot.command()
async def specificword(ctx, word: str):
    """
    Returns the amount of times the user has said the given word
    """
    await equity_package.specificword(ctx, word)

@specificword.error
async def specificword_error(ctx, error):
    """
    Error handler for the specificword function
    """
    await ctx.send(error)

@bot.command()
async def rainbow(ctx):
    """
    Randomly give one person in the server a rainbow name
    """
    await rainbow.rainbow(ctx)

@bot.command()
async def based(ctx):
    """
    Plays the song 'based' in a voice channel
    """
    ctx.send("https://open.spotify.com/track/2TogYEdCs90G87y97bOILl?si=PbhZGp-QR3SiWzlrRWyYfg")
    voice_channel = ctx.message.author.voice.channel
    connection = await voice_channel.connect(timeout=10)
    connection.play(discord.FFmpegPCMAudio(
        executable="/usr/bin/ffmpeg",
        source="src/misc_functionalities/based/based.mp3"
        ))
    while connection.is_playing():
        await asyncio.sleep(.1)
    await connection.disconnect()

@bot.command()
async def boowomp(ctx):
    """
    It's boowomp, it plays when they are sad
    """
    voice_channel = ctx.author.voice
    if voice_channel:
        voice_channel = voice_channel.channel
        connection = await voice_channel.connect(timeout=10)
        connection.play(discord.FFmpegPCMAudio(
            executable="/usr/bin/ffmpeg",
            source="src/misc_functionalities/boowomp/boowomp.mp3"
            ))
        while connection.is_playing():
            await asyncio.sleep(.1)
        await connection.disconnect()
    else:
        await ctx.send("https://bit.ly/3komZEQ")


@bot.command()
async def random(ctx):
    """
    Plays a unique audio in voice
    """
    voice_channel = ctx.author.voice
    if voice_channel:
        voice_channel = voice_channel.channel
        connection = await voice_channel.connect(timeout=10)
        connection.play(discord.FFmpegPCMAudio(
            executable="/usr/bin/ffmpeg",
            source="src/misc_functionalities/boowomp/random.mp3"
            ))
        while connection.is_playing():
            await asyncio.sleep(.1)
        await connection.disconnect()
    else:
        await ctx.send("https://bit.ly/3komZEQ")

bot.run(authkey)
