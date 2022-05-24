"""Helper class for checking the last time a user sent a message"""
import discord
from datetime import datetime

today = datetime.today()
async def dead_check(ctx):
    """Returns when each user messaged last then removes a user if they have not messaged in 1 month"""
    chan = ctx.channel
    users = ctx.guild.members
    dead_users = []
    new_msg = await ctx.send("Checking the dead...")
    for i in users:
        last_msg=await ctx.channel.history(limit=None).get(author__name=i.name)
        if not (last_msg is None):
            if (today - last_msg.created_at).days)) > 30:
                dead_users.append(i)

    print(dead_users)
    




    