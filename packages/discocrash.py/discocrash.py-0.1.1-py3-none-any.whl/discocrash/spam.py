import disnake
from disnake.ext import commands
import asyncio




async def spam(ctx, textspam, nummsg: int):
    for i in range(nummsg):
        await ctx.send(textspam)


async def spamdm(ctx, member: disnake.Member, text, nummsg):
  for i in range(nummsg):
    while True:
      await member.send(text)



async def everdm(ctx, text):
  author = ctx.message.author
  for member in ctx.guild.members:
        try:
            await member.send(args)
        except:
            continue