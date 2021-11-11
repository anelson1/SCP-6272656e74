import discord
import asyncio

async def send(long, message, random):
    try:
        VC = message.author.voice.channel
        connection = await VC.connect(timeout=10)
        if random:
            connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/boowomp/random.mp3"))
        elif not long:
            connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/boowomp/boowomp.mp3"))
        else:
            connection.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="src/misc_functionalities/boowomp/boowomp1hr.mp3"))
        while connection.is_playing():
            await asyncio.sleep(.1)
        await connection.disconnect()
    except:
        await message.channel.send("https://preview.redd.it/wkhqf50prmo61.png?auto=webp&s=7bd8f272554971443adefae53037a7895c1a2fbd")
