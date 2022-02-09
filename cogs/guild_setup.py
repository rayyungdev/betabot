import re
import discord
from discord.ext import commands
import sys
sys.path.append('../bbot')
from db_setup import *

class guild_setup(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def role_setup(self, ctx, *arg):
        if len(arg) > 2:
            await ctx.send(f'Too many arguments. This function only creates two roles')
            return
        if len(arg) == 1:
            await ctx.send(f'Not enough arguments. This function creates two roles')
            return
        if len(arg) == 0:
            await ctx.send(f'this function is used to create two standard roles, one for unvalidated users and one for validated users')
            await ctx.send(f'For example:\n>    !role_setup unvalidated_role_name, validated_role_name')
            return
        if arg[0] == arg[1]:
            await ctx.send(f'Roles cannot have the same name')
            return

        unvalidated_users = arg[0]
        validated_users = arg[1]
        response = await ctx.send(f'*None-Validated Role Name*:\n>  **{unvalidated_users}**\n*Validated Role Name*:\n>  **{validated_users}**\nIs this correct?')
        approval_reactions = {'thumbsup': '\U0001F44D', 'thumbsdown':'\U0001F44E'}
        for key, value in approval_reactions.items():
            await response.add_reaction(value)
        def check(reaction, user):
            return None
    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def channel_setup(self, ctx):
        guild = ctx.message.guild


def setup(client):
    client.add_cog(guild_setup(client))