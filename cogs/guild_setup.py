import discord
from discord.ext import commands
import sys
sys.path.append('../bbot')
from db_setup import *
import asyncio

'''
    Functions to keep in mind:
        - Create function to provide all existing users the default role
        - Create factory reset
        - Still need to store data into database so that other cogs can pull the same information (or I can just put everything into one cog)
'''
class guild_setup(commands.Cog, description = 'Guild Channel and Role Setup'):
    def __init__(self, client):
        self.client = client
        self.unval_role = None
        self.val_role = None
    @commands.command(brief = 'Create Standard Default Roles',
     description = 'this function is used to create two standard roles, one for unvalidated users and one for validated users\nFor example:\n>    !role_setup unvalidated_role_name, validated_role_name.\n Please note that the permissions will not be set up until you use the !channel_setup command')
    
    @commands.has_guild_permissions(administrator = True)
    async def role_setup(self, ctx, *arg):
        if len(arg) > 2:
            await ctx.send(f'Too many arguments. This function only creates two roles')
            return
        if len(arg) <= 1:
            await ctx.send(f'Not enough arguments. This function creates two roles')
            return
        if len(arg) == 0:
            await ctx.send(f'this function creates two roles. One for validated and another for unvalidated users.')
            return
        if arg[0] == arg[1]:
            await ctx.send(f'Roles cannot have the same name')
            return
        unvalidated_users = arg[0]  # Unvalidated Users
        validated_users = arg[1]    # Validated Users

        test_1 = discord.utils.get(self.client.get_guild(ctx.guild.id).roles, name = unvalidated_users)
        test_2 = discord.utils.get(self.client.get_guild(ctx.guild.id).roles, name = validated_users)

        if test_1 != None or test_2 != None:
            await ctx.send('These roles already exist. Please try again with unique role names')
            return

        response = await ctx.send(f'*None-Validated Role Name*:\n>  **{unvalidated_users}**\n*Validated Role Name*:\n>  **{validated_users}**\nIs this correct?')
        approval_reactions = {'thumbsup': '\U0001F44D', 'thumbsdown':'\U0001F44E'}
       
        for key, value in approval_reactions.items():
            await response.add_reaction(value)
       
        def check(reaction, user):
            return reaction.emoji in approval_reactions.values() and reaction.message.id ==response.id and user == ctx.author

        try: 
            reaction, user = await self.client.wait_for('reaction_add', timeout = 60, check=check)
        except asyncio.TimeoutError:
            msg = f'Sorry {ctx.id}, I did not get a response in time. Please use the command again and react appropiately'
            ctx.send(msg)
            return
            
        except Exception as e:
            msg = f'Sorry {ctx.id}, Something went wrong. Please use the command again and react appropiately'
            ctx.send(msg)
            return

        if reaction.emoji == approval_reactions.get('thumbsdown'):
            msg = f'Please use this command again if you would like to try this again'
            await ctx.send(msg)
            return
        unval_perms = discord.Permissions.none()
        default_perms = discord.Permissions(read_messages = True, read_message_history = True, send_messages = True, send_tts_messages = True, add_reactions = True, change_nickname = True, speak = True)
        await ctx.guild.create_role(name = unvalidated_users, permissions = unval_perms)
        await ctx.guild.create_role(name = validated_users, permissions = default_perms)

        ## Store this into database when I get it working
        self.unval_role = discord.utils.get(self.client.get_guild(ctx.guild.id).roles, name = unvalidated_users)
        self.val_role = discord.utils.get(self.client.get_guild(ctx.guild.id).roles, name = validated_users)
        
        await self.unval_role.edit(position = 1)
        await self.val_role.edit(posiion = 2)
        await ctx.send(f'Roles have successfully been created')
        return

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def channel_setup(self, ctx, intro_channel, new_list_channel):
        if self.unval_role == None or self.val_role == None:
            await ctx.send(f'You must use !role_setup to create roles before you can set up the channels.')
            return
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            self.unval_role: discord.PermissionOverwrite(read_messages = True, read_message_history = True, view_channel = True, send_messages = True)
        }

        await ctx.guild.create_category('new-user-introductions', overwrites = overwrites, position = 0)
        intro = discord.utils.get(ctx.guild.categories, name = 'new-user-introductions')
        await ctx.guild.create_text_channel(intro_channel, category = intro)

        await ctx.guild.create_category('incoming-members', position = 1)
        incoming = discord.utils.get(ctx.guild.categories, name = 'incoming-members')
        await ctx.guild.create_text_channel(new_list_channel, category = incoming)

        self.unval_role = None
        self.val_role = None
        return
def setup(client):
    client.add_cog(guild_setup(client))