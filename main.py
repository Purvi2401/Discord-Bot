import discord
from discord.ext import commands, tasks
import asyncio
from itertools import cycle
import os
import json
import random
# from dotenv import load_dotenv

# load_dotenv()

client = commands.Bot(command_prefix=')')

status = cycle(
    ['Try )help', 'Prefix - )'])


@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready')


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# main

mainshop = [{"name": "Watch", "price": 10, "description": "Time"},
            {"name": "Laptop", "price": 100, "description": "Work"},
            {"name": "PC", "price": 1000, "description": "Gaming"}]


@client.command(aliases=['bal'])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(
        title=f'{ctx.author.name} Balance', color=discord.Color.red())
    em.add_field(name="Wallet Balance", value=wallet_amt)
    em.add_field(name='Bank Balance', value=bank_amt)
    await ctx.send(embed=em)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f'{ctx.author.mention} Got {earnings} coins!!')

    users[str(user.id)]["wallet"] += earnings

    with open("inventory.json", 'w') as f:
        json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('inventory.json', 'w') as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open('inventory.json', 'r') as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('inventory.json', 'w') as f:
        json.dump(users, f)
    bal = users[str(user.id)]['wallet'], users[str(user.id)]['bank']
    return bal

# main ends

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# token = os.environ.get('TOKEN')
# client.run(token)
client.run('TOKEN')
