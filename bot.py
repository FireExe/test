import os, discord, random, datetime, time, asyncio, json, urllib
from discord.ext.commands import Bot

# We'll need to substitute the Prefix for an Enviroment Variable
BOT_PREFIX = os.environ['prefix'] # -Prfix is need to declare a Command in discord ex: !pizza "!" being the Prefix
TOKEN = os.environ['token'] # The token is also substituted for security reasons
Id = os.environ['Id']

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command("help")
# this is an event which is triggered when something happens in Discord 
# in this case on_ready() is called when the bot logs on
#you can checkthe Discord API Documentaion for more event Functions 
# here: https://discordapp.com/developers
QOTD = "None"
lockdown = False
giveawaymessage = "None"
reason = ""
Spam = []

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
def perms():
  print("egg")

def invalidrole(cn,role):
  server = discord.utils.get(client.guilds, name='Elemental Soul')
  channel = discord.utils.get(server.channels, name=cn)
  embed = discord.Embed(
     colour = discord.Colour.orange()
  ) 
  embed.set_author(name=" ")
  embed.add_field(name=":x: Invalid role: ", value="'"+role+"' is an invalid role",inline=False)
  await channel.send(" ", embed=embed)  
#main

@client.event
async def on_ready():
    activity = discord.Game(name="Elemental Soul")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.loop.create_task(status_task())
    
    
# below this line you can put custom Functions
@client.command()
async def roasts(ctx):
   if ctx.message.channel.name == "roasts":
    choices = [
     "You should eat some of that make up, to be pretty on the inside",
     "Can you stop making that disgusting sound, oh wait... it's your voice",
     "Your unseasoned",
     "You have one brain cell and it's fighting for dominance",
     "Your lips are drier then the sahara",
     "Your knees are ashier then the skin of kfc chicken",
     "Your face has be censored when ever it's on camera to prevent the trauma of seeing it",
     "You bring everyone a lot of joy, when you leave the room",
     "I would sue your barber if i were you, that haircut is more then an insult",
     "I would insult you but nature did a better job.",
     "Two wrongs don't make a right, take your parents as an example",
     "I don't care about your short comings, but your long stayings",
     "I would try hurt you instead of roasting, but it would be considered animal abuse",
     "You are the reason the gene pool needs a lifeguard",
     "It's a waste of time trying to cuss something so irrelevant",
     "I'm jealous of people that don't know you",
     "A million years of evolution and we get you",
     "I've got more brain cells then you and i'm just lines of code",
     "I'd tell you to go outside, but you'd just ruin that for everyone else too",
     "To which foundation do I need to donate to help you?",
     "I thought i was ugly but evolution really took a step back with you",
     "It must have been a sad day when you crawled from the abortion bucket",
     "Maybe you should try something more on your level, like rock-paper-scissors",
     "WOW! imagine if your parents weren't siblings",
     "Nooooob",
     "With aim like that, I pity whoever has to clean the floor around your toilet"
    ]
    await ctx.send(random.choice(choices))
   else:
    channel = discord.utils.get(ctx.message.guild.channels, name="roasts")
    await ctx.send("I only do roasts in "+str(channel.mention))

    
@client.command()
async def version(ctx):
    await ctx.send("Elemental Soul Bot v.1.7 by >Fire.Exe")

@client.command()
async def rolecount(ctx,role):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 role = discord.utils.get(ctx.message.guild.roles, name=role)
 num = 0
 x = role.members
 for member in x:
    num = num + 1
 embed.set_author(name=" ")
 embed.add_field(name="Users in "+str(role)+":", value=num,inline=False)
 await ctx.send(" ", embed=embed)

@client.command()
async def dm(ctx,role, *, msg):
  if ctx.message.author.guild_permissions.ban_members:
   embed = discord.Embed(
        colour = discord.Colour.orange()
   )
   embed.set_author(name=" ")
   embed.add_field(name="Message from "+str(ctx.message.author.name), value=msg,inline=False)
   if role == "all":
    dmrole = discord.utils.get(ctx.message.guild.roles, name="Bots")
    x = dmrole.members
    z = ctx.guild.members
    for member in z:
      if member in x:
       print(str(member.name)+" is a bot")
      else: 
         if member.id == client.user.id:
          return
         else:
            await member.send(" ", embed=embed)
   else:
    role = discord.utils.get(ctx.message.guild.roles, name=role)
    x = role.members
    for member in x:
         if member.id == client.user.id:
          return
         else:
            await member.send(" ", embed=embed)
           
@client.command()
async def dm_user(ctx,member: discord.Member, *, msg):
  print(str(ctx.message.author.id))
  if int(ctx.message.author.id) == int(Id):
   embed = discord.Embed(
        colour = discord.Colour.orange()
   )
   embed.set_author(name=" ")
   embed.add_field(name="Message from the void", value=msg,inline=False)
   await member.send(" ", embed=embed)
    
@client.command()
async def square(ctx, num : int):
    await ctx.send(num*num)
    await ctx.send(str(ctx.message.author))
    
    
@client.command(pass_content=True)
async def assign(ctx, left: str):
       user = ctx.message.author
       server = ctx.message.guild
       role = discord.utils.get(server.roles, name=left)
       if ctx.message.channel.name != "general" and ctx.message.channel.name != "qotd-answers" and ctx.message.channel.name != "roasts" and ctx.message.channel.name != "memes": 
        if left  == "nopartnerpings":
          await ctx.send("You will no longer receive partner pings " + str( user.name))
          await user.add_roles(role)
        elif left  == "qotdping":
          await ctx.send("You will now receive QOTD pings " + str( user.name))
          await user.add_roles(role)
        elif left  == "sneakping":
          await ctx.send("You will now receive sneak peak pings " + str( user.name))
          await user.add_roles(role)
        else:
          invalidrole(ctx.name,left)
     
@client.command(pass_content=True)
async def unassign(ctx, left: str):
       user = ctx.message.author
       server = ctx.message.guild
       role = discord.utils.get(server.roles, name=left)
       if ctx.message.channel.name != "general" and ctx.message.channel.name != "qotd-answers" and ctx.message.channel.name != "roasts" and ctx.message.channel.name != "memes":
        if left  == "nopartnerpings":
          await ctx.send("You will now recieve partner pings " + str( user.name))
          await user.remove_roles(role)
        elif left  == "qotdping":
          await ctx.send("You will no longer receive QOTD pings " + str( user.name))
          await user.remove_roles(role)
        elif left  == "sneakping":
          await ctx.send("You will no longer receive sneak peak pings " + str( user.name))
          await user.remove_roles(role)
        else:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: Invalid role: ", value="'"+left+"' is an invalid role",inline=False)
         await ctx.send(" ", embed=embed)
@client.command(pass_content=True)
async def kick(ctx, user: discord.Member):
    if user.guild_permissions.kick_members:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: User can not be kicked", value=str(user.name)+" has moderator permissions",inline=False)
         await ctx.send(" ", embed=embed)
    else:
        if ctx.message.author.guild_permissions.kick_members:
         await ctx.send(str(user.name)+" has been kicked")
         await user.kick()
        else:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: Lack of permissions", value=str(ctx.message.author.name)+" does not have the permissions to use the `kick` command",inline=False)
         await ctx.send(" ", embed=embed)
            
            
@client.command(pass_content=True)      
async def qotd(ctx, *, qotd):
        if ctx.message.author.guild_permissions.ban_members:
         user = ctx.message.author
         await ctx.send(str(user.name)+" has set the qotd to "+qotd)
         global QOTD 
         QOTD = qotd
        
@client.command(pass_content=True)
async def ban(ctx, user: discord.Member):
    if user.guild_permissions.kick_members:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: User can not be banned", value=str(user.name)+" has moderator permissions",inline=False)
         await ctx.send(" ", embed=embed)
    else:
        if ctx.message.author.guild_permissions.ban_members:
         await ctx.send(str(user.name)+" has been banned")
         await user.ban()
        else:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: Lack of permissions", value=str(ctx.message.author.name)+" does not have the permissions to use the `ban` command",inline=False)
         await ctx.send(" ", embed=embed)
            
            
@client.command(pass_content=True)   
async def mute(ctx, user: discord.Member):
    if user.guild_permissions.kick_members:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: User can not be muted", value=str(user.name)+" has moderator permissions",inline=False)
         await ctx.send(" ", embed=embed)
    else:
      if ctx.message.author.guild_permissions.kick_members:
         server = ctx.message.guild
         role = discord.utils.get(server.roles, name="Muted")
         await ctx.send(str(user.name)+" has been muted")
         await user.add_roles(role)
      else:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: Lack of permissions", value=str(ctx.message.author.name)+" does not have the permissions to use the `mute` command",inline=False)
         await ctx.send(" ", embed=embed)
     
@client.command()
async def lock(ctx):
   if ctx.message.author.guild_permissions.ban_members:
    await ctx.send("This channel will be locked until the command /unlock is used")
    rolesearch = discord.utils.get(ctx.message.guild.roles, name="Community")
    await ctx.message.channel.set_permissions(rolesearch, send_messages=False)
   else:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: Lack of permissions", value=str(ctx.message.author.name)+" does not have the permissions to use the `lock` command",inline=False)
         await ctx.send(" ", embed=embed)
    
@client.command()
async def unlock(ctx):
   if ctx.message.author.guild_permissions.ban_members:
    await ctx.send("This channel will be unlocked until the command /lock is used")
    rolesearch = discord.utils.get(ctx.message.guild.roles, name="Community")
    await ctx.message.channel.set_permissions(rolesearch, send_messages=True)
   else:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: Lack of permissions", value=str(ctx.message.author.name)+" does not have the permissions to use the `unlock` command",inline=False)
         await ctx.send(" ", embed=embed)
     
@client.command(pass_content=True)   
async def unmute(ctx, user: discord.Member):
    if user.guild_permissions.kick_members:
         embed = discord.Embed(
          colour = discord.Colour.orange()
         ) 
         embed.set_author(name=" ")
         embed.add_field(name=":x: User can not be muted", value=str(user.name)+" has moderator permissions",inline=False)
         await ctx.send(" ", embed=embed)
    else:
        if ctx.message.author.guild_permissions.kick_members:
         server = ctx.message.guild
         role = discord.utils.get(server.roles, name="Muted")
         await ctx.send(str(user.name)+" has been unmuted")
         await user.remove_roles(role)
            
@client.command(pass_content=True)   
async def roleall(ctx, left: str = None):
      server = ctx.message.guild
      if left:
        role = discord.utils.get(server.roles, name=left)
        if role == None:
          embed = discord.Embed(
           colour = discord.Colour.orange()
          ) 
          embed.set_author(name=" ")
          embed.add_field(name=":x: Invalid role: ", value="'"+left+"' is an invalid role",inline=False)
          await ctx.send(" ", embed=embed)  
        else:
         if ctx.message.author.guild_permissions.ban_members:
          await ctx.send("I'm gonna start giving everyone the "+left+" role and i'll notify you when i'm done :gear:")
          x = server.members
          for member in x:
            await member.add_roles(role)
          await ctx.send(""+str(ctx.message.author.mention)+" I've roled everyone :+1:")
         else:
          embed = discord.Embed(
           colour = discord.Colour.orange()
          ) 
          embed.set_author(name=" ")
          embed.add_field(name=":x: Incorrect usage: ", value="/roleall [role]",inline=False)
          await ctx.send(" ", embed=embed)
        
        
@client.command(pass_content=True)
async def help(ctx):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
  
 embed.set_author(name="Help")
 embed.add_field(name="/help", value="Shows this message",inline=False)
 embed.add_field(name="/modhelp", value="Shows moderation commands",inline=False)
 embed.add_field(name="/roasts", value="Get roasted",inline=False)
 embed.add_field(name="/blackjack", value="Play some blackjack",inline=False)
 embed.add_field(name="/group", value="Get the group link",inline=False)
 embed.add_field(name="/version", value="Checks my version",inline=False)
 embed.add_field(name="/assign", value="Give yourself a role",inline=True)
 embed.add_field(name="Example:", value="/assign QOTDping",inline=True)
 embed.add_field(name="/unassign", value="Remove a role from yourself",inline=False)
 embed.add_field(name="Example:", value="/unassign QOTDping",inline=True)
 embed.add_field(name="/membercount", value="Shows the amount of people in the server",inline=False)
 embed.add_field(name="/donate", value="Donate to the game",inline=False)
 await ctx.send("Here's all the commands and their uses:", embed=embed)
    
    
@client.command(pass_content=True)
async def modhelp(ctx):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 embed.set_author(name="Moderator Help")
 embed.add_field(name="/modhelp", value="Shows this message",inline=False)
 embed.add_field(name="/kick", value="Kick a user",inline=True)
 embed.add_field(name="Example:", value="/kick Hstist",inline=True)
 embed.add_field(name="/ban", value="Ban a user",inline=False)
 embed.add_field(name="Example:", value="/ban Hstist",inline=True)
 embed.add_field(name="/lock", value="Locks the channel the command was used in",inline=False)
 embed.add_field(name="/unlock", value="Unlocks the channel the command was used in",inline=False)
 embed.add_field(name="/lockserver", value="Locks or unlocks the server depending on it's current state",inline=False) 
 embed.add_field(name="/mute", value="Mutes the chosen user",inline=True)
 embed.add_field(name="Example:", value="/mute Hstist",inline=True)
 embed.add_field(name="/unmute", value="Unmutes the chosen user",inline=True)
 embed.add_field(name="Example:", value="/unmute Hstist",inline=True)
 await ctx.send("Here's all the moderation commands and their uses:", embed=embed)
        
    
@client.command(pass_content=True)
async def membercount(ctx):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 x = ctx.guild.members
 num = 0
 for member in x:
    num = num + 1
 embed.set_author(name=" ")
 embed.add_field(name="Users: ", value=num,inline=False)
 await ctx.send(" ", embed=embed)


    
@client.command(pass_content=True)
async def donate(ctx, amount : int = None):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 num = 0
 if amount:
  if  amount > 999: 
   embed.set_author(name=" ")
   embed.add_field(name="Large donations ", value="https://www.roblox.com/catalog/2693098576/Large-Donations",inline=False)
   await ctx.message.author.send(" ", embed=embed)
  elif amount > 499: 
   embed.set_author(name=" ")
   embed.add_field(name="Medium donations ", value="https://www.roblox.com/catalog/2693097087/Medium-Donations",inline=False)
   await ctx.message.author.send(" ", embed=embed)
  elif amount > 99: 
   embed.set_author(name=" ")
   embed.add_field(name="Small donations ", value="https://www.roblox.com/catalog/2693095047/Small-Donations",inline=False)
   await ctx.message.author.send(" ", embed=embed)
  elif amount > 49:
   embed.set_author(name=" ")
   embed.add_field(name="Micro donations ", value="https://www.roblox.com/catalog/2693093169/Micro-Donation",inline=False)
   await ctx.message.author.send(" ", embed=embed)
  else:
   embed.set_author(name=" ")
   embed.add_field(name=":x: Sorry", value="That donation is to small, 50 is the minimum",inline=False)
   await ctx.message.author.send(" ", embed=embed)
 else:
  embed.set_author(name=" ")
  embed.add_field(name=":x: Incorrect usage: ", value="/donate [amount]",inline=False)
  await ctx.send(" ", embed=embed)
    
@client.command(pass_content=True)
async def winner(ctx, item : str , user : discord.Member):
 if ctx.message.author.guild_permissions.ban_members:
  embed = discord.Embed(
        colour = discord.Colour.orange()
  )
  server = discord.utils.get(client.guilds, name='Bot making')
  channel = discord.utils.get(server.channels, name="weapon-winner-log")  
  embed.set_author(name=" ")
  embed.add_field(name="Added", value= str(user)+" has been added to the list of winners and their item won is the "+item,inline=False)
  await ctx.send(" ", embed=embed)
  await channel.send(" ", embed=embed)

@client.command(pass_content=True)
async def lockserver(ctx,res : str = None):
 if res:
  if ctx.message.author.guild_permissions.ban_members:  
    global reason
    global lockdown
    reason = res
    if lockdown == True:
        lockdown = False
        await ctx.send("The server will be unlocked until this command is used again")
    else:
        lockdown = True
        await ctx.send("The server will be locked until this command is used again")
    
 else:
  embed = discord.Embed(
        colour = discord.Colour.orange()
  ) 
  embed.set_author(name=" ")
  embed.add_field(name=":x: Incorrect usage: ", value="/lockserver [reason]",inline=False)
  await ctx.send(" ", embed=embed)
    
@client.command(pass_content=True)
async def group(ctx, amount : int = None):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 embed.set_author(name=" ")
 embed.add_field(name="Group", value="https://www.roblox.com/My/Groups.aspx?gid=4622364",inline=False)
 await ctx.message.author.send(" ", embed=embed)
   

@client.command(pass_content=True)
async def trello(ctx, amount : int = None):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 embed.set_author(name=" ")
 embed.add_field(name="Trello", value="https://trello.com/b/8aprufdU/elemental-soul",inline=False)
 await ctx.message.author.send(" ", embed=embed)
    
@client.command(pass_content=True)
async def activegiveaway(ctx):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 guild = ctx.message.guild
 channel =discord.utils.get(guild.channels, name="giveaways")
 embed.set_author(name=" ")
 embed.add_field(name="Test Giveaway", value="Giveaway ends in 10 seconds boi",inline=False)
 msg = await channel.send("React with :tada: to join the giveaway", embed=embed)
 await msg.add_reaction(emoji="🎉")
 global giveawaymessage
 giveawaymessage = msg
 await asyncio.sleep(10)
 giveawaymessage = "None"
 
@client.command(pass_content=True)
async def blackjack(ctx): 
    playervalue = 0
    computervalue =0
    strike = 0
    cards = [
        "Ace of clubs","Ace of diamonds","Jack of hearts","Jack of spades","Queen of clubs","Queen of hearts","King of spades",
        "King of diamonds","3 of clubs","5 of clubs","1 of diamonds","8 of diamonds","4 of spades","6 of spades","7 of hearts",
        "9 of hearts","1 of hearts","3 of diamonds"
    ]
    values = [
        10,10,10,10,10,10,10,10,3,5,1,8,4,6,7,9,1,3  
    ]
    playercards = []
    computercards = []
    for x in range(0,2):
        cardnum = -1
        for item in cards:
            cardnum = cardnum + 1
        num = random.randint(0,cardnum)
        playervalue = playervalue + values[num]
        playercards.append(cards[num])
        cards.remove(cards[num])
        values.remove(values[num])
    await ctx.send("Your starting deck is worth "+str(playervalue)+" and consists of...")
    for item in playercards:
           await ctx.send(item)
    for x in range(0,2):
        cardnum = -1
        for item in cards:
            cardnum = cardnum + 1
        num = random.randint(0,cardnum)
        computervalue = computervalue + values[num]
        computercards.append(cards[num])
        cards.remove(cards[num])
        values.remove(values[num])
    await ctx.send("And mine is worth "+str(computervalue))
    while computervalue < 21 and playervalue < 21 and strike < 2:
            cardnum = -1
            for item in cards:
             cardnum = cardnum + 1
            num = random.randint(0,cardnum)
            await ctx.send("Hit[H] or Stand[S]")
            card = await client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
            card = card.content.lower()
            if card == "H" or card == "h" or card == "hit" or card == "Hit":
                await ctx.send("I've drawn "+cards[num]+" for you")
                playercards.append(cards[num])
                playervalue = playervalue + values[num]
                cards.remove(cards[num])
                values.remove(values[num])
                await ctx.send("Your hand is now worth "+str(playervalue))
            elif card == "S" or card == "s" or card == "stand" or card == "Stand":
                 await ctx.send("You don't get a card then")
            else:
                 await ctx.send("I don't know that action")
                 strike = strike + 1
            choice = random.randint(0,1)
            if choice ==1:
             cardnum = -1
             for item in cards:
                 cardnum = cardnum + 1
             num = random.randint(0,cardnum)
             computervalue = computervalue + values[num]
             computercards.append(cards[num])
             cards.remove(cards[num])
             values.remove(values[num])
             await ctx.send("I'm hitting")
             await ctx.send("My hand is now worth "+str(computervalue))
            else:
             await ctx.send("I'm standing")
    if strike == 2:
      await ctx.send("I win because your just spamming random keys")  
    elif playervalue == 21:
       await ctx.send("You win")
    elif playervalue > 21:
        await ctx.send("You've bust so i win")
    elif computervalue == 21:
        await ctx.send("I win")
    elif computervalue > 21:
        await ctx.send("I've bust so you win")
                                     
        
    
@client.event
async def on_reaction_add(reaction, user):
   print("a reaction was added by")
   if giveawaymessage != "None":
    if reaction.message == giveawaymessage:
        guild = ctx.message.guild
        channel =discord.utils.get(guild.channels, name="giveaways")
        channel.send(str(user.mention)+" has joined the active giveaway")
        
        
        
@client.event
async def on_member_join(member):
    if lockdown == False:
     now = datetime.datetime.now()
     channel = discord.utils.get(member.guild.channels, name="welcome")
     role = discord.utils.get(member.guild.roles, name="qotdping")
     role2 = discord.utils.get(member.guild.roles, name="sneakping")
     channel2 = discord.utils.get(member.guild.channels, name="faqs")
     channel3 = discord.utils.get(member.guild.channels, name="es-bot-manual")
     channel4 = discord.utils.get(member.guild.channels, name="log")
     await channel.send("Welcome to Elemental Soul "+str(member.mention)+" Make sure to read "+str(channel2.mention)+" if you have any questions and https://www.roblox.com/groups/4622364/Elemental-Extremes#!/about for the group, also make sure to read "+str(channel3.mention)+" to learn my commands")
     await channel4.send(":inbox_tray:**"+str(member)+"**"+" (ID:"+str(member.id)+") has joined server at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" GMT on the "+str(now.day)+"/"+str(now.month)+"/"+str(now.year))
     await member.add_roles(role)
     await member.add_roles(role2)
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
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith("https://discord.gg/"):
        if message.author.guild_permissions.kick_members:
            print("Working")
        else:
            await message.delete()
  

    
client.run(TOKEN)



    
