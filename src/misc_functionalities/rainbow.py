from src import discord
import random
#pick a random user, ensure they arent an admin, make them rainbow
async def rainbow(message):
    users = message.guild.members
    num = random.randint(0, len(users))
    color = users[num].color
    role = message.guild.get_role(users[num].top_role.id)
    if role.permissions.administrator:
        print("is admin")
        role = message.guild.get_role(users[num].roles[-2].id)
        await message.channel.send(str(users[num]) + "is now based!")
        await colorChange(role, color)
    else:
        await message.channel.send(str(users[num]) + "is now based!")
        await colorChange(role, color)
        
async def colorChange(role, color):
    r = 255
    g = 0
    b = 0
    for i in range(100):
        print(r, g, b)
        if r == 255 and b == 0 and g != 255:
            g += 51
        elif g == 255 and r != 0:
            r -= 51
        elif g == 255 and b != 255:
            b += 51
        elif b == 255 and g != 0:
            g -= 51
        elif b == 255 and r != 255:
            r += 51
        elif r == 255 and b != 0:
            b -= 51
        await role.edit(colour=discord.Color.from_rgb(r, g, b))
    await role.edit(colour=color)
