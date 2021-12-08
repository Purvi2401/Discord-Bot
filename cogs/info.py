import discord
from discord.ext import commands
import psutil


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Info Cog Loaded Succesfully')


def setup(client):
    client.add_cog(Info(client))
