﻿import secrets
import discord


async def rps(cmd, message, args):
    if not args:
        embed = discord.Embed(color=0xDB0000, title='❗ Nothing inputted.')
        await message.channel.send(None, embed=embed)
    else:
        sign_list = ['rock', 'paper', 'scissors']
        my_choice = secrets.choice(sign_list)
        if args[0].lower().startswith('r'):
            their_choice = 'rock'
            counter = 'paper'
        elif args[0].lower().startswith('p'):
            their_choice = 'paper'
            counter = 'scissors'
        elif args[0].lower().startswith('s'):
            their_choice = 'scissors'
            counter = 'rock'
        else:
            embed = discord.Embed(color=0xDB0000, title='❗ Unrecognized sign.')
            await message.channel.send(None, embed=embed)
            return
        if my_choice == their_choice:
            embed = discord.Embed(color=0xFF9900, title=':fire: It\'s a draw!')
        elif my_choice == counter:
            embed = discord.Embed(color=0xDB0000, title='❗ You lose!')
        else:
            embed = discord.Embed(color=0x0099FF, title=':gem: You win!')
        embed.add_field(name='User\'s Choice', value='**' + their_choice.title() + '**')
        embed.add_field(name='Sigma\'s Choice', value='**' + my_choice.title() + '**')
        await message.channel.send(None, embed=embed)
