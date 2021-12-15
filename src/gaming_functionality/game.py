"""
Class for all boolin relation functionality
"""
import json
from datetime import datetime
import discord

GENERAL_ID = 423937254046826498
DEV_CHAN_ID = 636978333426384906
DEV_ROLE_ID = 760375992513724426

# Parse message and update JSON file with name and RSVP Status
async def game_rsvp(ctx, decision, bot):
    """Handler for the receiving of game requests"""
    json_file = open('src/bool_functionality/gamingdata.json', 'r')
    data = json.load(json_file)
    json_file.close()
    if decision:
        userdict = {str(ctx.message.author.id): "Y"}
        await ctx.message.channel.send("You agreed to game!")
        embed = discord.Embed(
            title=ctx.message.author,
            description="Has agreed to game!",
            color=discord.Colour.green())
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021 | Sent from " + ctx.guild.name)
        await bot.get_channel(GENERAL_ID).send(embed = embed)
    else:
        userdict = {str(ctx.message.author.id): "N"}
        await ctx.message.channel.send("You denied gaming!")
        embed = discord.Embed(
            title=ctx.message.author,
            description="Has denied the request to game!",
            color=discord.Colour.red())
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021 | Sent from " + ctx.guild.name)
        await bot.get_channel(GENERAL_ID).send(embed = embed)
    data.update(userdict)
    json_file = open('src/bool_functionality/boolindata.json', 'w')
    json.dump(data, json_file)
    json_file.close()

async def game_send(ctx, game):
    """Send RSVPs to game"""
    GAME_ROLE_ID = await ctx.guild.fetch_roles()["Gaming"]
    current_time = datetime.now().strftime("%H:%M:%S")
    current_day = datetime.now().strftime("%m/%d/%y")
    embed = discord.Embed(title="Gaming Request",
                          description="Asking the fellas to game",
                          color=ctx.message.author.color)
    embed.add_field(name="Gaming Requests",
                    value="Have been sent by " +
                    ctx.message.author.nick +
                    " on " +  current_day +
                    " at " + current_time)
    embed.set_thumbnail(url=ctx.message.author.avatar_url)
    embed.set_footer(text="Copyright Nelson Net 2021 | Sent from " + ctx.message.guild.name)
    await ctx.send(embed = embed)
    role = ctx.message.guild.get_role(GAME_ROLE_ID)
    json_file = '{"game": "' + game +'", '
    for member in role.members:
        json_file += '"' + str(member.id) + '": "NA", '
        chan = await member.create_dm()
        embed = discord.Embed(title="Gaming Request",
                              description="Asking the fellas to game",
                              color=ctx.message.author.color)
        embed.add_field(name = str(ctx.message.author),
                        value = "Would like to play "
                        + str(game)
                        + ". Please respond with !confirmgame <yes/no>.")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.set_footer(text="Copyright Nelson Net 2021 | Sent from " + ctx.message.guild.name)
        await chan.send(embed = embed)
    json_file = json_file[0:len(json_file)-2]
    json_file += "}"
    data = json.loads(json_file)
    file = open("src/bool_functionality/gamingdata.json" , 'w')
    json.dump(data, file)
    file.close()
    print(data)


async def game_list(message, annoy, bot):
    """List people who have RSVPed to game"""
   
    gamers = open("src/bool_functionality/boolindata.json", "r")
    gamedict = json.load(gamers)
    game = gamedict['game']
    embed = discord.Embed(title="Gaming List",
                          description="The list of people who were requested to play "
                          + game, color=message.author.color)
    for key, value in gamedict.items():
        if not key == "game":
            key = str(await bot.fetch_user(key))
            if value == "Y":
                embed.add_field(name = key, value="✅")
            if value == "N":
                embed.add_field(name=key, value="❌")
            if value == "NA":
                embed.add_field(name=key, value="❔")
    embed.set_footer(text="Copyright Nelson Net 2021 | Sent from " + message.guild.name)
    await message.channel.send(embed = embed)
    if annoy:
        for key, value in gamedict.items():
            if value == "NA":
                ping = await bot.fetch_user(key)
                await message.send(ping.mention)