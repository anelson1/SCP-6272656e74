import discord

async def angelo(message):
    chan = message.channel
    count = 0
    newmsg = await message.channel.send("Counting...")
    async with message.channel.typing():
        async for msg in chan.history(limit=1000):
            if msg.author == message.author:
                count+=1
        await newmsg.delete()
        await message.channel.send(message.author.nick + " has accounted for " + str((count/1000)*100) + "% of all messages in " + str(message.channel))
    if message.author.nick == "Angelo Nelson":
        await message.channel.edit(topic = "Pretty much just Angelo saying dumb shit " + str((count/1000)*100) + "% of the time")