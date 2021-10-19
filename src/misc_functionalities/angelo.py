import discord

async def specificangelo(message, word):
    if not word:
        await message.channel.send("Please provide a string")
        return
    chan = message.channel
    count = 0
    totalmsg = 0
    newmsg = await message.channel.send("Counting...")
    async with message.channel.typing():
        async for msg in chan.history(limit=None):
            totalmsg += 1
            if msg.author == message.author:
                words = msg.content.split()
                for i in words:
                    if i.lower() == word.lower():
                        count+=1
        await newmsg.delete()
    embed = discord.Embed(title="Specific Word Count", description="Counts the number of times a user has said a specific word", color=message.author.color)
    embed.add_field(name=message.author, value="Has said " + word + " "+  str(count-1) + " many times in " + str(message.channel))
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.set_footer(text="Based on " + str(totalmsg) + " messages")
    await message.channel.send(embed=embed)

async def angelo(message):
    chan = message.channel
    count = 0
    totalmsg = 0
    newmsg = await message.channel.send("Counting...")
    async with message.channel.typing():
        async for msg in chan.history(limit=None):
            totalmsg += 1
            if msg.author == message.author:
                count+=1
        await newmsg.delete()
    embed = discord.Embed(title="Word Count", description="Counts the number of times a user has sent messages", color=message.author.color)
    embed.add_field(name=message.author, value=message.author.nick + " has accounted for " + str((count/totalmsg)*100) + "% of all messages in " + str(message.channel))
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.set_footer(text="Based on " + str(totalmsg) + " messages")
    await message.channel.send(embed=embed)
    if message.author.nick == "Angelo Nelson":
        await message.channel.edit(topic = "Pretty much just Angelo saying dumb shit " + str((count/totalmsg)*100) + "% of the time")

async def bigangelo(message):
    chan = message.channel
    users = {}
    result = ""
    totalmsg = 0
    newmsg = await message.channel.send("Counting...")
    async with message.channel.typing():
        async for msg in chan.history(limit=None):
            try:
                if msg.author.nick == None:
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
        for k, v in sortedusers.items():
            await message.channel.send("***"+str(k)+"***" + " has accounted for " + "***"+str((v/totalmsg)*100) + "%*** of all messages in " + str(message.channel))
    await message.channel.send("Based on " + str(totalmsg) + " messages")
    