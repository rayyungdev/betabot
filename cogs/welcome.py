import asyncio
import re
from shutil import ExecError
from socket import timeout
import discord
from discord.ext import commands
import sys
sys.path.append('../bbot')
from db_setup import *

'''
    Fine tuning: 
    - Connect to database to save private information like id (Role, User, etc)
    - Change hard coded id numbers & roles as variables pulled from databases.

    - Create a cog that sets up guilds with the following functions:
        - Function creates specific channels (intro & new members) stores ID into DB
        - Function that creates the two standard roles (role & no roles) stores ID into DB
'''

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.introductions = 941055150481633310
        self.nlist = id=940778970964705340
        self.approval_reactions = {'thumbsup': '\U0001F44D', 'thumbsdown':'\U0001F44E'}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.client.user)
        print('ID:', self.client.user.id)
    
    @commands.command()
    async def channel_name(self, ctx):
        print(ctx.guild.text_channels)
        print(ctx.guild.roles)

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        ## Wasn't working because needed intents to be on
        ## Want to find way to automate the role id... or create stuff on a whim, who knows
        if len(member.roles) > 1:
            return
        
        no_role = discord.utils.get(self.client.get_guild(member.guild.id).roles, id = 938532676602843166)
        role = discord.utils.get(self.client.get_guild(member.guild.id).roles, id = 938529963638919168)
        new_user_channel = self.client.get_channel(self.nlist)
        intro_channel = self.client.get_channel(self.introductions)

        channel = member.guild.system_channel
        await member.add_roles(no_role)
        await channel.send('Welcome {0.mention}, please introduce yourself with your name'.format(member))
        
        def check_msg(message):  
            return (message.author != self.client.user) and (not message.content.startswith('!')) and (message.channel.id == self.introductions) and (message.author == member)
        
        try: 
            #Time out set to 5 minutes
            msg = await self.client.wait_for('message', check = check_msg, timeout = 300)
        except asyncio.TimeoutError:
            msg = f'Sorry {member.name}, we have not recieved an introduction and are unable to verify your identify. Please try again with a different invitation'
            await member.send(msg)
            await member.kick()
            await intro_channel.purge()
            return

        except Exception as e:
            msg = f'Sorry {member.name}. Something went wrong on our end. Please try again with a different invitation'
            await member.send(msg)
            await member.kick()
            await intro_channel.purge()
            return

        # Do not need to check if user has roles, as this only runs for new users. 

        response = await new_user_channel.send(f'***New Member Alert!***\nUsername: **[{msg.author}]** \nthis is their message:\n\n> {msg.content}\n\n**Do you want to approve?** \n*(react with thumbsup or thumbsdown)*')
        for key, value in self.approval_reactions.items():
            await response.add_reaction(value)

        def check(reaction, user):
            #Check if reaction is in approved reactions. I'll change it so there is no inheritance for this
            return reaction.emoji in self.approval_reactions.values() and reaction.message.id ==response.id and user != self.client.user

        # Wait 5 minutes for a response
        try: 
            reaction, user = await self.client.wait_for('reaction_add', timeout = 300, check=check)
        except asyncio.TimeoutError:
            msg = f'Sorry {member.name}, no one was able to approve your membership at this time.\nPlease try again with another invitation'
            await member.send(msg)
            await member.kick()
            await new_user_channel.send(f'*User {member} has been kicked due to lack of approval*')
            await intro_channel.purge()
            return
            
        except Exception as e:
            msg = f'Sorry {member.display_name}, no one was able to approve your membership at this time.\nPlease try again with another invitation'
            await member.send(msg)
            await member.kick()
            await new_user_channel.send(f'*User {member} has been kicked due to lack of approval*')
            await intro_channel.purge()
            print(f'Error occured at {e}')
            return
        
        if reaction.emoji == self.approval_reactions.get('thumbsup'):
            await member.add_roles(role)
            await member.remove_roles(no_role)
            await new_user_channel.send(f'***Congratulations <@{member.id}>, you have been approved!***')

        elif reaction.emoji == self.approval_reactions.get('thumbsdown'):
            await member.kick()
            await new_user_channel.send(f'***User {member} has been kicked***')
        
        await intro_channel.purge()

    # Generalize Role Name
    @commands.command()
    @commands.has_guild_permissions(manage_messages = True)
    async def delete(self, ctx, amount = None):
        await ctx.channel.purge(limit = amount)

def setup(client):
    client.add_cog(welcome(client))
