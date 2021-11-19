"""
Class for all boolin relation functionality
"""
import json
from datetime import datetime
import discord

MAIN_SERVER_ID = 423937254046826496
GENERAL_ID = 423937254046826498
DEV_CHAN_ID = 636978333426384906
BOOL_ROLE_ID = 855652264663318540
DEV_ROLE_ID = 760375992513724426
# Parse message and update JSON file with name and RSVP Status
async def bool_rsvp(ctx, decision, bot):
    """Handler for the recieving of bool invites"""
    if decision:
        userdict = {str(ctx.message.author): "Yes"}
        await ctx.message.channel.send("You agreed to bool!")
        embed = discord.Embed(
            title=ctx.message.author,
            description="Has agreed to bool!",
            color=discord.Colour.green())
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021")
        await bot.get_channel(GENERAL_ID).send(embed = embed)
    else:
        userdict = {str(ctx.message.author): "No"}
        embed = discord.Embed(
            title=ctx.message.author,
            description="Has turned down the offer to bool!",
            color=discord.Colour.red())
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021")
        await bot.get_channel(GENERAL_ID).send(embed = embed)
    invnum = open("src/bool_functionality/invnum.txt").read()
    try:
        myfile = open("src/bool_functionality/"+invnum+".json", "r+")
    except:
        myfile = open("src/bool_functionality/"+invnum+".json", "w+")
    content = myfile.read()
    myfile.close()
    try:
        myjson = json.loads(content)
        myjson.update(userdict)
        json_string = json.dumps(myjson)
    except:
        json_string = json.dumps(userdict)
    myfile1 = open("src/bool_functionality/"+invnum+".json", "w+")
    myfile1.write(json_string)
    myfile1.close()


async def bool_send(ctx, dateofbool):
    """Send RSVPs to bool"""
    current_time = datetime.now().strftime("%H:%M:%S")
    current_day = datetime.now().strftime("%m/%d/%y")
    embed = discord.Embed(title="Bool RSVP",
                          description="Asking the fellas to bool",
                          color=ctx.message.author.color)
    embed.add_field(name="Bool invites",
                    value="Have been sent by " +
                    ctx.message.author.nick +
                    " on " +  current_day +
                    " at " + current_time)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.set_footer(text="Copyright Nelson Net 2021 | " + ctx.message.guild.name)
    await ctx.send(embed = embed)
    datefile = open("src/bool_functionality/booldate.txt", "w+")
    datefile.write(dateofbool)
    datefile.close()
    role = ctx.message.guild.get_role(BOOL_ROLE_ID)
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
        embed = discord.Embed(title="Bool RSVP",
                              description="Asking the fellas to bool",
                              color=ctx.message.author.color)
        embed.add_field(name = str(ctx.message.author),
                        value = "Would like to bool on "
                        + str(dateofbool)
                        + ". Please respond with !confirmbool <yes/no>.")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021 | " + ctx.message.guild.name)
        await chan.send(embed = embed)


async def bool_list(message):
    """List people who have RSVPed to bool"""
    invnum = open("src/bool_functionality/invnum.txt", "r").read()
    boolers = open("src/bool_functionality/"+invnum+".json", "r")
    booldict = json.load(boolers)
    date = open("src/bool_functionality/booldate.txt").read()
    embed = discord.Embed(title="Bool List",
                          description="The list of people who agreed to bool on "
                          + date, color=message.author.color)
    for key, value in booldict.items():
        if value == "Yes":
            embed.add_field(name = key, value=" has agreed")
    embed.set_footer(text="Copyright Nelson Net 2021 | " + message.guild.name)
    await message.channel.send(embed = embed)
