"""
Based Bot for meme generation and bool RSVP handeling.
"""
from datetime import datetime
from src.misc_functionalities import equity_package, boowomp_package
from src.meme_functionality import meme
from src.bool_functionality import bool
from discord.ext import commands
import discord
import os
import asyncio

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='?', description="A bot to rival the all powerfull", intents=intents)

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
    game = discord.Game("with your emotions")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Booting up...")
    print("Booted! Welcome to Based Bot")


@bot.command()
async def shitpost(ctx, caption):
    """
    Creates a meme from the given text
    """
    await meme.shitpost(ctx, caption)

@shitpost.error
async def shitpost_error(ctx, error):
    """
    Error handler for the shitposting function
    """
    await ctx.send("You need to provide a caption")

@bot.command()
async def bool(ctx, dateofbool):
    """
    Send a RSVP to bool to every member of the 'boolin' role
    """
    await bool.bool_send(ctx, dateofbool)

@bool.error
async def bool_error(ctx, error):
    """
    error handler for bool function
    """
    await ctx.send("Please provide a date")

@bot.command()
async def listbool(ctx):
    """
    List everyone who agreed to bool
    """
    await bool.bool_list(ctx)

@bot.command()
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
    await ctx.send("Please provide a valid user")

@bot.command()
async def equity(ctx, user):
    """
    Returns the users 'chat equity'
    """
    await equity_package.angelo(ctx, user)

@equity.error
async def equity_error(ctx, error):
    """
    Error handler for equity function
    """
    await ctx.send("Please provide a valid user")

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
    await equity_package.specificangelo(ctx, word)

@specificword.error
async def specificword_error(ctx, error):
    """
    Error handler for the specificword function
    """
    await ctx.send("Please provide a valid string")

@bot.command()
async def rainbow(ctx):
    """
    Randomly give one person in the server a rainbow name (Warning: May get the bot banned for abuse of the API)
    """
    await rainbow.rainbow(ctx)

@bot.command()
async def based(ctx):
    """
    Sends the song 'based' by The Symposium in the active voice channel of the function caller
    """
    ctx.send("https://open.spotify.com/track/2TogYEdCs90G87y97bOILl?si=PbhZGp-QR3SiWzlrRWyYfg")
    VC = ctx.message.author.voice.channel
    connection = await VC.connect(timeout=10)
    connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/based/based.mp3"))
    while connection.is_playing():
        await asyncio.sleep(.1)
    await connection.disconnect()

@bot.command()
async def boowomp(ctx):
    """
    It's boowomp, it plays when they are sad
    """
    try:
        VC = ctx.author.voice.channel
        connection = await VC.connect(timeout=10)
        connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/boowomp/boowomp.mp3"))
        while connection.is_playing():
            await asyncio.sleep(.1)
        await connection.disconnect()
    except:
        await ctx.send("https://preview.redd.it/wkhqf50prmo61.png?auto=webp&s=7bd8f272554971443adefae53037a7895c1a2fbd")


@bot.command()
async def random(ctx):
    """
    Plays 1 hour of silence broken up by random sounds in the callers voice channel
    """
    try:
        VC = ctx.author.voice.channel
        connection = await VC.connect(timeout=10)
        connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/boowomp/random.mp3"))
        while connection.is_playing():
            await asyncio.sleep(.1)
        await connection.disconnect()
    except:
        await ctx.send("https://preview.redd.it/wkhqf50prmo61.png?auto=webp&s=7bd8f272554971443adefae53037a7895c1a2fbd")


# What happens upon receiving a message
@bot.event
async def on_message(message):
    try:
        # Commands to be performed within a DM
        if(type(message.channel) == discord.channel.DMChannel):
            await bool.bool_RSVP(message, bot)
        # Commands to be performed within a server channel
        else:
            # On every message sent, check to see if it should become a meme
            await meme.roulette(message)

            # Sends the song 'based' in chat any time the word based is said then tries to join a voice call and plays the song
            if "Based" in message.content:
                await based.send(False, message)

    except Exception as e:
        print(e)
        await bot.get_channel(875459781958197318).send(str(e) + " has occured at " + str(datetime.now()))

bot.run(authkey)
