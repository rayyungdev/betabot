import asyncio
import discord
from discord.ext import commands
import sys
sys.path.append('../bbot')
from db_setup import *
from dotenv import load_dotenv

'''
    Fine tuning: 
    - Connect to database to load and save private information... Still need to find a way to share the variables created from the guild_setup cog
'''
load_dotenv()

'''
Use function !channel_name to view your role information. 
This will be printed in terminal for privacy. 

Plug the corresponding ID's into your .env file. 
'''
INTRO_CHANNEL_ID = int(os.getenv('INTRO_CHANNEL_ID'))
NEW_USER_CHANNEL_ID = int(os.getenv('NEW_USER_CHANNEL_ID'))
NO_ROLE_ID= int(os.getenv('NO_ROLE_ID'))
ROLE_ID = int(os.getenv('ROLE_ID'))

class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.intro_channel = INTRO_CHANNEL_ID
        self.new_user_list_channel = NEW_USER_CHANNEL_ID
        self.no_role = NO_ROLE_ID
        self.role = ROLE_ID

        self.approval_reactions = {'thumbsup': '\U0001F44D', 'thumbsdown':'\U0001F44E'}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ---->', self.client.user)
        print('ID:', self.client.user.id)
    
    @commands.command()
    async def channel_name(self, ctx):
        print(f'Channel Information: \n {ctx.guild.text_channels}\n')
        print(f'Role Information: \n{ctx.guild.roles}')

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        ## Wasn't working because needed intents to be on
        ## Want to find way to automate the role id... or create stuff on a whim, who knows
        if len(member.roles) > 1:
            return
        
        no_role = discord.utils.get(member.guild.roles, id = self.no_role)
        role = discord.utils.get(member.guild.roles, id = self.role)

        new_user_channel = self.client.get_channel(self.new_user_list_channel)
        intro_channel = self.client.get_channel(self.intro_channel)

        await member.add_roles(no_role)
        await intro_channel.send('Welcome {0.mention}, please introduce yourself with your name'.format(member))
        
        def check_msg(message):  
            return (message.author != self.client.user) and (not message.content.startswith('!')) and (message.channel.id == self.intro_channel) and (message.author == member)
        
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

        response = await new_user_channel.send(f'@here\n***New Member Alert!***\nUsername: **[{msg.author}]** \nthis is their message:\n\n> {msg.content}\n\n**Do you want to approve?** \n*(react with thumbsup or thumbsdown)*')
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
        return

    # Generalize Role Name
    @commands.command(brief = 'Clear Chat History')
    @commands.has_guild_permissions(manage_messages = True)
    async def delete(self, ctx, amount = None):
        await ctx.channel.purge(limit = amount)
        return
def setup(client):
    client.add_cog(welcome(client))