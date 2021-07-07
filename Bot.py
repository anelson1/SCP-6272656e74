import discord
import random
import os
#import opuslib
import nacl
import ffmpeg
import asyncio
import cv2
import numpy as np
import meme
import json
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)
authkey=os.getenv("botkey")
m_list =open('mlist.txt').readlines()
r_list = open('rlist.txt').readlines()
MAIN_SERVER_ID = 423937254046826496
GENERAL_ID = 423937254046826498
DEV_CHAN_ID = 636978333426384906
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
    image = "images/"+str(random.randint(1,len(numimages)))+'.png'
    meme.make_meme(text1, text2,image)
@client.event
async def on_ready():
    game = discord.Game("a dangerous game")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("Ready for Gaming")

@client.event
async def on_message(message):
    #try:
        if(type(message.channel) == discord.channel.DMChannel):
            if message.content == "!Y" or message.content == "!N":
                if message.content == "!Y":
                    dict = {str(message.author):"Yes"}
                    await message.channel.send("You agreed to bool!")
                    await client.get_channel(GENERAL_ID).send(str(message.author) + " has agreed to bool!")
                if message.content == "!N":
                    dict = {str(message.author):"No"}
                    await message.channel.send("You turned down the offer to bool.")
                    await client.get_channel(GENERAL_ID).send(str(message.author) + " has turned down the offer to bool!")
                invnum = open("invnum.txt").read()
                try:
                    myfile = open(invnum+".json", "r+")
                except:
                    myfile = open(invnum+".json", "w+")
                content = myfile.read()
                myfile.close()
                print(content)
                print(invnum+".json")
                try:
                    myjson = json.loads(content)
                    myjson.update(dict)
                    print(myjson)
                    jsonString = json.dumps(myjson)
                except Exception as e:
                    print(e)
                    jsonString = json.dumps(dict)
                myfile1 = open(invnum+".json", "w+")
                myfile1.write(jsonString)
                myfile1.close()
        else:
            check = random.randint(1,100)
            print("Random Number is: " + str(check))
            if check == 1:
                shitpost(message.content)   
                await message.channel.send(file=discord.File('temp.png')) 
            if message.author == client.user:
                return
            if "!shitpost" in message.content:
                text = message.content[10::]
                msg = await message.channel.send("Beginning Shitpost...")
                shitpost(text)
                await msg.delete()
                await message.channel.send(file=discord.File('temp.png')) 

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
                role = message.guild.get_role(users[num].top_role.id)
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
            if "!bool" in message.content:
                if message.author.id != 213559733758459905:
                    await message.channel.send("For security reasons, only Angelo can initate this command.")
                else:
                    await message.channel.send("Sending invites...")
                    param = message.content[6::]
                    role = message.guild.get_role(760375992513724426)
                    invitenumber = open("invnum.txt", "r").read()
                    newinvitenumber = open("invnum.txt", "w+")
                    newinvitenumber.write(str(int(invitenumber) + 1))
                    newinvitenumber.close()
                    for member in role.members:
                        if member.dm_channel == None:
                            chan = await member.create_dm()
                        else:
                            chan = member.dm_channel
                        await chan.send(str(message.author) + " would like to bool on " + str(param) + ". Please respond with !Y for yes or !N for no.")    
            if message.content == "!listbool":
                invnum = open("invnum.txt", "r").read()
                boolers = open(invnum+".json", "r")
                booldict = json.load(boolers)
                string = "So far: "
                for k,v in booldict.items():
                    if v == "Yes":
                        string+= k + ", "
                string += "has agreed to bool"
                await message.channel.send(string)


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
