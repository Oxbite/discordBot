import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
load_dotenv()

# Access the bot token from the environment variable
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError("Bot token not found in the environment variables. Check your .env file.")


# Explicitly define intents
intents = discord.Intents.default()
intents.members = True
intents.messages = True  # Add this line to enable message content intent
role_name = "codingGeek"
# Create an instance of the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for when a member joins the server
@bot.event
async def on_member_join(member):
    try:
        # Send a welcome message to the new member
        welcome_message = (
            "🚀 **Join Our Exclusive Boot Camp!**\n\n"
            "🔥 Elevate your skills and level up your knowledge in our upcoming Boot Camp! 🔥\n\n"
            "📅 **Date:** Jan 10th, 2024\n"
            "📍 **Location:** Online in our Discord Server!!\n\n"
            "🌟 **What to Expect:**\n"
            "- Comprehensive sessions covering HTML, CSS, and JavaScript\n"
            "- Hands-on projects to build real-world applications\n"
            "- Expert guidance from seasoned web developers\n"
            "- Networking opportunities within the tech community\n\n"
            "🎓 **Who Should Attend:**\n"
            "- Aspiring Web Developers\n"
            "- Students pursuing Web Development\n"
            "- Professionals looking to add web development to their skill set\n\n"
            "🔗 **Register Now:** https://www.oxbite.com/bootcamp2024\n\n"
            "👉 Don't miss out on this fantastic opportunity to dive into the world of web development! "
            "Limited spots available, so secure your spot now! 👈"
        )
        await member.send(welcome_message)

        # Get the role named "codingGeek"
        role = discord.utils.get(member.guild.roles, name=role_name)

        # If the role is found, assign it to the member
        if role:
            await member.add_roles(role)
            print(f"Assigned the role '{role_name}' to {member.name}")
        else:
            print(f"Role '{role_name}' not found. Make sure the role exists.")
    except discord.Forbidden:
        # If the bot doesn't have permission to send DMs or assign roles, handle the error
        print(f"Failed to send a welcome message or assign the role to {member.name}. Missing permissions.")


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

# Run the bot
bot.run(TOKEN)
