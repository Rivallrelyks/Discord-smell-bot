import discord
from discord.ext import commands
import random
import asyncio
import os
from datetime import datetime, timedelta

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Store user smell counts, cooldowns, and recent messages
smell_counts = {}
smell_cooldowns = {}
recent_messages = {}  # Track recent messages per user to avoid repeats

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready to make people smell! 🤢')

@bot.command(name='smell')
async def tell_smell(ctx, member: discord.Member = None):
    """Tell someone they smell"""
    
    # Check cooldown (30 seconds per user)
    user_id = ctx.author.id
    if user_id in smell_cooldowns:
        time_left = smell_cooldowns[user_id] - datetime.now()
        if time_left > timedelta(0):
            await ctx.send(f"Whoa there! You can't smell people for another {time_left.seconds} seconds! Give your nose a break! 👃⏰")
            return
    
    # Set cooldown
    smell_cooldowns[user_id] = datetime.now() + timedelta(seconds=30)
    
    # If no member is mentioned, target the command user
    if member is None:
        member = ctx.author
    
    # Track smell counts
    if member.id not in smell_counts:
        smell_counts[member.id] = 0
    smell_counts[member.id] += 1
    
    # Different messages based on smell count
    if smell_counts[member.id] >= 10:
        special_messages = [
            f"🏆 LEGENDARY STINKER ALERT! 🏆 {member.mention} has been smelled {smell_counts[member.id]} times! They're officially the server's stinkiest legend!",
            f"🎖️ {member.mention} has achieved MAXIMUM STINK LEVEL ({smell_counts[member.id]} smells)! Scientists want to study them!",
            f"👑 BOW DOWN TO THE STINK KING/QUEEN! 👑 {member.mention} has been smelled {smell_counts[member.id]} times!"
        ]
        message = random.choice(special_messages)
    elif smell_counts[member.id] >= 5:
        message = f"🚨 REPEAT OFFENDER! 🚨 {member.mention} has been caught smelling {smell_counts[member.id]} times! (They're getting used to it...)"
    else:
        # Regular smell messages
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
        
        # Smart message selection to avoid repeats
        user_key = f"{ctx.author.id}_{member.id}"  # Track per smeller-target pair
        
        # Get messages this user hasn't seen recently for this target
        if user_key not in recent_messages:
            recent_messages[user_key] = []
        
        # Filter out recently used messages
        available_messages = [msg for msg in smell_messages if msg not in recent_messages[user_key]]
        
        # If we've used all messages, reset the history but keep the last 15 to avoid repeats
        if not available_messages:
            recent_messages[user_key] = recent_messages[user_key][-15:]  # Keep last 15 to avoid immediate repeats
            available_messages = [msg for msg in smell_messages if msg not in recent_messages[user_key]]
        
        # Select message and add to recent history
        message = random.choice(available_messages)
        recent_messages[user_key].append(message)
        
        # Keep only the last 20 messages in history to prevent memory bloat
        if len(recent_messages[user_key]) > 20:
            recent_messages[user_key] = recent_messages[user_key][-20:]
    
    await ctx.send(message)

@bot.command(name='group_smell')
async def group_smell(ctx):
    """Tell everyone in the server they smell"""
    group_messages = [
        "Everyone in this server smells! Time for a group shower! 🚿💨",
        "ATTENTION: This entire server has been declared a biohazard zone! ☣️🏠",
        "Breaking news: Scientists have detected a massive stink cloud over this Discord server! 🌫️🔬",
        "Emergency evacuation: Everyone here smells so bad, the bot needs hazmat protection! 🤖⚠️",
        "Group therapy session needed: Y'all collectively smell like a dumpster fire! 🗑️🔥"
    ]
    await ctx.send(random.choice(group_messages))

@bot.command(name='stinkleaderboard', aliases=['smellboard', 'stinklist'])
async def stink_leaderboard(ctx):
    """Show the top 10 smelliest people"""
    if not smell_counts:
        await ctx.send("Nobody has been smelled yet! Everyone's surprisingly fresh! ✨")
        return
    
    # Sort users by smell count
    sorted_smells = sorted(smell_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    embed = discord.Embed(
        title="🏆 OFFICIAL STINK LEADERBOARD 🏆",
        description="The server's most aromatic individuals:",
        color=0x8B4513  # Brown color for stink theme
    )
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    leaderboard_text = ""
    for i, (user_id, count) in enumerate(sorted_smells):
        try:
            user = bot.get_user(user_id) or await bot.fetch_user(user_id)
            username = user.display_name if user else "Unknown User"
            medal = medals[i] if i < len(medals) else "📍"
            leaderboard_text += f"{medal} **{username}** - {count} smell{'s' if count != 1 else ''}\n"
        except:
            continue
    
    embed.add_field(name="Rankings", value=leaderboard_text or "No data available", inline=False)
    embed.set_footer(text="Remember: Being on this list is... questionable! 👃")
    
    await ctx.send(embed=embed)

@bot.command(name='mystinks', aliases=['mysmells', 'smellme'])
async def my_stinks(ctx):
    """Check how many times you've been smelled"""
    user_id = ctx.author.id
    count = smell_counts.get(user_id, 0)
    
    if count == 0:
        responses = [
            "Wow! You're surprisingly fresh! 🌸✨",
            "Clean as a whistle! Nobody's smelled you yet! 🎵✨",
            "Congratulations! You have achieved peak freshness! 🏆🌺"
        ]
    elif count == 1:
        responses = [f"You've been smelled once! Still pretty fresh! 🌿"]
    elif count < 5:
        responses = [f"You've been smelled {count} times. Getting a bit ripe! 🧄"]
    elif count < 10:
        responses = [f"Oof! {count} smells recorded. You might want to shower... 🚿💨"]
    else:
        responses = [f"LEGENDARY STINKER! {count} smells and counting! You're basically a walking biohazard! ☣️👑"]
    
    await ctx.send(random.choice(responses))

@bot.command(name='randomsmell')
async def random_smell(ctx):
    """Smell a random person in the server"""
    # Get all members who aren't bots
    members = [m for m in ctx.guild.members if not m.bot]
    if not members:
        await ctx.send("No humans to smell! Just bots here... and bots don't smell! (I think...) 🤖")
        return
    
    victim = random.choice(members)
    
    # Update their smell count
    if victim.id not in smell_counts:
        smell_counts[victim.id] = 0
    smell_counts[victim.id] += 1
    
    surprise_messages = [
        f"🎲 RANDOM SMELL ATTACK! 🎲 {victim.mention} has been randomly selected to smell terrible! Lucky you! 🍀💨",
        f"🎯 SURPRISE! {victim.mention} was chosen by the smell gods to be today's stinky victim! 🎪",
        f"🎰 JACKPOT! {victim.mention} wins the lottery... the SMELL lottery! 🎊💨"
    ]
    
    await ctx.send(random.choice(surprise_messages))

@bot.command(name='shower')
async def take_shower(ctx):
    """Take a shower to reduce your smell count"""
    user_id = ctx.author.id
    
    if user_id not in smell_counts or smell_counts[user_id] == 0:
        await ctx.send("You're already squeaky clean! No shower needed! 🛁✨")
        return
    
    # Reduce smell count by 1-3 (random shower effectiveness)
    reduction = random.randint(1, min(3, smell_counts[user_id]))
    smell_counts[user_id] -= reduction
    
    shower_messages = [
        f"🚿 *SHOWER TIME!* 🚿 {ctx.author.mention} scrubbed off {reduction} smell{'s' if reduction != 1 else ''}! Much better! ✨",
        f"🛁 Splish splash! {ctx.author.mention} took a bath and removed {reduction} stink point{'s' if reduction != 1 else ''}! 🧼",
        f"🚿 {ctx.author.mention} used soap! It's super effective! -{reduction} smell{'s' if reduction != 1 else ''}! 🧽✨"
    ]
    
    await ctx.send(random.choice(shower_messages))

@bot.command(name='smellhelp')
async def smell_help(ctx):
    """Show all smell-related commands"""
    embed = discord.Embed(
        title="🤢 SMELL BOT COMMANDS 🤢",
        description="All the ways to make people stink!",
        color=0x00ff00
    )
    
    commands_list = """
    `!smell` - You smell!
    `!smell @user` - Tell someone they smell
    `!group_smell` - Everyone smells!
    `!randomsmell` - Smell a random person
    `!stinkleaderboard` - Top 10 smelliest people
    `!mystinks` - Check your smell count
    `!shower` - Take a shower to smell better
    `!smellhelp` - Show this menu
    """
    
    embed.add_field(name="Commands", value=commands_list, inline=False)
    embed.set_footer(text="Remember: It's all in good fun! 😄")
    
    await ctx.send(embed=embed)

# Error handling
@tell_smell.error
async def smell_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("I couldn't find that person! But you probably smell too! 😏")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Slow down there, smell detective! Try again in {error.retry_after:.1f} seconds! 👃⏰")

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
