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
            f"Mythbusters confirmed: {member.mention}'s smell can melt steel beams! 🏗️🔥",
            # 100 NEW MESSAGES WITH MOVIE REFERENCES
            f"Frankly my dear, {member.mention}, you stink! (Gone with the Wind) 🎬💨",
            f"I see smelly people... and it's {member.mention}! (The Sixth Sense) 👻👃",
            f"May the stench be with you, {member.mention}! (Star Wars) ⭐💫",
            f"Houston, we have a smell problem... it's {member.mention}! (Apollo 13) 🚀🤢",
            f"I'll be back... with air freshener for {member.mention}! (Terminator) 🤖🌸",
            f"Show me the soap! {member.mention} needs it! (Jerry Maguire) 🧼✨",
            f"Nobody puts {member.mention} in a corner... because they smell! (Dirty Dancing) 💃🤢",
            f"You talking to me about smells? {member.mention} takes the crown! (Taxi Driver) 🚕👑",
            f"Life is like a box of chocolates, {member.mention}... yours went bad! (Forrest Gump) 🍫😷",
            f"I'm gonna make {member.mention} a smell they can't refuse! (The Godfather) 🎭💨",
            f"Here's Johnny... and his terrible smell, {member.mention}! (The Shining) 🪓🤢",
            f"E.T. phone home... {member.mention} smells like outer space! (E.T.) 👽📞",
            f"Roads? Where we're going, {member.mention}, we don't need air fresheners! (Back to the Future) 🚗⏰",
            f"Inconceivable! {member.mention}'s smell defies logic! (The Princess Bride) ⚔️👸",
            f"I feel the need... the need for deodorant around {member.mention}! (Top Gun) ✈️🧴",
            f"After all this time? Always smelly, {member.mention}! (Harry Potter) ⚡🦌",
            f"My precious... is soap for {member.mention}! (Lord of the Rings) 💍🧼",
            f"I am your father... and you smell terrible, {member.mention}! (Star Wars) 🖤⚔️",
            f"Hasta la vista, {member.mention}'s hygiene! (Terminator 2) 🤖👋",
            f"You can't handle the stench of {member.mention}! (A Few Good Men) ⚖️💨",
            f"Elementary, my dear Watson, {member.mention} needs a bath! (Sherlock Holmes) 🔍🛁",
            f"Frankenstein's monster smells better than {member.mention}! (Frankenstein) ⚡🧟",
            f"With great power comes great smell... sorry {member.mention}! (Spider-Man) 🕷️💨",
            f"I see you, {member.mention}... and smell you too! (Avatar) 🌿👁️",
            f"Rosebud... was {member.mention}'s last soap! (Citizen Kane) 🌹🧼",
            f"Here's looking at you, smelly {member.mention}! (Casablanca) 👀💨",
            f"Toto, I don't think we're in Kansas anymore... {member.mention} smells like Oz! (Wizard of Oz) 🌪️🤢",
            f"Bond. James Bond. Licensed to smell... {member.mention}! (007) 🕴️💨",
            f"I'll have what she's having... wait no, {member.mention} smells terrible! (When Harry Met Sally) 🍽️😷",
            f"You had me at hello... then {member.mention} walked in! (Jerry Maguire) 💕🤢",
            f"My mama always said, {member.mention} smells like a box of rotten chocolates! (Forrest Gump) 🍫👵",
            f"There's no place like home... away from {member.mention}'s smell! (Wizard of Oz) 🏠💨",
            f"I'm not a smart man, but I know what stinks... it's {member.mention}! (Forrest Gump) 🪶🤢",
            f"Nobody expects the Spanish Inquisition... or {member.mention}'s smell! (Monty Python) ⚔️💨",
            f"Keep your friends close, but {member.mention}'s smell closer! (The Godfather) 🤝💨",
            f"Say hello to my little friend... air freshener for {member.mention}! (Scarface) 🔫🌸",
            f"I'm gonna take him to the cleaners... literally, {member.mention}! (Various gangster movies) 🧽💰",
            f"Why so serious about hygiene, {member.mention}? (The Dark Knight) 🃏🛁",
            f"You shall not pass... without showering first, {member.mention}! (Lord of the Rings) 🧙‍♂️🚿",
            f"I am Iron Man... and {member.mention} is Stink Man! (Iron Man) 🤖💨",
            f"Avengers... assemble air fresheners for {member.mention}! (Avengers) 🦸‍♂️🌸",
            f"With great stink comes great responsibility, {member.mention}! (Spider-Man) 🕸️💨",
            f"I can do this all day... smelling {member.mention}! Wait, no I can't! (Captain America) 🛡️🤢",
            f"Hulk SMASH... {member.mention}'s B.O.! (Hulk) 💚💥",
            f"That's America's... smelliest citizen, {member.mention}! (Captain America) 🇺🇸💨",
            f"I love you 3000... showers for {member.mention}! (Avengers: Endgame) ❤️🚿",
            f"This is the way... to the shower, {member.mention}! (The Mandalorian) 🛡️🚿",
            f"Do or do not, there is no try... but {member.mention} needs to try soap! (Star Wars) 🟢🧼",
            f"Help me, Obi-Wan... {member.mention} is too smelly! (Star Wars) 👸💨",
            f"Use the Force, {member.mention}... to find a shower! (Star Wars) ⚔️🚿",
            f"It's a trap! {member.mention}'s smell is everywhere! (Star Wars) 🐙💨",
            f"These aren't the droids you're looking for... but {member.mention} is the smell we found! (Star Wars) 🤖👃",
            f"The Force is strong with this one's smell, {member.mention}! (Star Wars) ⚡💨",
            f"Great Scott! {member.mention} smells like they're from 1885! (Back to the Future) ⚡🕰️",
            f"Nobody puts Baby in a corner, but we're putting {member.mention} outside! (Dirty Dancing) 👶🚪",
            f"I'm the king of the world... of bad smells, {member.mention}! (Titanic) 🚢👑",
            f"Draw me like one of your French girls... but don't smell like {member.mention}! (Titanic) 🎨🇫🇷",
            f"My heart will go on... but {member.mention}'s smell won't! (Titanic) ❤️🚢",
            f"Mama says stupid is as stupid does... and {member.mention} smells! (Forrest Gump) 🪶👵",
            f"Run, {member.mention}, run... to the shower! (Forrest Gump) 🏃‍♂️🚿",
            f"Houston, we have a problem... {member.mention} is on the space station! (Apollo 13) 🚀😷",
            f"To infinity and beyond... {member.mention}'s smell reaches galaxies! (Toy Story) 🚀🌌",
            f"You've got a friend in me... but {member.mention} needs soap! (Toy Story) 🤠🧼",
            f"There's a snake in my boot... and {member.mention} in my nose! (Toy Story) 🐍👢",
            f"Hakuna Matata... except for {member.mention}'s smell! (The Lion King) 🦁💨",
            f"Just keep swimming away from {member.mention}'s smell! (Finding Nemo) 🐠🏊‍♀️",
            f"Ohana means family... but {member.mention} smells like garbage! (Lilo & Stitch) 🌺🗑️",
            f"Let it go... {member.mention}'s hygiene already did! (Frozen) ❄️💨",
            f"The cold never bothered me anyway... but {member.mention}'s smell does! (Frozen) ☃️🤢",
            f"Some people are worth melting for... {member.mention} isn't one! (Frozen) ⛄💧",
            f"Adventure is out there... away from {member.mention}! (Up) 🎈🏃‍♂️",
            f"Squirrel! Oh wait, that's just {member.mention}'s smell! (Up) 🐿️💨",
            f"I have a particular set of skills... detecting {member.mention}'s smell! (Taken) 📞🔍",
            f"I'll find you... {member.mention}, and I'll bring soap! (Taken) 🧼🔎",
            f"Are you not entertained by {member.mention}'s smell?! (Gladiator) ⚔️🏛️",
            f"What we do in life echoes in eternity... like {member.mention}'s stench! (Gladiator) ⚡👑",
            f"You either die a hero or live long enough to smell like {member.mention}! (The Dark Knight) 🦇😷",
            f"It's not who I am underneath, but what I smell... it's {member.mention}! (Batman Begins) 🌃💨",
            f"Some men just want to watch the world burn... {member.mention} wants to smell it! (The Dark Knight) 🔥👃",
            f"You think darkness is your ally? {member.mention}, you were born in stink! (The Dark Knight Rises) 🌑💨",
            f"I was born in it, molded by it... {member.mention} and their smell! (The Dark Knight Rises) 💪🤢",
            f"The first rule of Fight Club is... don't smell like {member.mention}! (Fight Club) 👊🧼",
            f"His name was Robert Paulson... {member.mention}'s smell was legendary! (Fight Club) 👤💨",
            f"I am Jack's complete lack of hygiene... wait, that's {member.mention}! (Fight Club) 🎭🚿",
            f"Welcome to the Matrix, {member.mention}... where you still smell! (The Matrix) 🕶️💊",
            f"There is no spoon... but there is {member.mention}'s smell! (The Matrix) 🥄💨",
            f"Neo, you are the One... {member.mention} is the Smelly One! (The Matrix) 🕴️🤢",
            f"Show me the money... for {member.mention}'s soap! (Jerry Maguire) 💰🧼",
            f"You complete me... except {member.mention}, you smell! (Jerry Maguire) 💕💨",
            f"I'm not bad, I'm just drawn that way... unlike {member.mention}'s smell! (Who Framed Roger Rabbit) 💋🎨",
            f"Elementary, my dear {member.mention}... you need deodorant! (Sherlock Holmes) 🔍🧴",
            f"The game is afoot... and it smells like {member.mention}! (Sherlock Holmes) 👣💨",
            f"Clever girl... {member.mention} is clever at avoiding showers! (Jurassic Park) 🦕🚿",
            f"Life finds a way... to make {member.mention} smell terrible! (Jurassic Park) 🧬💨",
            f"They're moving in herds... away from {member.mention}! (Jurassic Park) 🦕🏃‍♂️",
            f"Hold on to your butts... {member.mention} is about to smell worse! (Jurassic Park) 🍑💨",
            f"Nobody expects the Spanish Inquisition... or {member.mention}'s armpit! (Monty Python) ⚔️💪",
            f"It's just a flesh wound... but {member.mention}'s smell is fatal! (Monty Python) ⚔️💀",
            f"Run away! Run away from {member.mention}! (Monty Python) 🏃‍♂️💨",
            f"We are the knights who say Ni... and {member.mention} who says P-U! (Monty Python) ⚔️🌳",
            f"Your mother was a hamster and your father smelt of elderberries, {member.mention}! (Monty Python) 🐹🍇",
            f"I fart in your general direction, {member.mention}... oh wait, that's you! (Monty Python) 💨🏰",
            f"What is your favorite color? Blue! No wait, it's the smell of {member.mention}! (Monty Python) 🌉🎨",
            f"Ni! Ni! {member.mention} needs soap! Ni! (Monty Python) 🌳🧼",
            f"She turned me into a newt! {member.mention} turns me into someone with no sense of smell! (Monty Python) 🦎👃",
            f"'Tis but a scratch... unlike {member.mention}'s permanent stench! (Monty Python) ⚔️💨",
            f"I'm not dead yet! But {member.mention}'s smell might kill me! (Monty Python) ⚰️💀",
            f"Bring out your dead... starting with {member.mention}'s hygiene! (Monty Python) 🔔⚰️",
            f"We want a shrubbery... and a shower for {member.mention}! (Monty Python) 🌿🚿",
            f"It's only a model... unlike {member.mention}'s very real smell! (Monty Python) 🏰💨",
            f"On second thought, let's not go to Camelot... {member.mention} is there! (Monty Python) 🏰🏃‍♂️",
            f"I'm not a witch! But {member.mention} smells like they brew potions! (Monty Python) 🧙‍♀️⚗️",
            f"She's got huge... tracts of smell, that {member.mention}! (Monty Python) 🏰💨",
            f"And now for something completely different... {member.mention} taking a shower! (Monty Python) 📺🚿",
            f"Nobody expects... {member.mention} to smell this bad! (Monty Python) 😱💨",
            # 100 NEW MEME, ANIME & DARK HUMOR RESPONSES
            f"It's over {member.mention}! I have the high ground... and better hygiene! (Star Wars/Prequel Memes) ⚔️🏔️",
            f"{member.mention} used Self-Destruct! It's super effective... on everyone's noses! (Pokemon) 💥👃",
            f"When you realize {member.mention} is sus... because they smell! (Among Us) 🔴🤢",
            f"{member.mention} was ejected. Reason: Too smelly. (Among Us) 🚀💨",
            f"Red flag! {member.mention} is the imposter... of good hygiene! (Among Us) 🚩🧼",
            f"{member.mention} vented... their smell into the whole server! (Among Us) 🕳️💨",
            f"Emergency meeting! {member.mention} is stinking up electrical! (Among Us) 🚨⚡",
            f"I ain't the sharpest tool in the shed, but {member.mention} is the smelliest! (Shrek/All Star) 🧰💨",
            f"Somebody once told me {member.mention} was gonna stink me! (Shrek/All Star) 🎵🤢",
            f"{member.mention} is not like other girls... they smell worse! (VSCO/Not Like Other Girls) ✨💨",
            f"It's giving... unwashed energy, {member.mention}! (Gen Z slang) 💅🤢",
            f"{member.mention} said no cap... but forgot to say no stink! (Gen Z) 🧢💨",
            f"{member.mention} is lowkey highkey stinking up the place! (Gen Z) 📱💨",
            f"POV: {member.mention} enters the chat and everyone's nose dies! (TikTok) 📱💀",
            f"This you? *shows picture of soap* {member.mention} (Twitter meme) 🧼📸",
            f"{member.mention} really said 'hygiene is optional' and meant it! (Twitter) 💬🚿",
            f"Tell me you don't shower without telling me... {member.mention}: (TikTok trend) 🤫🚿",
            f"The duality of man: Good personality vs {member.mention}'s smell! (Philosophy meme) ⚖️💨",
            f"Virgin soap user vs Chad natural musk {member.mention}! (Virgin vs Chad) 👑💨",
            f"Sigma grindset: Ignore hygiene, acquire stench - {member.mention} (Sigma male) 💪💨",
            f"Based and stink-pilled, {member.mention}! (4chan/Political Compass) 🗿💨",
            f"{member.mention} chose violence... against everyone's nostrils! (Twitter meme) ⚔️👃",
            f"Breaking: Local {member.mention} discovers water is wet... still won't use it! (News meme) 📰💧",
            f"{member.mention} really went 'Hold my beer' to hygiene standards! (Hold my beer) 🍺🧼",
            f"Nobody: \nAbsolutely nobody: \n{member.mention}: *exists smellily* (Nobody meme) 👤💨",
            f"Me: Can we get deodorant? \nMom: We have deodorant at home \nDeodorant at home: {member.mention} (Meme) 🏠🧴",
            f"Roses are red, {member.mention} smells like death! (Roses are red meme) 🌹💀",
            f"{member.mention} out here looking like a whole contamination site! (Reaction meme) ☢️🏭",
            f"The good ending: {member.mention} discovers soap! (Good/Bad ending meme) ✨🧼",
            f"The bad ending: {member.mention} runs out of deodorant! (Good/Bad ending meme) 😈💨",
            f"Achievement Unlocked: {member.mention} - 'Biological Warfare' (Gaming achievement) 🏆☣️",
            f"Error 404: {member.mention}'s hygiene not found! (Error meme) 🖥️❌",
            f"It's Wednesday my dudes... and {member.mention} still hasn't showered! (Wednesday frog) 🐸📅",
            f"Friendship ended with fresh air, now mouth breathing is my best friend - {member.mention} nearby (Friendship ended meme) 🤝💨",
            f"{member.mention} really said 'I don't need deodorant' and we all suffered! (Really said) 💬😵",
            f"Therapist: {member.mention}'s smell isn't real, it can't hurt you. \n{member.mention}'s smell: (Therapist meme) 🛋️💀",
            f"Scientists hate this one trick {member.mention} uses to clear rooms! (Clickbait) 🧪💨",
            f"Day 47: {member.mention} still believes Axe body spray counts as a shower! (Day X) 📅🚿",
            f"Plot twist: {member.mention} is actually three skunks in a trenchcoat! (Plot twist) 🦨🧥",
            f"Congratulations! You've unlocked {member.mention}'s final form: Pure Stench! (Final form) 🎊💨",
            f"{member.mention} entered the chat, hygiene left the chat! (Entered/left chat) 💬🚪",
            # ANIME REFERENCES
            f"Omae wa mou... stinky desu, {member.mention}! (Fist of the North Star) 👊💀",
            f"{member.mention} used Thousand Years of Death... on everyone's sense of smell! (Naruto) 🥷💨",
            f"NANI?! {member.mention}'s smell power level... IT'S OVER 9000! (Dragon Ball Z) ⚡💪",
            f"Believe it, dattebayo! {member.mention} really stinks! (Naruto) 🍜💨",
            f"Za Warudo! Time stops... but {member.mention}'s smell doesn't! (JoJo) ⏰💨",
            f"Yare yare daze... {member.mention} needs a shower! (JoJo) 🚬🚿",
            f"MUDA MUDA MUDA! {member.mention}'s attempts at hygiene! (JoJo) 👊💨",
            f"ORA ORA ORA! {member.mention} vs basic cleanliness! (JoJo) 👊🧼",
            f"{member.mention}'s Stand: 「STINKY FINGERS」! (JoJo) ✋💨",
            f"Kono {member.mention} da! And I smell terrible! (JoJo) 😈💨",
            f"Is this a pigeon? No, it's {member.mention}'s body odor! (Butterfly meme/Anime) 🦋💨",
            f"{member.mention}-san... your smell is sugoi! (Weeb talk) 🎌💨",
            f"Senpai noticed {member.mention}... unfortunately! (Anime trope) 👀💨",
            f"{member.mention} used Talk no Jutsu... it failed because of the smell! (Naruto) 💬💨",
            f"Ultra Instinct can't dodge {member.mention}'s stench! (Dragon Ball) ⚡👃",
            f"{member.mention}'s Bankai: Stinky Blade of Ultimate Funk! (Bleach) ⚔️💨",
            f"Even Death Note couldn't write away {member.mention}'s smell! (Death Note) 📓💨",
            f"{member.mention} is the main character... of a hygiene horror anime! (Anime MC) 📺💀",
            f"Kawaii on the outside, stinky on the inside - {member.mention}! (Kawaii culture) 🎀💨",
            f"{member.mention}'s smell has entered the chat like a Titan! (Attack on Titan) 🗡️👹",
            f"Sasuke left the village because of {member.mention}'s smell! (Naruto) 🏃‍♂️💨",
            f"{member.mention}'s quirk: Eternal Stench! (My Hero Academia) 🦸‍♂️💨",
            f"Even One Punch Man can't one-punch {member.mention}'s smell away! (One Punch Man) 👊💨",
            f"{member.mention} is speed... stinky speed! (Sonic/meme) 💨⚡",
            f"Your next line is 'I should shower' - {member.mention}! (JoJo) 🔮💬",
            f"Za Hando erased {member.mention}'s hygiene! (JoJo) ✋❌",
            f"{member.mention} went Plus Ultra... on being smelly! (My Hero Academia) 💪💨",
            f"Dekiru! {member.mention} can do it... smelling bad! (Anime motivation) 💪💨",
            # DARK HUMOR
            f"{member.mention} smells like they're already halfway to their final destination! ⚰️💀",
            f"Breaking news: {member.mention} has been declared legally dead by smell alone! 📰💀",
            f"{member.mention}'s hygiene died before they did! 🪦🚿",
            f"Even the Grim Reaper holds his nose around {member.mention}! 💀👃",
            f"{member.mention} smells like they're decomposing while still alive! 🧟‍♂️💨",
            f"Plot twist: {member.mention} is patient zero of the smell apocalypse! 🧟‍♂️☣️",
            f"{member.mention}'s smell could wake the dead... then put them back to sleep! ⚰️😴",
            f"If smell could kill, {member.mention} would be a serial killer! 🔪💨",
            f"{member.mention}'s aroma has its own body count! 💀📊",
            f"Warning: {member.mention}'s smell may cause existential crisis! ⚠️🤔",
            f"{member.mention} makes corpses smell like roses by comparison! 🌹⚰️",
            f"Even skeletons have better hygiene than {member.mention}! 💀🧼",
            f"{member.mention}'s smell is so bad, it's considered a war crime in 47 countries! ⚔️🌍",
            f"Scientists study {member.mention} to understand what happens after death! 🧪💀",
            f"{member.mention} smells like they've been marinating in regret and disappointment! 🍖😞",
            f"If {member.mention}'s smell was a disease, it would be terminal! 🏥💀",
            f"{member.mention}'s hygiene flatlined years ago! 📈💀",
            f"The only thing rotting faster than {member.mention}'s teeth is their reputation! 🦷📉",
            f"{member.mention} smells like they're speedrunning decomposition! ⏱️💀",
            f"Darwin's theory can't explain how {member.mention}'s smell evolved! 🐒💨",
            f"{member.mention}'s smell is proof that not all life is precious! 🌱💀",
            f"Even vultures won't circle {member.mention}! 🦅❌",
            f"{member.mention} makes garbage dumps file noise complaints! 🗑️📋",
            f"{member.mention}'s smell is darker than my soul! 🖤💨",
            f"If smell was currency, {member.mention} would crash the economy! 💰📉",
            f"{member.mention} smells like they've given up on life... and life gave up first! 🏳️💀",
            f"The afterlife called, they don't want {member.mention} either! ☎️👻",
            f"{member.mention}'s smell is so bad, it's considered cruel and unusual punishment! ⚖️💨",
            f"Even nihilists find meaning in avoiding {member.mention}! 🤷‍♂️🏃‍♂️",
            f"{member.mention} proves that some things are better left buried! ⚰️💨",
            f"Therapists need therapy after smelling {member.mention}! 🛋️😵",
            # MORE MEMES AND INTERNET CULTURE
            f"Stonks! {member.mention}'s smell value only goes up! 📈💨",
            f"This is fine... said nobody near {member.mention}! 🔥🐕",
            f"Big chungus energy but make it smelly - {member.mention}! 🐰💨",
            f"Doge says: Much stink, very smell, wow - {member.mention}! 🐕💨",
            f"Press F to pay respects to anyone near {member.mention}! ⌨️💀",
            f"{member.mention} is built different... unfortunately! 🏗️💨",
            f"Ratio + {member.mention} smells + L + you fell off (hygienically)! (Twitter) 📱💨",
            f"POV: You're trying to explain deodorant to {member.mention}! 🎭🧴",
            f"{member.mention} said 'periodt' to showering apparently! 💅❌",
            f"Not {member.mention} being the main character of Stink TikTok! 📱💨",
            f"The audacity of {member.mention} existing without soap! 😤🧼",
            f"Ma'am this is a Wendy's... and {member.mention} is stinking it up! 🍟💨",
            f"{member.mention} really said 'let them eat cake' but for smell! 🍰💨",
            f"Gordon Ramsay: This smell is RAW! *points at {member.mention}* 👨‍🍳💨",
            f"Judge Judy would rule against {member.mention}'s hygiene! ⚖️💨",
            f"{member.mention} walked so other stinky people could run... away from soap! 🏃‍♂️🧼"
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

