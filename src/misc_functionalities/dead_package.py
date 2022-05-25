"""Helper class for checking the last time a user sent a message"""
import discord
from datetime import datetime

today = datetime.today()
async def dead_check(ctx):
    """Returns when each user messaged last then removes a user if they have not messaged in 1 month"""
    users = ctx.guild.members
    new_msg = await ctx.send("Checking the dead...")
    async with ctx.channel.typing():
        for i in users:
            last_msg=await ctx.channel.history(limit=None).get(author__name=i.name)
            if not (last_msg is None):
                if (today - last_msg.created_at).days > 30:
                    await i.remove_roles(ctx.guild.get_role(974090144451809341))
                    embed = discord.Embed(title = i.display_name, description = "will be killed!", color=i.color)
                    embed.set_thumbnail(url=i.avatar_url)
                    embed.set_footer(text=ctx.guild.name + " | Nelson Net 2022")
                    await ctx.channel.send(embed=embed)    




    