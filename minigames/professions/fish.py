import secrets
import discord
from .mechanics import roll_rarity, make_item_id, get_all_items, get_items_in_rarity, notify_channel_of_special
from sigma.core.utilities.data_processing import user_avatar


async def fish(cmd, message, args):
    all_fish = get_all_items('fish', cmd.resource('data'))
    if not cmd.bot.cooldown.on_cooldown(cmd.name, message.author):
        cmd.bot.cooldown.set_cooldown(cmd.name, message.author, 60)
        kud = cmd.db.get_currency(message.author, message.guild)
        if kud['current'] >= 20:
            cmd.db.rmv_currency(message.author, message.guild, 20)
            rarity = roll_rarity()
            if args:
                if message.author.id in cmd.bot.cfg.dsc.owners:
                    try:
                        rarity = int(args[0])
                    except TypeError:
                        pass
            all_items_in_rarity = get_items_in_rarity(all_fish, rarity)
            item = secrets.choice(all_items_in_rarity)
            value = item.value
            connector = 'a'
            if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            if value == 0:
                response_title = f'{item.icon} You caught {connector} {item.name} and threw it away!'
            else:
                response_title = f'{item.icon} You caught {connector} {item.rarity_name} {item.name}!'
                item_id = make_item_id()
                data_for_inv = {
                    'item_id': item_id,
                    'item_file_id': item.item_file_id,
                }
                cmd.db.add_to_inventory(message.author, data_for_inv)
            response = discord.Embed(color=item.color, title=response_title)
            response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
            if item.rarity >= 5:
                if 'fish_channel' in cmd.cfg:
                    await notify_channel_of_special(message, cmd.bot.get_all_channels(), cmd.cfg['fish_channel'], item)
        else:
            response = discord.Embed(color=0xDB0000, title=f'❗ You don\'t have enough {cmd.bot.cfg.pref.currency}!')
    else:
        timeout = cmd.bot.cooldown.get_cooldown(cmd.name, message.author)
        response = discord.Embed(color=0x696969, title=f'🕙 Your new bait will be ready in {timeout} seconds.')
    await message.channel.send(embed=response)
