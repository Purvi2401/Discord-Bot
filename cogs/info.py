import discord
from discord.ext import commands
import psutil


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Info Cog Loaded Succesfully')

    @commands.command(aliases=['help'])
    async def _help(self, ctx):
        embedvar = discord.Embed(
            title="Help Commands", description=None, color=0x00ff00)

        embedvar.add_field(name=')balance / )bal',
                           value='To see your balance', inline=False)
        embedvar.add_field(name=')beg',
                           value='To beg some money', inline=False)
        embedvar.add_field(name=')deposit',
                           value='To deposit money in bank', inline=False)
        embedvar.add_field(name=')withdraw',
                           value='To withdraw money from bank', inline=False)
        embedvar.add_field(name=')send',
                           value='Send money to someone', inline=False)
        embedvar.add_field(name=')rob',
                           value='Rob some random money ', inline=False)
        embedvar.add_field(name=')shop', value='To view shop', inline=False)
        embedvar.add_field(name=')buy', value='To, buy an item', inline=False)
        embedvar.add_field(name=')sell', value='To sell an item', inline=False)
        embedvar.add_field(name=')bag',
                           value='To view your shopping cart', inline=False)
        embedvar.add_field(name=')lb',
                           value='To view leaderboard', inline=False)

        await ctx.send(embed=embedvar)


def setup(client):
    client.add_cog(Info(client))
