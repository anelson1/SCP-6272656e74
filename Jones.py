import discord
import random

client = discord.Client()


@client.event
async def on_ready():
    print("Ahoy!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!gayroulette":
        users = message.guild.members
        num = random.randint(0,len(users))
        color = users[num].color
        await  message.channel.send("Ahoy! @" + str(users[num]) + " me boy! You are tonight's biggest gay! AGHAHAHAHAHAHA")
        role = message.guild.get_role(users[num].top_role.id)
        if role == "Admin":
            await  message.channel.send("Ahoy! @" + str(users[num]) + "on account of your admin status, you have been spared from the big gay! AGHAHAHAHA")
        else:
            print(role)
            r = 255
            g = 0
            b = 0
            for i in range(100):
                if r == 255 and b == 0 and g is not 255:
                    g += 51
                elif g == 255 and r is not 0:
                    r -= 51
                elif g == 255 and b is not 255:
                    b += 51
                elif b == 255 and g is not 0:
                    g -= 51
                elif b == 255 and r is not 255:
                    r += 51
                elif r == 255 and b is not 0:
                    b -= 51
                await role.edit(colour=discord.Colour.from_rgb(r, g, b))
            await role.edit(colour=color)

    elif "gay" in message.content:
        color = message.author.color
        role = message.guild.get_role(message.author.top_role.id)
        if role.permissions.administrator:
            await  message.channel.send("Ahoy! " + str(message.author.nick) + " on account of your admin status, you have been spared from the big gay! AGHAHAHAHA")
        else:
            await  message.channel.send("Ahoy! " + str(message.author.nick) + " you have the big gay! AGHAHAHAHAHAHAHHAHA")
            r = 255
            g = 0
            b = 0
            for i in range(100):
                if r == 255 and b == 0 and g is not 255:
                    g+=51
                elif g == 255 and r is not 0:
                    r-=51
                elif g == 255 and b is not 255:
                    b+=51
                elif b==255 and g is not 0:
                    g-=51
                elif b == 255 and r is not 255:
                    r+=51
                elif r==255 and b is not 0:
                    b-=51
                await role.edit(colour = discord.Colour.from_rgb(r,g,b))
            await role.edit(colour=color)




client.run("MzU5NzI4Nzg5MDcwMDIwNjA4.XQby-w.gHl18aBKwSyluiPLkVmT79HcB9o")
