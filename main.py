import os
from dotenv import load_dotenv
import discord
import datetime
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

# Replace 'YOUR_BOTTOK_EN' with your actual bot token
load_dotenv()

# Access the bot token from the environment variable
TOKEN = os.environ['TOKEN']

if not TOKEN:
  raise ValueError(
      "Bot token not found in the environment variables. Check your .env file."
  )

# Explicitly define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Add this line to enable message content intent
# Create an instance of the bot with intents
thread_tracking = {}
bot = commands.Bot(command_prefix='!', intents=intents)
SPECIFIC_CHANNEL_ID = 1346163307010330684


@bot.event
async def on_message(message):
  if message.author.bot or message.channel.id != SPECIFIC_CHANNEL_ID:
    return  # Ignore bot messages and messages in other channels

  channel = message.channel
  today = datetime.date.today().isoformat()

  # Check if the thread exists
  thread_info = thread_tracking.get(channel.id, None)

  if not thread_info or thread_info["date"] != today:
    try:
      # Create a new thread
      thread = await channel.create_thread(
          name=f"Daily Updates - {today}",
          type=discord.ChannelType.public_thread,
          # auto_archive_duration=1440,
      )
      thread_tracking[channel.id] = {"thread": thread, "date": today}
    except discord.Forbidden:
      print(f"Missing permissions to create thread in #{channel.name}.")
      return
  else:
    # Fetch existing thread and check if it's archived
    try:
      thread = await bot.fetch_channel(thread_info["thread"].id)
      if thread.archived:  # Unarchive if necessary
        await thread.edit(archived=False)
    except discord.NotFound:
      # If thread was deleted, create a new one
      thread = await channel.create_thread(
          name=f"Daily Updates - {today}",
          type=discord.ChannelType.public_thread,
          # auto_archive_duration=1440,
      )
      thread_tracking[channel.id] = {"thread": thread, "date": today}

  # ✅ Send the message in the thread
  try:
    lines = message.content.splitlines()
    formatted_message = f"**{lines[0]}**\n" + "\n".join(
        lines[1:]) if len(lines) > 1 else f"**{lines[0]}**"

    await thread.send(formatted_message)
  except discord.Forbidden:
    print(f"Bot cannot send messages in {thread.name}. Check permissions.")


# Run the bot
bot.run(TOKEN)
