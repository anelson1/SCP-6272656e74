"""Helper class for checking the last time a user sent a message"""
import discord
from datetime import date

today = date.today()

async def dead_check(ctx):
    """Returns when each user messaged last then removes a user if they have not messaged in 1 month"""
    chan = ctx.channel
    users = {}
    users_to_kill =[]
    newmsg = await ctx.send("Checking the dead...")
    async with ctx.channel.typing():
        async for msg in chan.history(limit=None):
            msgdate = msg.created_at

            if msg.author not in users:
                users[msg.author] = msgdate
    embed = discord.Embed(title="Dead Checker",
                    description="Returns the last time a user sent a message",
                    color=discord.Color.random())
    await newmsg.delete()
    for key, value in users.items():
        embed.add_field(name=str(key), value=value.strftime("%m/%d/%Y") + " at " + value.strftime("%H:%M:%S"), inline=False)
        if (int(value.strftime("%m")) - int(today.strftime("%m"))) >= 1:
            users_to_kill.append(key)
    embed.set_footer(text=str(ctx.channel) + " | Nelson Net 2022")
    await ctx.send(embed=embed)
    for i in users_to_kill:
        await i.remove_roles(ctx.guild.get_role(974090144451809341))
        embed = discord.Embed(title = i.name, description = "will be killed!", color=i.color)
        embed.set_thumbnail(url=i.avatar_url)
        embed.set_footer(text=ctx.guild.name + " | Nelson Net 2022")
        await ctx.send(embed=embed)




    