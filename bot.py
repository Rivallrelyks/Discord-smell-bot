import discord
from discord.ext import commands
import random
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='smell')
async def tell_smell(ctx, member: discord.Member = None):
    """Tell someone they smell"""
    
    if member is None:
        member = ctx.author
    
    smell_messages = [
   f"{member.mention}, you smell! 🤢",
        f"Oof, {member.mention} needs a shower! 🚿",
        f"{member.mention}, what's that smell? Oh wait, it's you! 😷",
        f"Someone get {member.mention} some deodorant! 🧴",
        f"{member.mention} smells like old cheese! 🧀",
        f"P-U! {member.mention}, you stink! 💨",
        f"{member.mention} smells like a gym sock that's been left in a locker for 3 months! 🧦",
        f"Whoa {member.mention}, did you wrestle a skunk? 🦨",
        f"{member.mention} smells like expired milk mixed with sadness! 🥛😭",
        f"Alert! {member.mention} has activated biological warfare! ☣️",
        f"{member.mention} smells like a tuna sandwich left in the sun! 🐟☀️",
        f"Breaking news: {member.mention} has been classified as a hazmat situation! ⚠️",
        f"{member.mention} smells like a wet dog rolled in garbage! 🐕🗑️",
        f"Scientists are studying {member.mention}'s smell to create new weapons! 🧪⚗️",
        f"{member.mention} could clear a room faster than a fire alarm! 🚨",
        f"Roses are red, violets are blue, {member.mention} smells like a dirty shoe! 👟",
        f"{member.mention} smells like they bathed in pickle juice and regret! 🥒😞",
        f"Warning: {member.mention} may cause spontaneous nose blindness! 👃❌",
        f"{member.mention} smells like a zombie's armpit! 🧟‍♂️💪",
        f"Fun fact: {member.mention}'s smell is visible from space! 🛰️👀",
        f"{member.mention} smells like old broccoli having an existential crisis! 🥦😱",
        f"Plot twist: {member.mention} IS the mysterious gas leak! 💨🔍",
        f"{member.mention} smells like a dragon's morning breath! 🐲😤",
        f"Attention: {member.mention} has weaponized their body odor! 🎯💣",
        f"{member.mention} smells like defeat and cheese puffs! 🧀😔",
        f"Local news: {member.mention} single-handedly destroyed the ozone layer! 🌍💥",
        f"{member.mention} smells like they're marinated in confusion and bad choices! 🤔💭",
        f"Emergency broadcast: {member.mention} has created a new form of pollution! 📢🏭",
        f"{member.mention} smells like a failed science experiment! ⚗️💥",
        f"Breaking: {member.mention}'s smell just got its own zip code! 📮🏠",
        f"{member.mention} smells like they've been seasoned by sadness! 🧂😢",
        f"Archaeologists found {member.mention}'s smell in ancient ruins! 🏛️📜",
        f"{member.mention} smells like liquid regret and broken dreams! 💧😴",
        f"Weather update: There's a 100% chance of stink around {member.mention}! ⛈️📊",
        f"{member.mention} smells like they lost a fight with a garbage disposal! 🗑️🥊",
        f"Medical mystery: How is {member.mention} still conscious with that smell? 🏥❓",
        f"{member.mention} smells like they've been marinating in their own despair! 🍖😰",
        f"Congratulations {member.mention}! You've achieved legendary stench status! 🏆👑",
        f"{member.mention} smells like a mix of old socks and shattered hopes! 🧦💔",
        f"Plot armor can't protect you from {member.mention}'s smell! 🛡️❌",
        f"{member.mention} smells like they've been blessed by the Stink Fairy! 🧚‍♀️💨",
        f"Fun fact: {member.mention}'s deodorant filed a restraining order! 🧴⚖️",
        f"{member.mention} smells like they've been cursed by an ancient gym! 🏛️💪",
        f"Breaking: NASA wants to study {member.mention}'s smell as alternative rocket fuel! 🚀⛽",
        f"{member.mention} smells like they've been fermenting in their own juices! 🍷🤢",
        f"Mythbusters confirmed: {member.mention}'s smell can melt steel beams! 🏗️🔥"
    ]
    
    message = random.choice(smell_messages)
    await ctx.send(message)

@bot.command(name='group_smell')
async def group_smell(ctx):
    """Tell everyone in the server they smell"""
    await ctx.send("Everyone in this server smells! Time for a group shower! 🚿💨")

@tell_smell.error
async def smell_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("I couldn't find that person! But you probably smell too! 😏")

# Use environment variable for token (Railway will provide this)

bot.run(os.getenv('DISCORD_TOKEN'))
