"""Helper class for checking the last time a user sent a message"""
import discord
from datetime import datetime

today = datetime.today()
async def dead_check(ctx):
    """Returns when each user messaged last then removes a user if they have not messaged in 1 month"""
    usr_msg = {}
    chan = ctx.channel
    new_msg = await ctx.send("Checking the dead...")
    async with ctx.channel.typing():
        async for msg in chan.history(limit=None):
            if msg.author not in usr_msg:
                usr_msg[msg.author] = msg.created_at
        
        for key, value in usr_msg.items():
                if (today - value).days > 30:
                    await key.remove_roles(ctx.guild.get_role(974090144451809341))
                    embed = discord.Embed(title = key.display_name, description = "will be killed!", color=key.color)
                    embed.set_thumbnail(url=key.avatar_url)
                    embed.set_footer(text=ctx.guild.name + " | Nelson Net 2022")
                    await ctx.channel.send(embed=embed)    
    await new_msg.delete()



    