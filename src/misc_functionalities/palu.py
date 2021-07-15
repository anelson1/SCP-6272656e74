from src import discord, client
import random

async def generate_emoji(message):
    emoji = discord.utils.get(client.emojis, name="beamend")
    await message.channel.send(emoji)
    for i in range(random.randint(0, 10)):
        await message.channel.send(discord.utils.get(client.emojis, name="beam"))
    await message.channel.send(discord.utils.get(client.emojis, name="palu2"))
    await message.channel.send(discord.utils.get(client.emojis, name="palu1"))