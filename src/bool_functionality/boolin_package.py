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
    """Handler for the receiving of bool invites"""
    json_file = open('src/bool_functionality/boolindata.json', 'r')
    data = json.load(json_file)
    json_file.close()
    if decision:
        userdict = {str(ctx.message.author.id): "Y"}
        await ctx.message.channel.send("You agreed to bool!")
        embed = discord.Embed(
            title=ctx.message.author,
            description="Has agreed to bool!",
            color=discord.Colour.green())
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021")
        await bot.get_channel(GENERAL_ID).send(embed = embed)
    else:
        userdict = {str(ctx.message.author.id): "N"}
        await ctx.message.channel.send("You turned down the offer to bool!")
        embed = discord.Embed(
            title=ctx.message.author,
            description="Has turned down the offer to bool!",
            color=discord.Colour.red())
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021")
        await bot.get_channel(GENERAL_ID).send(embed = embed)
    data.update(userdict)
    json_file = open('src/bool_functionality/boolindata.json', 'w')
    json.dump(data, json_file)
    json_file.close()

async def bool_send(ctx, date_of_bool):
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
    role = ctx.message.guild.get_role(BOOL_ROLE_ID)
    json_file = '{"date": "' + date_of_bool +'", '
    for member in role.members:
        json_file += '"' + str(member.id) + '": "NA", '
        chan = await member.create_dm()
        embed = discord.Embed(title="Bool RSVP",
                              description="Asking the fellas to bool",
                              color=ctx.message.author.color)
        embed.add_field(name = str(ctx.message.author),
                        value = "Would like to bool on "
                        + str(date_of_bool)
                        + ". Please respond with !confirmbool <yes/no>.")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021 | " + ctx.message.guild.name)
        await chan.send(embed = embed)
    json_file = json_file[0:len(json_file)-2]
    json_file += "}"
    data = json.loads(json_file)
    file = open("src/bool_functionality/boolindata.json" , 'w')
    json.dump(data, file)
    file.close()
    print(data)


async def bool_list(message, annoy, bot):
    """List people who have RSVPed to bool"""
   
    boolers = open("src/bool_functionality/boolindata.json", "r")
    booldict = json.load(boolers)
    date = booldict['date']
    embed = discord.Embed(title="Bool List",
                          description="The list of people who were asked to bool on "
                          + date, color=message.author.color)
    for key, value in booldict.items():
        if not key == "date":
            key = str(await bot.fetch_user(key))
            if value == "Y":
                embed.add_field(name = key, value="✅")
            if value == "N":
                embed.add_field(name=key, value="❌")
            if value == "NA":
                embed.add_field(name=key, value="❔")
    embed.set_footer(text="Copyright Nelson Net 2021 | " + message.guild.name)
    await message.channel.send(embed = embed)
    if annoy:
        for key, value in booldict.items():
            if value == "NA":
                ping = await bot.fetch_user(key)
                await message.send(ping.mention)