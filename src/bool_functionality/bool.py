from src.constants import MAIN_SERVER_ID, GENERAL_ID, DEV_CHAN_ID, BOOL_ROLE_ID, DEV_ROLE_ID
import discord
import json
from datetime import datetime, time

# Parse message and update JSON file with name and RSVP Status
async def bool_RSVP(message, client):
    if message.content == "!Y" or message.content == "!N":
        if message.content == "!Y":
            dict = {str(message.author): "Yes"}
            await message.channel.send("You agreed to bool!")
            embed = discord.Embed(title=message.author, description="Has agreed to bool!", color=discord.Colour.green())
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Copyright Nelson Net 2021")
            await client.get_channel(GENERAL_ID).send(embed = embed)
        if message.content == "!N":
            dict = {str(message.author): "No"}
            embed = discord.Embed(title=message.author, description="Has turned down the offer to bool!", color=discord.Colour.red())
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Copyright Nelson Net 2021")
            await client.get_channel(GENERAL_ID).send(embed = embed)
        invnum = open("src/bool_functionality/invnum.txt").read()
        try:
            myfile = open("src/bool_functionality/"+invnum+".json", "r+")
        except:
            myfile = open("src/bool_functionality/"+invnum+".json", "w+")
        content = myfile.read()
        myfile.close()
        try:
            myjson = json.loads(content)
            myjson.update(dict)
            jsonString = json.dumps(myjson)
        except Exception as e:
            jsonString = json.dumps(dict)
        myfile1 = open("src/bool_functionality/"+invnum+".json", "w+")
        myfile1.write(jsonString)
        myfile1.close()
    else:
        await message.channel.send("Please enter !Y or !N please")
        
        
# Send RSVPs to bool


async def bool_send(message):
    current_time = datetime.now().strftime("%H:%M:%S")
    current_day = datetime.now().strftime("%m/%d/%y")
    embed = discord.Embed(title="Bool RSVP", description="Asking the fellas to bool", color=message.author.color)
    embed.add_field(name = "Bool invites", value="Have been sent by " + message.author.nick + " on " +  current_day + " at " + current_time)
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.set_footer(text="Copyright Nelson Net 2021 | " + message.guild.name)
    await message.channel.send(embed = embed)
    param = message.content[6::]
    datefile = open("src/bool_functionality/booldate.txt", "w+")
    datefile.write(param)
    datefile.close()
    role = message.guild.get_role(BOOL_ROLE_ID)
    try:
        invitenumber = open("src/bool_functionality/invnum.txt", "r").read()
    except:
        invitenumber = open("src/bool_functionality/invnum.txt", "w+").read()
        invitenumber = 0
    newinvitenumber = open("src/bool_functionality/invnum.txt", "w+")
    newinvitenumber.write(str(int(invitenumber) + 1))
    newinvitenumber.close()
    for member in role.members:
        chan = await member.create_dm()
        embed = discord.Embed(title="Bool RSVP", description="Asking the fellas to bool", color=message.author.color)
        embed.add_field(name = str(message.author), value = "Would like to bool on " + str(param) + ". Please respond with !Y for yes or !N for no.")
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021 | " + message.guild.name)
        await chan.send(embed = embed)
           
            
# List people who have RSVPed to bool


async def bool_list(message):
    invnum = open("src/bool_functionality/invnum.txt", "r").read()
    boolers = open("src/bool_functionality/"+invnum+".json", "r")
    booldict = json.load(boolers)
    date = open("src/bool_functionality/booldate.txt").read()
    embed = discord.Embed(title="Bool List", description="The list of people who agreed to bool on " + date, color=message.author.color)
    for k, v in booldict.items():
        if v == "Yes":
            embed.add_field(name = k, value=" has agreed")
    embed.set_footer(text="Copyright Nelson Net 2021 | " + message.guild.name)
    await message.channel.send(embed = embed)
