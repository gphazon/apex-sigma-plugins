import asyncio
import discord
from .nodes.sortie_functions import get_sortie_data, generate_sortie_embed
from .nodes.fissure_functions import get_fissure_data, generate_fissure_embed
from .nodes.alert_functions import get_alert_data, generate_alert_embed


async def wf_clockwork(ev):
    while True:
        try:
            all_guilds = ev.bot.guilds
            sorties = await get_sortie_data(ev.db)
            if sorties:
                sortie_response = generate_sortie_embed(sorties)
                for guild in all_guilds:
                    sortie_channel = ev.db.get_guild_settings(guild.id, 'WarframeSortieChannel')
                    if sortie_channel:
                        sortie_target_channel = discord.utils.find(lambda x: x.id == sortie_channel, guild.channels)
                        if sortie_target_channel:
                            try:
                                await sortie_target_channel.send(embed=sortie_response)
                            except discord.ClientException:
                                pass
            fissures = await get_fissure_data(ev.db)
            if fissures:
                fissure_response = generate_fissure_embed(fissures)
                for guild in all_guilds:
                    fissure_channel = ev.db.get_guild_settings(guild.id, 'WarframeFissureChannel')
                    if fissure_channel:
                        fissure_target_channel = discord.utils.find(lambda x: x.id == fissure_channel, guild.channels)
                        try:
                            await fissure_target_channel.send(embed=fissure_response)
                        except discord.ClientException:
                            pass
            alerts, triggers = await get_alert_data(ev.db)
            if alerts:
                alert_response = await generate_alert_embed(alerts)
                for guild in all_guilds:
                    mentions = []
                    if triggers:
                        for trigger in triggers:
                            wf_tags = ev.db.get_guild_settings(guild.id, 'WarframeTags')
                            if wf_tags is None:
                                wf_tags = {}
                            if wf_tags:
                                if trigger in wf_tags:
                                    bound_role = discord.utils.find(lambda x: x.id == wf_tags[trigger], guild.roles)
                                    if bound_role:
                                        mentions.append(bound_role.mention)
                    alert_channel = ev.db.get_guild_settings(guild.id, 'WarframeAlertChannel')
                    if alert_channel:
                        alert_target_channel = discord.utils.find(lambda x: x.id == alert_channel, guild.channels)
                        try:
                            if mentions:
                                await alert_target_channel.send(' '.join(mentions), embed=alert_response)
                            else:
                                await alert_target_channel.send(embed=alert_response)
                        except discord.ClientException:
                            pass
        except discord.ClientException:
            pass
        except Exception:
            pass
        await asyncio.sleep(5)
