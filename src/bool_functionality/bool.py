from src.constants import MAIN_SERVER_ID, GENERAL_ID, DEV_CHAN_ID, BOOL_ROLE_ID, DEV_ROLE_ID
from src import client
import json

# Parse message and update JSON file with name and RSVP Status


async def bool_RSVP(message):
    if message.content == "!Y" or message.content == "!N":
        if message.content == "!Y":
            dict = {str(message.author): "Yes"}
            await message.channel.send("You agreed to bool!")
            await client.get_channel(GENERAL_ID).send(str(message.author) + " has agreed to bool!")
        if message.content == "!N":
            dict = {str(message.author): "No"}
            await message.channel.send("You turned down the offer to bool.")
            await client.get_channel(GENERAL_ID).send(str(message.author) + " has turned down the offer to bool!")
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
    if message.author.id != 213559733758459905:
        await message.channel.send("For security reasons, only Angelo can initate this command.")
    else:
        await message.channel.send("Sending invites...")
        param = message.content[6::]
        datefile = open("src/bool_functionality/booldate.txt", "w+")
        datefile.write(param)
        datefile.close()
        role = message.guild.get_role(BOOL_ROLE_ID)
        invitenumber = open("src/bool_functionality/invnum.txt", "r").read()
        newinvitenumber = open("src/bool_functionality/invnum.txt", "w+")
        newinvitenumber.write(str(int(invitenumber) + 1))
        newinvitenumber.close()
        for member in role.members:
            chan = await member.create_dm()
            await chan.send(str(message.author) + " would like to bool on " + str(param) + ". Please respond with !Y for yes or !N for no.")
            
            
# List people who have RSVPed to bool


async def bool_list(message):
    invnum = open("src/bool_functionality/invnum.txt", "r").read()
    boolers = open("src/bool_functionality/"+invnum+".json", "r")
    booldict = json.load(boolers)
    date = open("src/bool_functionality/booldate.txt").read()
    string = "So far: "
    for k, v in booldict.items():
        if v == "Yes":
            string += k + ", "
    string += "has agreed to bool on " + date
    await message.channel.send(string)
