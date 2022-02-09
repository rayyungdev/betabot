# betabot
Guild Managing Discord Bot: 

This is BetaBot, a discord-guild managing bot. 
Its goal is to make guilds more private by preventing unverified users from having access to a guild's user list and a guild's access to channels. 

v0.0.0:  
  Current Usage Requirements:  
  
      - User Permissions:  
          - Only users with admin permissions can load & unload cogs
          - Only users with manage_channel permissions can use the !delete command
          
      - betabot permissions: 
          - Administrative Permissions
          - Presence Itent == True
          - Members Intent == True
          - Message Content == True 
          - Should have the highest access in terms of hierarchy. 
      
      - Guild needs to have two existing roles and two corresponding channels with the following permissions:
              - No Roles (Role):
                    - This is the default role that all new UNVERIFIED users will get when they first enter the guild. 
                    - As long as this role is above @everyone in the Discord Hierarchy.
                    - ALL permissions should be turned off (from View Channels to Move Members)
                    
              - Introduction (Channel):
                    - Set this channel to private
                          - Only No Roles and betabot should have access to this channel
                                  - No Roles Permissions:
                                          - Send Messages == True
                                          - View Channel == True
                                          - Read Message History == True
                                          - Use Application Commands == True
                                          
              - Verified User Role (Role): 
                      - This is the default role that all new VERIFIED users will get once they are verified by someone within the guild. 
                      - This role should be just above the No Roles in terms of the discord Hierarhcy. 
                              - Least prioritized role above @everyone 
                              
              - New_Users_List (Channel): 
                    - BetaBot will forward messages from the introduction channel to this channel.
                    - Does not require any special permissions, since no role users cannot see other channels. 
                            - Recommended:
                                  - Only BetaBot has access to send messages across this channel
   Set Up:  
   
   
      - create .env file to set these variables: 
              - DISCORD_TOKEN = bot token ID
              - DISCORD_GUILD = Guild name
              - CONNECTION_URL = None (for future work) 
              
              Set these variables to 0 during first installation. You can get this information using the !channel_name command aftewards. 
              - INTRO_CHANNEL_ID = Introduction Channel ID  
              - NEW_USER_CHANNEL_ID = New User List Channel ID 
              - NO_ROLE_ID = No Role ID number
              - ROLE_ID = Role ID number
          
  Future Updates:   
  
  
        - Currently working on setting up new cog: guild_setup 
              - Goal is to create the two roles and channels to streamline the process
              - Use database to upload variable information so that the bot can manage multiple guilds. 
        - Ping specific roles when an unverified user makes messages the server based on their introduction. 
