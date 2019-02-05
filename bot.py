import os, discord, random, datetime, time, asyncio, json
from discord.ext.commands import Bot

# We'll need to substitute the Prefix for an Enviroment Variable
BOT_PREFIX = os.environ['prefix'] # -Prfix is need to declare a Command in discord ex: !pizza "!" being the Prefix
TOKEN = os.environ['token'] # The token is also substituted for security reasons

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command("help")
# this is an event which is triggered when something happens in Discord 
# in this case on_ready() is called when the bot logs on
#you can checkthe Discord API Documentaion for more event Functions 
# here: https://discordapp.com/developers
QOTD = "None"
data = {}
data["User"]=[]
giveawaymessage = "None"
    

async def status_task():
    while True:
        now = datetime.datetime.now()
        await asyncio.sleep(10)
        if now.hour == 15 and now.minute == 30:
         global QOTD 
         if QOTD != "None":  
          server = discord.utils.get(client.guilds, name='Elemental Soul')
          role = discord.utils.get(server.roles, name="QOTDping")
          channel = discord.utils.get(server.channels, name="qotd")
          channel2 = discord.utils.get(server.channels, name="self-assign-roles")
          await channel.send(str(role.mention)+" "+QOTD+" Don't like pings? Go to "+str(channel2.mention))
          QOTD = "None"
        

@client.event
async def on_ready():
    activity = discord.Game(name="Elemental Soul | /help")
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
     "I'm not trash talking, I'm talking to trash",
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
     "Nooooob"
    ]
    await ctx.send(random.choice(choices))
   else:
    channel = discord.utils.get(ctx.message.guild.channels, name="roasts")
    await ctx.send("I only do roasts in "+str(channel.mention))

    
@client.command()
async def version(ctx):
    await ctx.send("Elemental Soul Bot v.08 by >Fire.Exe")


@client.command()
async def add(ctx, left : int, right : int):
    await ctx.send(left + right)


@client.command()
async def divide(ctx, left : int, right : int):
    await ctx.send(left / right)
    


@client.command()
async def multiply(ctx, left : int, right : int):
    await ctx.send(left * right)


@client.command()
async def subtract(ctx, left: int, right: int):
        await ctx.send(left - right)


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
        if left  == "Nopartnerpings":
          await ctx.send("You will no longer receive partner pings " + str( user.name))
          await user.add_roles(role)
        elif left  == "QOTDping":
          await ctx.send("You will now receive QOTD pings " + str( user.name))
          await user.add_roles(role)
        elif left  == "Sneakpeakping":
          await ctx.send("You will now receive sneak peak pings " + str( user.name))
          await user.add_roles(role)
            
     
@client.command(pass_content=True)
async def unassign(ctx, left: str):
       user = ctx.message.author
       server = ctx.message.guild
       role = discord.utils.get(server.roles, name=left)
       if ctx.message.channel.name != "general" and ctx.message.channel.name != "qotd-answers" and ctx.message.channel.name != "roasts" and ctx.message.channel.name != "memes":
        if left  == "Nopartnerpings":
          await ctx.send("You will now recieve partner pings " + str( user.name))
          await user.remove_roles(role)
        elif left  == "QOTDping":
          await ctx.send("You will no longer receive QOTD pings " + str( user.name))
          await user.remove_roles(role)
        elif left  == "Sneakpeakping":
          await ctx.send("You will no longer sneak peak pings " + str( user.name))
          await user.remove_roles(role)
    
@client.command(name="kick",
                description="'Kick a member'    'Usage:/kick[member]'     'Example:/kick dJnokia'",
                brief="'Usage:/kick[member]'",
                pass_content=True)
async def kick(ctx, user: discord.Member):
        if ctx.message.author.guild_permissions.kick_members:
         await ctx.send(str(user.name)+" has been kicked")
         await user.kick()
            
@client.command(pass_content=True)      
async def qotd(ctx, *, qotd):
        if ctx.message.author.guild_permissions.ban_members:
         user = ctx.message.author
         await ctx.send(str(user.name)+" has set the qotd to "+qotd)
         global QOTD 
         QOTD = qotd
        
@client.command(pass_content=True)
async def ban(ctx, user: discord.Member):
        if ctx.message.author.guild_permissions.ban_members:
         await ctx.send(str(user.name)+" has been banned")
         await user.ban()
            
            
@client.command(pass_content=True)   
async def mute(ctx, user: discord.Member):
        if ctx.message.author.guild_permissions.kick_members:
         server = ctx.message.guild
         role = discord.utils.get(server.roles, name="Muted")
         await ctx.send(str(user.name)+" has been muted")
         await user.add_roles(role)
        
        
@client.command(pass_content=True)   
async def unmute(ctx, user: discord.Member):
        if ctx.message.author.guild_permissions.kick_members:
         server = ctx.message.guild
         role = discord.utils.get(server.roles, name="Muted")
         await ctx.send(str(user.name)+" has been unmuted")
         await user.remove_roles(role)
            
            
@client.command(pass_content=True)   
async def roleall(ctx, left: str):
        if ctx.message.author.guild_permissions.ban_members:
         server = ctx.message.guild
         role = discord.utils.get(server.roles, name=left)
         await ctx.send("I'm gonna start giving everyone the "+left+" role and i'll notify you when i'm done :gear:")
         x = server.members
         for member in x:
            await member.add_roles(role)
         await ctx.send(""+str(ctx.message.author.mention)+" I've roled everyone :+1:")
        
        
@client.command(pass_content=True)
async def help(ctx):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
  
 embed.set_author(name="Help")
 embed.add_field(name="/help", value="Shows this message",inline=False)
 embed.add_field(name="/roasts", value="Get roasted",inline=False)
 embed.add_field(name="/version", value="Checks my version",inline=False)
 embed.add_field(name="/assign", value="Give yourself a role",inline=True)
 embed.add_field(name="Example:", value="/assign QOTDping",inline=True)
 embed.add_field(name="/unassign", value="Remove a role from yourself",inline=False)
 embed.add_field(name="Example:", value="/unassign QOTDping",inline=True)
 embed.add_field(name="/membercount", value="Shows the amount of people in the server",inline=False)
 embed.add_field(name="/kick", value="Kick a user",inline=True)
 embed.add_field(name="Example:", value="/kick YourDad",inline=True)
 embed.add_field(name="/ban", value="Ban a user",inline=False)
 embed.add_field(name="Example:", value="/ban YourDad",inline=True)
 await ctx.send("Here's all the commands and their uses:", embed=embed)
        
    
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
async def group(ctx, amount : int = None):
 embed = discord.Embed(
        colour = discord.Colour.orange()
 )
 embed.set_author(name=" ")
 embed.add_field(name="Group", value="https://www.roblox.com/My/Groups.aspx?gid=4622364",inline=False)
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
    now = datetime.datetime.now()
    channel = discord.utils.get(member.guild.channels, name="welcome")
    role = discord.utils.get(member.guild.roles, name="QOTDping")
    channel2 = discord.utils.get(member.guild.channels, name="faqs")
    channel3 = discord.utils.get(member.guild.channels, name="es-bot-manual")
    channel4 = discord.utils.get(member.guild.channels, name="log")
    await channel.send("Welcome to Elemental Soul "+str(member.mention)+" Make sure to read "+str(channel2.mention)+" if you have any questions and https://www.roblox.com/groups/4622364/Elemental-Extremes#!/about for the group, also make sure to read "+str(channel3.mention)+" to learn my commands")
    await channel4.send(":inbox_tray:**"+str(member)+"**"+" (ID:"+str(member.id)+") has joined server at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" GMT on the "+str(now.day)+"/"+str(now.month)+"/"+str(now.year))
    await member.add_roles(role)
    
   
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


client.run(TOKEN)



    
