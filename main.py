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


@client.command(aliases=['dp'])
async def deposit(ctx):
    await open_account(ctx.author)
    await ctx.send("Please enter the amount")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    message = await client.wait_for("message", check=check)

    amt = message.content

    bal = await update_bank(ctx.author)

    amt = int(amt)
    if amt > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amt < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1*amt)
    await update_bank(ctx.author, amt, 'bank')
    await ctx.send(f'{ctx.author.mention} You deposited {amt} coins')


@client.command(aliases=['wd'])
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    await ctx.send("Please enter the amount")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    message = await client.wait_for("message", check=check)

    amt = message.content

    bal = await update_bank(ctx.author)

    amt = int(amt)

    if amt > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amt < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, amt)
    await update_bank(ctx.author, -1*amt, 'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amt} coins')


@client.command(aliases=['sm'])
async def send(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    await ctx.send("Please enter the amount")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    message = await client.wait_for("message", check=check)

    amount = message.content

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author, -1*amount, 'bank')
    await update_bank(member, amount, 'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')


@client.command(aliases=['rb'])
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)

    if bal[0] < 100:
        await ctx.send('It is useless to rob him/her :(')
        return

    earning = random.randrange(0, bal[0])

    await update_bank(ctx.author, earning)
    await update_bank(member, -1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')


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
