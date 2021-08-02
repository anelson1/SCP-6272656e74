from src import discord
import asyncio

async def send(long, message):
    if not long:
        await message.channel.send("https://open.spotify.com/track/2TogYEdCs90G87y97bOILl?si=PbhZGp-QR3SiWzlrRWyYfg")
    try:
        VC = message.author.voice.channel
        connection = await VC.connect(timeout=10)
        if not long:
            connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/based/shortbased.mp3"))
        else:
            connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/based/based.mp3"))
        while connection.is_playing():
            await asyncio.sleep(.1)
        await connection.disconnect()
    except:
        print("not in call")
