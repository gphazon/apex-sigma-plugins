import discord


async def blockwords(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            blocked_words = cmd.db.get_guild_settings(message.guild.id, 'BlockedWords')
            if blocked_words is None:
                blocked_words = []
            added_words = []
            for word in args:
                if word.lower() not in blocked_words:
                    blocked_words.append(word.lower())
                    added_words.append(word.lower())
            cmd.db.set_guild_settings(message.guild.id, 'BlockedWords', blocked_words)
            if added_words:
                color = 0x66CC66
                title = f'✅ I have added {len(added_words)} to the blacklist.'
            else:
                color = 0x0099FF
                title = 'ℹ No new words were added.'
            response = discord.Embed(color=color, title=title)
        else:
            response = discord.Embed(title='⛔ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)
