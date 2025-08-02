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
        f"P-U! {member.mention}, you stink! 💨"
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