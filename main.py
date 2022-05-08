import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord.ext.commands import Bot
import datetime
import requests, json

def generate(msg, tokens=50):
    return null # broken

GUILD_ID = 937743943326638190 
ANNOUNCE_CHANNEL = 937749948668211270
WELCOME_CHANNEL = 937749120129581086
ver = "1.0"
intents = nextcord.Intents.default()
intents.members = True
bot = Bot(command_prefix='$', intents=intents)

@bot.slash_command(guild_ids=[GUILD_ID], description="Ban a member from the server.")
async def ban(interaction: Interaction, arg: nextcord.Member=None):
    if interaction.user.get_role(937745800317010041):
        if arg is None:
            await interaction.response.send_message("You need to mention a user to ban.")
            return
        try:
            arg.send("You have been banned from the server.")
            await interaction.guild.ban(arg, reason="Banned by rosebot")
            embed = nextcord.Embed(title="Banned", description=f"{arg.mention} has been banned from the server.\n```Rosebot punishment system {ver}```", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
        except Exception as e:
            embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
            embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
            await interaction.response.send_message(embed=embed)
            return
    else:
        await interaction.response.send_message("You are not a moderator. Shush.")


@bot.slash_command(guild_ids=[GUILD_ID], description="Super secret bot owner command.")
async def echo(interaction: Interaction, arg: str):
    if interaction.user.id == 883031597291569193:
        await interaction.response.send_message(arg)
    else:
        embed = nextcord.Embed(title="Error", description="You are not the owner of this bot.", color=nextcord.Color.blurple())
        await interaction.response.send_message(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="[Admins] Change the state of a suggestion.")
async def conclude(interaction: Interaction, accept: bool, msgid: str, notes: str):
    arg = int(msgid)
    if interaction.user.get_role(937745800317010041):
        if arg is None:
            await interaction.response.send_message("You need to specify a suggestion ID.")
            return
        try:
            message = await interaction.guild.get_channel(937752150354829362).fetch_message(arg)
            suggestion_content = message.embeds[0].fields[0].value
            if message is None:
                await interaction.response.send_message("That suggestion ID does not exist.")
                return
            if accept:
                await message.edit(embed=nextcord.Embed(title="Suggestion Accepted", description=f"{suggestion_content}\n```"+notes+"```", color=nextcord.Color.green()))
                await interaction.response.send_message("Suggestion accepted.")
                return
            else:
                await message.edit(embed=nextcord.Embed(title="Suggestion Rejected", description=f"{suggestion_content}\n```"+notes+"'```", color=nextcord.Color.red()))
                await interaction.response.send_message("Suggestion rejected, don't you love crushing people's dreams :)")
                return
        except Exception as e:
            embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
            embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
            await interaction.response.send_message(embed=embed)
            return

@bot.slash_command(guild_ids=[GUILD_ID], description="Warn a member in the server.")
async def warn(interaction: Interaction, arg: nextcord.Member, reason=str):
    if interaction.user.get_role(937745800317010041):
        if arg is None:
            await interaction.response.send_message("You need to mention a user to warn.")
            return
        try:
            embed = nextcord.Embed(title="Warned", description=f"{arg.mention} has been warned for {reason}\n```Rosebot punishment system {ver}```", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            embed2dm = nextcord.Embed(title="You have been warned", description=f"You have been warned for {reason}\n```Rosebot punishment system {ver}```", color=nextcord.Color.blurple())
            await arg.send_message(embed=embed2dm)
            return
        except Exception as e:
            embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
            embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
            await interaction.response.send_message(embed=embed)
            return

@bot.slash_command(guild_ids=[GUILD_ID], description="Add a role to everyone in the server")
async def addrole(interaction: Interaction, arg: nextcord.Role):
    if interaction.user.id == 883031597291569193:
        users = []
        if arg is None:
            await interaction.response.send_message("You need to mention a role to add.")
            return
        try:
            for member in interaction.guild.members:
                await interaction.channel.send(f"**{member.name}** has been given the role **{arg.name}**.")
                await member.add_roles(arg)
                users.append(member.name)
            fstring = " ".join(users)
            await interaction.response.send_message("Role added to everyone.")
            return
        except Exception as e:
            embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
            embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
            await interaction.response.send_message(embed=embed)
            return
    else:
        await interaction.response.send_message("You are not fizzdev, this is a super special command anyways.")

@bot.slash_command(guild_ids=[GUILD_ID], description="Purge messages in a channel.")
async def purge(interaction: Interaction, arg: int=None):
    if interaction.user.get_role(937745800317010041):
        if arg is None:
            await interaction.response.send_message("You need to specify a number of messages to purge.")
            return
        try:
            await interaction.channel.purge(limit=arg)
            embed = nextcord.Embed(title="Purged", description=f"{arg} messages have been purged.", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
        except Exception as e:
            embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
            embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
            await interaction.response.send_message(embed=embed)
            return
    else:
        await interaction.response.send_message("You are not a moderator. Shush.")

@bot.event
async def on_member_join(member: nextcord.Member):
    try:
        embed = nextcord.Embed(title="Welcome to the server!", description=f"{member.mention} has joined the discord server! We hope you have a fun time here :D", color=nextcord.Color.blurple())
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"{member.guild.name} | {member.guild.member_count} members")
        await member.guild.get_channel(WELCOME_CHANNEL).send(embed=embed)
    except Exception as e:
        embed = nextcord.Embed(title="Welcome to the server!", description=f"{member.mention} has joined the discord server! We hope you have a fun time here :D", color=nextcord.Color.blurple())
        embed.set_footer(text=f"{member.guild.name} | {member.guild.member_count} members")
        await member.guild.get_channel(WELCOME_CHANNEL).send(embed=embed)
    role = member.guild.get_role(938134834751078480)
    c2 = member.guild.get_role()
    if not member.bot:
        global invites_dict
        guild = member.guild
        guild_invites = await guild.invites()
        invitecode = guild_invites[0].code
        await c2.send(f"{member.mention} joined using the invite {invitecode}")
    await member.add_roles(role)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message: nextcord.Message):
    if message.author.bot:
        return
    if message.content.startswith("<@!934838543208042586>"):
        await message.channel.send("Hey, I'm a bot, not a human. If you want to talk to me, please use `/` commands.")
        return
    if message.channel.id == 937752150354829362:
        embed = nextcord.Embed(title="Suggestion", description=f"{message.author.mention} has suggested:", color=nextcord.Color.blurple())
        embed.add_field(name="Suggestion", value=message.content)
        embed.set_footer(text=f"Suggested by {message.author.name}", icon_url=message.author.avatar)
        x = await message.guild.get_channel(937752150354829362).send(embed=embed)
        await x.add_reaction("✅")
        await x.add_reaction("❌")
        await message.delete()
        return
    if "@fizz" in message.content:
        embed = nextcord.Embed(title="Warned", description=f"{message.author.mention} has been warned (and timed out) for Mentioning an admin. I understand that you may be asking a question, but that's why we have the <#939939466460667964> channel.\n```Rosebot punishment system {ver}```", color=nextcord.Color.blurple())
        await message.channel.send(embed=embed)
        return

@bot.event
async def on_message_delete(message: nextcord.Message):
    if message.author.bot:
        return
    if message.channel.id == 937752150354829362:
        return
    d_ch = message.guild.get_channel(938137638609772564)
    embed = nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} got a message deleted in {message.channel.mention}", color=nextcord.Color.blurple())
    embed.add_field(name="Message", value=message.content)
    embed.set_footer(text=f"Message was by {message.author.name}", icon_url=message.author.avatar)
    await d_ch.send(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="This is how you connect to the Minecraft server.")
async def ip(interaction: Interaction):
    embed = nextcord.Embed(title="How to connect to the server", description="These instructions will walk you through the process of connecting to the RoseSMP!", color=nextcord.Color.blurple())
    embed.add_field(name="Java Edition", value="Open Minecraft, go to Multiplayer, click `Add Server` and the name can be anything you want. The Server Address is `play.luminamc.com`!")
    embed.add_field(name="Bedrock Edition", value="Open Minecraft, Click play, go to Servers, scroll down to the bottom and click `Add Server` and the name can be anything you want. The Server Address is `play.luminamc.com`, and the Port is `19132`")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Access the server map using this link.")
async def map(interaction: Interaction):
    embed = nextcord.Embed(title="Server Map", description="Click the link below to access the server map!", color=nextcord.Color.blurple())
    embed.add_field(name="Server Map", value="http://luminamc.com/")
    await interaction.response.send_message(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Use GPT-2 AI to finish a sentence.")
async def gpt2(interaction: Interaction, prompt: str):
    b = await interaction.response.send_message("Making request to rosebot AI.")
    x = generate(prompt, "500")["body"]["result"].replace("\n", " ")
    await interaction.channel.send(interaction.user.mention + " **generated** " + x)

@bot.slash_command(guild_ids=[GUILD_ID], description="Add a colour role to yourself.")
async def colour(interaction: Interaction, colour: int = SlashOption(name="picker", description="The colour that you want", choices={"Yellow": 1, "Green": 2, "Blue": 3, "Purple": 4}, ), ):
    change = False
    if colour is None:
        embed = nextcord.Embed(title="Error", description="You need to choose a number!", color=nextcord.Color.blurple())
        await interaction.response.send_message(embed=embed)
        return
    for role in interaction.user.roles:
        for r in [938118763939786784, 938118656737562674, 938118701637591150, 938118724978901032]:
            if role.id == r:
                await interaction.user.remove_roles(role)
                change = True
    if colour == 1:
        role = 938118763939786784
        c = nextcord.Color.gold()
    elif colour == 2:
        role = 938118656737562674
        c = nextcord.Color.green()
    elif colour == 3:
        role = 938118701637591150
        c = nextcord.Color.blue()
    elif colour == 4:
        role = 938118724978901032
        c = nextcord.Color.purple()
    try:
        await interaction.user.add_roles(interaction.guild.get_role(role))
        if change:
            embed = nextcord.Embed(title="Success", description="You have changed colour role!", color=c)
        else:
            embed = nextcord.Embed(title="Success", description="You have been given a colour role!", color=c)
        await interaction.response.send_message(embed=embed)
        return
    except Exception as e:
        embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
        embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
        await interaction.response.send_message(embed=embed)
        return

@bot.slash_command(guild_ids=[GUILD_ID], description="Get a list of all the colour roles.")
async def colours(interaction: Interaction):
    embed = nextcord.Embed(title="Colour roles", description="These are the colour roles that you can get.", color=nextcord.Color.blurple())
    embed.add_field(name="**Colours**", value="Yellow\nGreen\nBlue\nPurple\nGet a role with `/colour`", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Choose if you want to recieve pings for announcements.")
async def pings(interaction: Interaction, arg: str = SlashOption(name="on", description="Turn pings on", choices={"on": "on", "off": "off"}, ), ):
    pingrole = interaction.guild.get_role(938134834751078480)
    if arg is None:
        embed = nextcord.Embed(title="Error", description="You need to choose `on` or `off`.", color=nextcord.Color.blurple())
        await interaction.response.send_message(embed=embed)
        return
    if arg == "on":
        if pingrole in interaction.user.roles:
            embed = nextcord.Embed(title="Hey!", description="You already have pings on, kinda cool innit.", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
        else:
            await interaction.user.add_roles(pingrole)
            embed = nextcord.Embed(title="Success", description="You now have pings on!", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
    elif arg == "off":
        if pingrole in interaction.user.roles:
            await interaction.user.remove_roles(pingrole)
            embed = nextcord.Embed(title="Success", description="You now have pings off!", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
        else:
            embed = nextcord.Embed(title="Hey!", description="You already have pings off, maybe you should turn them on :)", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
    else:
        embed = nextcord.Embed(title="Error", description="How did you get here?", color=nextcord.Color.blurple())
        await interaction.response.send_message(embed=embed)
        return

@bot.slash_command(guild_ids=[GUILD_ID], description="Remove all your colour roles.")
async def rmcolour(interaction: Interaction):
    change = False
    for role in interaction.user.roles:
        for r in [938118763939786784, 938118656737562674, 938118701637591150, 938118724978901032]:
            if role.id == r:
                await interaction.user.remove_roles(role)
                change = True
    if change:
        embed = nextcord.Embed(title="Success", description="You have removed all your colour roles!", color=nextcord.Color.green())
        await interaction.response.send_message(embed=embed)
        return
    else:
        embed = nextcord.Embed(title="Error", description="You don't have any colour roles!", color=nextcord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

@bot.slash_command(guild_ids=[GUILD_ID], description="This command can let moderators and administrators create an announcement.")
async def announce(interaction: Interaction, ping: bool , arg: str):
    c = bot.get_channel(ANNOUNCE_CHANNEL)
    if interaction.user.get_role(937745800317010041):
        e = nextcord.Embed(title="Announcement", description=arg, color=nextcord.Color.blurple(), timestamp=datetime.datetime.utcnow())
        e.set_footer(text=f"Announced by {interaction.user.name}", icon_url=interaction.user.avatar)
        if ping:
            await c.send(content="<@&938134834751078480> ping :moyai:", embed=e)
        else:
            await c.send(embed=e)
        await interaction.response.send_message("Announcement sent!")
    else:
        embed = nextcord.Embed(title="Error", description=f"You do not have permission to execute this command.", color=nextcord.Color.blurple())
        await interaction.response.send_message(embed=embed)

@bot.slash_command(guild_ids=[GUILD_ID], description="Kick a member from the server.")
async def kick(interaction: Interaction, arg: nextcord.Member=None):
    if interaction.user.get_role(937745800317010041):
        if arg is None:
            await interaction.response.send_message("You need to mention a user to kick.")
            return
        try:
            await interaction.guild.kick(arg, reason="Kicked by rosebot")
            embed = nextcord.Embed(title="Kicked", description=f"{arg.mention} has been kicked from the server.\n```Rosebot punishment system {ver}```", color=nextcord.Color.blurple())
            await interaction.response.send_message(embed=embed)
            return
        except Exception as e:
            embed = nextcord.Embed(title="Error", description=f"{e}", color=nextcord.Color.blurple())
            embed.add_field(name="Please contact an admin", value="This error has been logged and will be used to improve rosebot v2 :)")
            await interaction.response.send_message(embed=embed)
            return
    else:
        await interaction.response.send_message("You are not a moderator. Shush.")

bot.run("token")
