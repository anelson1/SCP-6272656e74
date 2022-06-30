"""
Based Bot for meme generation and bool RSVP handling.
"""
import os
import asyncio
import random
import logging
import discord
from discord.ext import commands

from src.meme_functionality import meme
from src.bool_functionality import boolin_package
from src.misc_functionalities import equity_package
from src.misc_functionalities import dead_package
from src.gaming_functionality import game_package
from src.print_functionality import print_package

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
    await bot.change_presence(activity=discord.Game(name="with fate"))

@bot.event
async def on_raw_reaction_add(payload):
    """
    What happens when a reaction is added to a message
    """
    if not payload.user_id == bot.user.id:
        if payload.event_type == "REACTION_ADD":
            try:
                chan = bot.get_guild(payload.guild_id).get_channel(payload.channel_id)
                general_chan = bot.get_guild(payload.guild_id).get_channel(423937254046826498)
                msg = await chan.fetch_message(payload.message_id)
            except:
                print("uh oh")
            if str(payload.emoji) == "✅":
                await boolin_package.bool_rsvp(await bot.fetch_user(payload.user_id), True, bot, True)
            elif str(payload.emoji) == "❌":
                await boolin_package.bool_rsvp(await bot.fetch_user(payload.user_id), False, bot, True)
            elif payload.emoji.id == 807071047169474610:
                user = payload.member
                guild = msg.guild
                await user.add_roles(guild.get_role(974090144451809341))
                embed = discord.Embed(title = user.display_name, description = "is not dead!", color=user.color)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text=guild.name + " | Nelson Net 2022")
                await general_chan.send(embed=embed)
            else:
                code = 0
                for i in range((len(msg.reactions))):
                    if i == 0 and str(msg.reactions[i]) == "😎":
                        code = code + 1
                    if i == 1 and str(msg.reactions[i]) == "😔":
                        code = code + 1
                    if i == 2 and str(msg.reactions[i]) == "😐":
                        code = code + 1
                    if i == 3 and str(msg.reactions[i]) == "😈":
                        code = code + 1
                    if i == 4 and str(msg.reactions[i]) == "🤠":
                        code = code + 1
                if code == 5:
                    await chan.send("Code Accepted. You can now use the Nuclear Option...")
                    f = open("verifieduser.txt","w")
                    f.write(str(payload.user_id))
                    f.close()
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
async def boolin(ctx, *, dateofbool: str):
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
async def confirmbool(ctx, decision: bool):
    """
    Respond to the bool RSVP
    """
    await boolin_package.bool_rsvp(ctx, decision, bot, False)

@confirmbool.error
async def confirmbool_error(ctx, error):
    """
    error handler for confirm function
    """
    await ctx.send(error)

@bot.command()
async def listbool(ctx, annoy=False):
    """
    List everyone who agreed to bool
    """
    await boolin_package.bool_list(ctx, annoy, bot)

@bot.command()
async def game(ctx, *, game:str):
    """
    Send a game request to every member of the 'Gaming' role
    """
    await game_package.game_send(ctx, game)

@game.error
async def game_error(ctx, error):
    """
    error handler for game function
    """
    await ctx.send(error)

@bot.command()
async def confirmgame(ctx, decision: bool):
    """
    Respond to the bool RSVP
    """
    await game_package.game_rsvp(ctx, decision, bot)

@confirmgame.error
async def confirmgame_error(ctx, error):
    """
    error handler for confirm function
    """
    await ctx.send(error)

@bot.command()
async def listgame(ctx, annoy=False):
    """
    List everyone who agreed to play the game
    """
    await game_package.game_list(ctx, annoy, bot)

@bot.command(name="whois")
async def whois(ctx, user: discord.Member):
    """
    Takes the given user and looks up information about them
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
    Returns the given user's 'chat equity'
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
    await ctx.send(
        "https://open.spotify.com/track/2TogYEdCs90G87y97bOILl?si=PbhZGp-QR3SiWzlrRWyYfg")
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
async def randomSound(ctx):
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

    else:
        await ctx.send("https://bit.ly/3komZEQ")

@bot.command()
async def printstatus(ctx):
    """Returns the current status of a print"""
    await print_package.fetch_status(ctx)

@bot.command()
async def nuclear(ctx, user: discord.Member):
    """Ping user relentlessly"""
    f = open("verifieduser.txt", "r")
    if str(ctx.author.id) == str(f.read()):
        await ctx.send("Authorized. Preparing Strike")
        for i in range(69):
            msg = await ctx.send(user.mention)
            await msg.delete()
        f.close()
        f = open("verifieduser.txt", "w")
        f.write("")
        f.close()
    else:
        await ctx.send("You do not have the authorization to use this command...")
        f.close()

@bot.command()
async def dead(ctx):
    await dead_package.dead_check(ctx)

@bot.command()
async def pog(ctx):
    """Sends a Pog"""
    pog_list = [991869057085231195, 777033116107407390, 991872892977557504, 991872896899240017, 991876332952760380,807071047169474610]
    randomEmoji = random.choice((pog_list))
    emoji = ctx.bot.get_emoji(randomEmoji)
    await ctx.send(emoji)

bot.run(authkey)
