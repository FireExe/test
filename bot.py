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
    choices = [
     "You have some egg head shape",
     "You should eat some of that make up, to be pretty on the inside",
     "You need to fix that head shape of yours",
     "Your unseasoned",
     "You have the Rthro head shape",
     "Your lips are drier then the sahara",
     "Your knees are ashier then the skin of kfc chicken",
     "What is "+ctx.message.author.name+", that name is so unoriginal",
     "When i saw your head ,I realised a new 3d polygon had been discovered",
     "When someone tried to replicate your head in blender an error came up: triangle limit exceded ",
     "Dead trim, nuff said",
     "I would insult you but nature did a better job.",
     "Two wrongs don't make a right, take your parents as an example",
     "I'm not trash talking, I'm talking to trash",
     "It's a waste of time trying to cuss something so irrelevant",
     "I'm jealous of people that don't know you",
     "A million years of evolution and we get you",
     "I'd tell you to go outside, but you'd just ruin that for everyone else too",
     "To which foundation do I need to donate to help you?",
     "i thought i was ugly but evolution really took a step back with you",
     "It must have been a sad day when you crawled from the abortion bucket",
     "Maybe you should try something more on your level, like rock-paper-scissors",
     "WOW! imagine if your parents weren't siblings",
     "Nooooob"
    ]
    await ctx.send(random.choice(choices))

    
@client.command()
async def version(ctx):
    await ctx.send("Elemental Soul Bot v.05 by >Fire.Exe")


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
        if left  == "Nopartnerpings":
          await ctx.send("You will no longer receive partner pings " + str( user.name))
          await user.add_roles(role)
        elif left  == "QOTDping":
          await ctx.send("You will now receive QOTD pings " + str( user.name))
          await user.add_roles(role)
            
     
@client.command(pass_content=True)
async def unassign(ctx, left: str):
        user = ctx.message.author
        server = ctx.message.guild
        role = discord.utils.get(server.roles, name=left)
        if left  == "Nopartnerpings":
          await ctx.send("You will now recieve partner pings " + str( user.name))
          await user.remove_roles(role)
        elif left  == "QOTDping":
          await ctx.send("You will no longer receive QOTD pings " + str( user.name))
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
         role = discord.utils.get(server.roles, name="Muted")
         await ctx.send(str(user.name)+" has been muted")
         await user.add_roles(role)
        
@client.command(pass_content=True)   
async def mute(ctx, user: discord.Member):
        if ctx.message.author.guild_permissions.kick_members:
         role = discord.utils.get(server.roles, name="Muted")
         await ctx.send(str(user.name)+" has been unmuted")
         await user.remove_roles(role)
        
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
    
        
@client.event
async def on_member_join(member):
    now = datetime.datetime.now()
    channel = discord.utils.get(member.guild.channels, name="welcome")
    role = discord.utils.get(member.guild.roles, name="QOTDping")
    channel2 = discord.utils.get(member.guild.channels, name="faqs")
    channel3 = discord.utils.get(member.guild.channels, name="group")
    channel4 = discord.utils.get(member.guild.channels, name="log")
    await channel.send("Welcome to Elemental Soul "+str(member.mention)+" Make sure to read "+str(channel2.mention)+" if you have any questions and "+str(channel3.mention)+" for the group")
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



    
