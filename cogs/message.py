import discord
from discord.ext import commands
import sys
sys.path.append('../../messaging')
from db_setup import *
from dotenv import load_dotenv
import os
from account_setup import *

load_dotenv()
sender_address = os.getenv('MY_ADDRESS')

password = os.getenv('PASSWORD ')
class message(commands.Cog, description = 'Notification Email Cog'):
    def __init__(self, client):
        self.client = client

    @commands.command(brief = "email command", description = "send email through discord")
    @commands.has_guild_permissions(administrator = True)
    async def email(self, ctx):
        await ctx.send(f'What is the address you''d like to send to?')
        def check(message):
            return (message.author == ctx.author) and (message.channel == ctx.channel)
        reciever = await self.client.wait_for("message", check = check, timeout = 30)

        await ctx.send(f'What is the subject of this message?')
        subj = await self.client.wait_for("message", check = check, timeout = 30)

        await ctx.send(f'What is the message for {reciever.content}')
        msg = await self.client.wait_for("message", check = check, timeout = 30)
        
        try: 
            mail_msg = message_make(msg.content, subj.content)
            await ctx.send(f'This is the email: \n{mail_msg}')

            email(mail_msg, reciever.content)
            await ctx.send(f'Email sent')
        except Exception as e:
            print(e)
def setup(client):  
    client.add_cog(message(client))