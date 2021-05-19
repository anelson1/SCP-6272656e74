import discord
import random
import os
#import opuslib
import nacl
import ffmpeg
import asyncio
import cv2
import numpy as np
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
authkey=os.getenv("botkey")
m_list =open('mlist.txt').readlines()
r_list = open('rlist.txt').readlines()
def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=5)
        new_width = textSize[0][0]
        #print(new_width)
        if (new_width <= width):
            return scale/10
    return 1
def find_space(text):
    midpoint = int(len(text)/2)
    print(midpoint, text[midpoint])
    if text[midpoint] != ' ':
        for i in text[int(len(text)/2)::]:
            print(i)
            if i == ' ':
                return midpoint
            midpoint+=1
    return midpoint
def shitpost(message):
    text = message
    midpoint = find_space(text)
    text1 = text[0:midpoint]
    text2 = text[midpoint+1::]
    numimages = os.listdir("images")
    image = cv2.imread("images/"+str(random.randint(1,len(numimages)))+'.png', cv2.IMREAD_UNCHANGED)
    height = image.shape[0]
    width = image.shape[1]
    if height < width:
        landscape = True
    fontscale1 = get_optimal_font_scale(text1,width)
    fontscale2 = get_optimal_font_scale(text2,width)
    textsize1 = cv2.getTextSize(text1,cv2.FONT_HERSHEY_DUPLEX,fontscale1,5)
    textwidth1 = textsize1[0][0]
    textheight1 = textsize1[0][1]
    textsize2 = cv2.getTextSize(text2,cv2.FONT_HERSHEY_DUPLEX,fontscale2,5)
    textwidth2 = textsize2[0][0]
    textheight2 = textsize2[0][1]
    cv2.putText(image, text1,(int((width/2)-(textwidth1/2)),(int((height/10) - (textheight1/10)))+int(1.1*textsize1[1])),cv2.FONT_HERSHEY_DUPLEX,fontscale1,(0,0,0,255),10)
    cv2.putText(image, text1,(int((width/2)-(textwidth1/2)),(int((height/10) - (textheight1/10)))+int(1.1*textsize1[1])),cv2.FONT_HERSHEY_DUPLEX,fontscale1,(255,255,255,255),2)
    cv2.putText(image, text2,(int((width/2)-(textwidth2/2)),(int((8.5*height/10) + (8.5*textheight2/10)))-int(textsize2[1])),cv2.FONT_HERSHEY_DUPLEX,fontscale2,(0,0,0,255),10)
    cv2.putText(image, text2,(int((width/2)-(textwidth2/2)),(int((8.5*height/10) + (8.5*textheight2/10)))-int(textsize2[1])),cv2.FONT_HERSHEY_DUPLEX,fontscale2,(255,255,255,255),2)
    cv2.imwrite('output.png', image)
@client.event
async def on_ready():
    print("Ni-")


@client.event
async def on_message(message):
    check = random.randint(1,100)
    print("Random Number is: " + str(check))
    if check == 1:
        shitpost(message.content)   
        await message.channel.send(file=discord.File('output.png')) 
    role = message.guild.get_role(message.author.top_role.id)
    if message.author == client.user:
        return
    if "!shitpost" in message.content:
        text = message.content[10::]
        shitpost(text)
        await message.channel.send(file=discord.File('output.png')) 

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
