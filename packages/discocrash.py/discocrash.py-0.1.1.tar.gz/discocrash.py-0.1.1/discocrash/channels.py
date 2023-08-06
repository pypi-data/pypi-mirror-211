import disnake
from disnake.ext import commands
import asyncio


async def channel_spam(channel, webhookname, contentmsg, embedmsg, nummsg: int):
    try:
        webhook = await channel.create_webhook(name=webhookname)
        for _ in range(nummsg):
          await webhook.send(content=contentmsgwebhook, embed=disnake.Embed(title=embedmsgwebhook))
    except:
       for _ in range(nummsg):
         await channel.send(content=contentmsgwebhook, embed=disnake.Embed(title=embedmsgwebhook))

async def sendch(ch,text,count):
 for _ in range(count):
    try: await ch.send(text)
    except: pass