"""Helper class for rainbow functions"""
import random
import discord

#pick a random user, ensure they arent an admin, make them rainbow
async def rainbow(ctx):
    """Pick a user, and change their role color very quick in rainbow order"""
    users = ctx.guild.members
    num = random.randint(0, len(users))
    color = users[num].color
    role = ctx.guild.get_role(users[num].top_role.id)
    if role.permissions.administrator:
        print("is admin")
        role = ctx.guild.get_role(users[num].roles[-2].id)
        await ctx.send(str(users[num]) + "is now based!")
        await color_change(role, color)
    else:
        await ctx.send(str(users[num]) + "is now based!")
        await color_change(role, color)


async def color_change(role, color):
    """Helper for the rainbow method"""
    red = 255
    green = 0
    blue = 0
    for _ in range(100):
        print(red, green, blue)
        if red == 255 and blue == 0 and green != 255:
            green += 51
        elif green == 255 and red != 0:
            red -= 51
        elif green == 255 and blue != 255:
            blue += 51
        elif blue == 255 and green != 0:
            green -= 51
        elif blue == 255 and red != 255:
            red += 51
        elif red == 255 and blue != 0:
            blue -= 51
        await role.edit(colour=discord.Color.from_rgb(red, green, blue))
    await role.edit(colour=color)
