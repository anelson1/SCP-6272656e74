from src import discord, client

async def whois(message, id):
    try:
        try:
            user = await message.guild.fetch_member(id)
            member = True
        except:
            user = await client.fetch_user(id)
            member = False
    except:
        await message.channel.send("No user was found, please try again")
        return
    if member: 
        embed = discord.Embed(title = user.display_name, color=user.color)
        embed.add_field(name="Full Tag:", value=user)
        embed.add_field(name="Currently Playing:", value=user.activity)
        embed.add_field(name="Status:", value=user.status.value)
        embed.add_field(name="Joined on:", value=user.joined_at.strftime('%m/%d/%y'))
        embed.add_field(name="Top Role:", value=user.top_role)
    else:
        embed = discord.Embed(title = user, color=discord.Color.random())
    embed.add_field(name="ID:", value=str(user.id))
    embed.add_field(name="Account created on:", value=user.created_at.strftime('%m/%d/%y'))
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text=message.guild.name + " | Copywrite Nelson Net 2021")
    await message.channel.send(embed=embed)