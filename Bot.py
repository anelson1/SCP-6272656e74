import discord
import random

client = discord.Client()
with open ("key.txt", "r") as myfile:
    authkey=myfile.read()

@client.event
async def on_ready():
    print("Ahoy!")


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
            await  message.channel.send("Ahoy! @" + str(users[num]) + "that will have to be a negatory me boy!")
        else:
            await  message.channel.send("Ahoy! @" + str(users[num]) + " me boy! You are now rainbow! AGHAHAHAHAHAHA")
            await colorChange(role, color)
    elif "!rainbow" in message.content:
        color = message.author.color
        if not role.permissions.administrator:
            await  message.channel.send("Ahoy! " + str(message.author.nick) + " you have color! AGHAHAHAHAHAHAHHAHA")
            await colorChange(role, color)
    if message.content == "!palu":
        emoji = discord.utils.get(client.emojis, name = "beamend")
        await message.channel.send(emoji)
        for i in range(random.randint(0,10)):
            await message.channel.send(discord.utils.get(client.emojis, name = "beam"))
        await message.channel.send(discord.utils.get(client.emojis, name = "palu2"))
        await message.channel.send(discord.utils.get(client.emojis, name = "palu1"))
    if message.content == "end" and role.permissions.administrator:
        print("Bye")
        exit(0)

async def colorChange(role, color):
    r = 255
    g = 0
    b = 0
    for i in range(100):
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
        await role.edit(colour = discord.Colour.from_rgb(r,g,b))
    await role.edit(colour=color)



client.run(authkey)
