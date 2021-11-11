"""Helper class for equity related operations"""
import discord

async def specificword(ctx, word):
    """Counts how many times the user has said a specific word"""
    chan = ctx.channel
    count = 0
    totalmsg = 0
    newmsg = await ctx.send("Counting...")
    async with ctx.channel.typing():
        async for msg in chan.history(limit=None):
            totalmsg += 1
            if msg.author == ctx.author:
                words = msg.content.split()
                for i in words:
                    if i.lower() == word.lower():
                        count+=1
        await newmsg.delete()
    embed = discord.Embed(title="Specific Word Count",
                          description="Counts the number of times a user has said a specific word",
                          color=ctx.author.color)
    embed.add_field(name=ctx.author,
                    value="Has said "
                    + word
                    + " "
                    + str(count-1)
                    + " many times in "
                    + str(ctx.channel))
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text="Based on " + str(totalmsg) + " messages")
    await ctx.send(embed=embed)

async def equity(ctx, user):
    """Returns the equity of the user"""
    chan = ctx.channel
    count = 0
    totalmsg = 0
    newmsg = await ctx.send("Counting...")
    async with chan.typing():
        async for msg in chan.history(limit=None):
            totalmsg += 1
            if msg.author == user:
                count+=1
        await newmsg.delete()
    embed = discord.Embed(title="Chat Equity",
                          description="Gives the percentage of messages that belong to the user",
                          color=user.color)
    embed.add_field(name=user,
                    value=user.display_name
                    + " has accounted for "
                    + str((count/totalmsg)*100)
                    + "% of all messages in "
                    + str(ctx.channel))
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text="Based on " + str(totalmsg) + " messages")
    await ctx.send(embed=embed)
    if user.nick == "Angelo Nelson":
        await ctx.channel.edit(topic="Pretty much just Angelo saying dumb shit "
                               + str((count/totalmsg)*100)
                               + "% of the time")

async def bigangelo(ctx):
    """Calculates the total equity of everyone in the channel"""
    chan = ctx.channel
    users = {}
    totalmsg = 0
    newmsg = await ctx.send("Counting...")
    async with ctx.channel.typing():
        async for msg in chan.history(limit=None):
            try:
                if msg.author.nick is None:
                    name = msg.author
                else:
                    name = msg.author.nick
            except:
                name = msg.author
            totalmsg+=1
            if name not in users:
                users[name] = 1
            else:
                users[name] = users[name] + 1
        sortedusers = dict(sorted(users.items(),key= lambda x:x[1], reverse=True))
        await newmsg.delete()
        embed = discord.Embed(title="Total Chat Equity for " + str(ctx.channel),
                              description="Gives the equity of all users",
                              color=discord.Color.random())
        for key, value in sortedusers.items():
            embed.add_field(name=str(key),
                            value="Has accounted for "
                            + str((value/totalmsg)*100)
                            + "% of all messages",
                            inline=False)
        embed.set_footer(text="Based on " + str(totalmsg) + " messages")
    await ctx.send(embed=embed)
    