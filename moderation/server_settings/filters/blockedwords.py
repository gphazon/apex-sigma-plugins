import discord


async def blockedwords(cmd, message, args):
    blocked_words = cmd.db.get_guild_settings(message.guild.id, 'BlockedWords')
    if not blocked_words:
        response = discord.Embed(color=0x0099FF, title='ℹ There are no blocked words.')
    else:
        response = discord.Embed(color=0x0099FF)
        response.add_field(name=f'ℹ There are {len(blocked_words)} blocked words.', value=', '.join(blocked_words))
    await message.channel.send(embed=response)
