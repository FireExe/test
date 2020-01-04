import os, discord, random, datetime, time, asyncio, json, urllib
from discord.ext.commands import Bot
BOT_PREFIX = os.environ['prefix'] # -Prfix is need to declare a Command in discord ex: !pizza "!" being the Prefix
TOKEN = os.environ['token'] # The token is also substituted for security reasons
Id = os.environ['Id']

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command("help")
QOTD = "None"
lockdown = False
giveawaymessage = "None"
reason = ""
Spam = []
version =  "0.56"

async def status_task():
    while True:
        now = datetime.datetime.now()
        await asyncio.sleep(10)
        if now.hour == 15 and now.minute == 30:
         global QOTD 
         if QOTD != "None":  
          server = discord.utils.get(client.guilds, name='Elemental Soul')
          channel = discord.utils.get(server.channels, name="qotd")
          channel2 = discord.utils.get(server.channels, name="es-bot-manual")
          await channel.send("@everyone "+QOTD+" Don't like pings? Go to "+str(channel2.mention))
          QOTD = "None"
#functions
async def hasperms(ctx,effect,user):
 embed = discord.Embed(
    colour = discord.Colour.orange()
 ) 
 embed.set_author(name=" ")
 embed.add_field(name=":x: User can not be "+effect, value=str(user.name)+" has moderator permissions",inline=False)
 await ctx.send(" ", embed=embed)

async def invalidrole(ctx,role):
  embed = discord.Embed(
     colour = discord.Colour.orange()
  ) 
  embed.set_author(name=" ")
  embed.add_field(name=":x: Invalid role: ", value="'"+role+"' is an invalid role",inline=False)
  await ctx.send(" ", embed=embed)  
    
async def noperms(ctx,command):
  embed = discord.Embed(
     colour = discord.Colour.orange()
  ) 
  embed.set_author(name=" ")
  embed.add_field(name=":x: Lack of permissions", value=str(ctx.message.author.name)+" does not have the permissions to use the `"+command+"` command",inline=False)
  await ctx.send(" ", embed=embed)
    
async def incorrect(ctx,correct):
  embed = discord.Embed(
   colour = discord.Colour.orange()
  ) 
  embed.set_author(name=" ")
  embed.add_field(name=":x: Incorrect usage: ", value=correct,inline=False)
  await ctx.send(" ", embed=embed)
#main

@client.event
async def on_ready():
    activity = discord.Game(name="Elemental Soul")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    server = discord.utils.get(client.guilds, name='Elemental Soul')
    channel = discord.utils.get(server.channels, name="remove-pings")
    #channel2 = discord.utils.get(server.channels, name="general")
    #await channel2.send("Just received an update my version is now "+version)
    await channel.purge(limit=2)
    embed = discord.Embed(
     colour = discord.Colour.orange()
    ) 
    embed.set_author(name="Role Reactions ")
    embed.add_field(name="How to use :", value="React with a reaction corresponding to a role to gain the role and remove the reaction to remove the role ",inline=False)
    embed.add_field(name="For no partner pings react with: ",value="📥",inline=False)
    embed.add_field(name="For no giveway pings react with: ",value="🎁",inline=False)
    embed.add_field(name="For no sneak peek pings react with: ",value="👀",inline=False)
    embed.add_field(name="For no qotd pings react with: ",value="❓",inline=False)
    message = await channel.send(" ", embed=embed)
    await message.add_reaction("📥")
    await message.add_reaction("🎁")
    await message.add_reaction("👀")
    await message.add_reaction("❓")
    client.loop.create_task(status_task())
    
    
@client.command()
async def dm(ctx,role, *, msg):
    if ctx.author.guild_permissions.ban_members:
     embed = discord.Embed(
      colour = discord.Colour.orange()
    )
    embed.set_author(name=" ")
    embed.add_field(name="Message from "+str(ctx.author.name), value=msg,inline=False)
    if role == "all":
      dmrole = discord.utils.get(ctx.guild.roles, name="Bots")
      x = dmrole.members
      z = ctx.guild.members
      for member in z:
        await asyncio.sleep(2)
        if member in x:
         print(str(member.name)+" is a bot")
        else: 
          if member.id == self.client.user.id:
            return
          else:
            try:
              print(member.name)
              await member.send(" ", embed=embed)
            except discord.Forbidden:
              pass
      await ctx.send("Done")
    else:
      role = discord.utils.get(ctx.guild.roles, name=role)
      x = role.members
      for member in x:
          if member.id == self.client.user.id:
            return
          else:
              await member.send(" ", embed=embed)
            
@client.event
async def on_member_join(member):
    if lockdown == False:
     now = datetime.datetime.now()
     channel = discord.utils.get(member.guild.channels, name="welcome")
     role = discord.utils.get(member.guild.roles, name="qotdping")
     role2 = discord.utils.get(member.guild.roles, name="sneakping")
     role3 = discord.utils.get(member.guild.roles, name="giveawayping")
     channel2 = discord.utils.get(member.guild.channels, name="faqs")
     channel3 = discord.utils.get(member.guild.channels, name="es-bot-manual")
     channel4 = discord.utils.get(member.guild.channels, name="log")
     await channel.send("Welcome to Elemental Soul "+str(member.mention)+" Make sure to read "+str(channel2.mention)+" if you have any questions and https://www.roblox.com/groups/4622364/Elemental-Extremes#!/about for the group, also make sure to read "+str(channel3.mention)+" to learn my commands")
     await channel4.send(":inbox_tray:**"+str(member)+"**"+" (ID:"+str(member.id)+") has joined server at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" GMT on the "+str(now.day)+"/"+str(now.month)+"/"+str(now.year))
     await member.add_roles(role)
     await member.add_roles(role2)
     await member.add_roles(role3)
    else:
     await member.send("We're currently under lock down because "+reason)
     await member.kick()
    
   
@client.event
async def on_member_remove(member):
    now = datetime.datetime.now()
    channel = discord.utils.get(member.guild.channels, name="welcome")
    channel2 = discord.utils.get(member.guild.channels, name="log")
    await channel.send("Bye "+str(member.name)+" We hope to see you back at Elemental Soul soon!")
    await channel2.send(":outbox_tray:**"+str(member)+"**"+" (ID:"+str(member.id)+") has left the server at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" GMT on the "+str(now.day)+"/"+str(now.month)+"/"+str(now.year))
    
    
@client.event
async def on_message_delete(before):
    now = datetime.datetime.now()
    embed = discord.Embed(
        colour = discord.Colour.red()
    )
    server = before.guild
    embed.set_author(name=" ")
    embed.add_field(name="Deleted Message:", value=before.content,inline=False)
    channel = discord.utils.get(server.channels, name="log")
    channel2 = discord.utils.get(server.channels, name=str(before.channel))
    await channel.send(""+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" :x:**"+str(before.author)+"**"+" (ID:"+str(before.author.id)+")'s has been deleted from "+str(channel2.mention)+":", embed=embed)

@client.event
async def on_reaction_add(reaction,user):
   server = discord.utils.get(client.guilds, name='Elemental Soul')
   channel = discord.utils.get(server.channels, name="remove-pings")
   if reaction.message.channel == channel:
    if reaction.emoji == "📥":
      role = discord.utils.get(server.roles, name="nopartnerpings")  
      await user.add_roles(role)
      await user.send("You will no longer receive partner pings")
    elif reaction.emoji == "👀":
      role = discord.utils.get(server.roles, name="sneakping")  
      await user.remove_roles(role)
      await user.send("You will no longer receive sneak peek pings")
    elif reaction.emoji == "🎁":
      role = discord.utils.get(server.roles, name="giveawayping")  
      await user.remove_roles(role)
      await user.send("You will no longer receive giveaway pings")
    elif reaction.emoji == "❓":
      role = discord.utils.get(server.roles, name="qotdping")  
      await user.remove_roles(role)
      await user.send("You will no longer receive qotd pings")
        
@client.event
async def on_reaction_remove(reaction,user):
   server = discord.utils.get(client.guilds, name='Elemental Soul')
   channel = discord.utils.get(server.channels, name="remove-pings")
   if reaction.message.channel == channel:
    if reaction.emoji == "📥":
      role = discord.utils.get(server.roles, name="nopartnerpings")  
      await user.remove_roles(role)
      await user.send("You will now receive partner pings")
    elif reaction.emoji == "👀":
      role = discord.utils.get(server.roles, name="sneakping")  
      await user.add_roles(role)
      await user.send("You will now receive sneak peak pings")
    elif reaction.emoji == "🎁":
      role = discord.utils.get(server.roles, name="giveawayping")  
      await user.add_roles(role)
      await user.send("You will now receive giveaway pings")
    elif reaction.emoji == "❓":
      role = discord.utils.get(server.roles, name="qotdping")  
      await user.add_roles(role)
      await user.send("You will now receive qotd pings")
        
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith("https://discord.gg/"):
        if message.author.guild_permissions.kick_members:
            print("Working")
        else:
            await message.delete()
  

    
client.run(TOKEN)



    
