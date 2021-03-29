import discord
import random
import os
#import opuslib
import nacl
import ffmpeg
import asyncio
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
authkey=os.getenv("botkey")
m_list =open('mlist.txt').readlines()
r_list = open('rlist.txt').readlines()

@client.event
async def on_ready():
    print("Ni-")


@client.event
async def on_message(message):
    role = message.guild.get_role(message.author.top_role.id)
    if message.author == client.user:
        return
    if message.content == "!rr":
        users = message.guild.members
        num = random.randint(0,len(users))
        color = users[num].color
        role = message.guild.get_role(users[num].top_role.id)
        if role.permissions.administrator:
            print("is admin")
            role = message.guild.get_role(users[num].roles[-2].id)
            await  message.channel.send(str(users[num]) + "is now based!")
            await colorChange(role, color)
        else:
            await  message.channel.send(str(users[num]) + "is now based!")
            await colorChange(role, color)
    elif "!rainbow" in message.content:
        color = message.author.color
        if not role.permissions.administrator:
            await  message.channel.send("Hello! " + str(message.author.nick) + ", you're now based!")
            await colorChange(role, color)
        else:
            print("is admin")
            role = message.guild.get_role(message.author.roles[-2].id)
            print("Role is : " + str(role))
            await  message.channel.send("@" + str(message.author) + "is based!")
            await colorChange(role, color)
            print("Done")
    if message.content == "!palu":
        emoji = discord.utils.get(client.emojis, name = "beamend")
        await message.channel.send(emoji)
        for i in range(random.randint(0,10)):
            await message.channel.send(discord.utils.get(client.emojis, name = "beam"))
        await message.channel.send(discord.utils.get(client.emojis, name = "palu2"))
        await message.channel.send(discord.utils.get(client.emojis, name = "palu1"))
    if message.content == "!brian":
        print(message.guild.roles)
        m_word = random.choice(m_list)
        r_word = random.choice(r_list)
        await message.channel.send(m_word + r_word)
    if "based" in message.content:
        await message.channel.send("https://open.spotify.com/track/2TogYEdCs90G87y97bOILl?si=PbhZGp-QR3SiWzlrRWyYfg")
        try:
            VC = message.author.voice.channel
            connection = await VC.connect(timeout = 10)
            connection.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="shortbased.mp3"))
            while connection.is_playing():
                await asyncio.sleep(.1)
            await connection.disconnect()
        except:
            print("not in call")
    if message.content == "!Based":
        try:
            VC = message.author.voice.channel
            connection = await VC.connect(timeout = 10)
            connection.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="based.mp3"))
            while connection.is_playing():
                await asyncio.sleep(.1)
            await connection.disconnect()
        except:
            await message.channel.send("Try being in a voice call next time dumbass")       
    if message.content == "end" and role.permissions.administrator:
        print("Bye")
        exit(0)

async def colorChange(role, color):
    r = 255
    g = 0
    b = 0
    for i in range(100):
        print(r, g ,b)
        if r == 255 and b == 0 and g != 255:
            g+=51
        elif g == 255 and r != 0:
            r-=51
        elif g == 255 and b != 255:
            b+=51
        elif b==255 and g != 0:
            g-=51
        elif b == 255 and r != 255:
            r+=51
        elif r==255 and b != 0:
            b-=51
        await role.edit(colour = discord.Color.from_rgb(r,g,b))
    await role.edit(colour=color)



client.run(authkey)
