import disnake
from disnake.ext import commands
import asyncio


async def kickeveryone(ctx, reasonkick, textauthor, guildtext):
    kicked = 0
    nokicked = 0
    await ctx.message.delete()
    for janek in ctx.guild.members:
        if int(janek.id) != int(ctx.message.author.id):
            try:
                await ctx.guild.kick(janek, reason=reasonkick)
                kicked +=1
            except:
                nokicked +=1

    try:
        await ctx.author.send(textauthor)
    except:
        await ctx.send(guildtext)



