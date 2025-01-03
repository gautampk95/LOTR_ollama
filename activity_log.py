from discord.ext import commands
import datetime

# Log file path
LOG_FILE = "discord_activity_log.txt"
QA_FILE = "chatbot_qna.txt"

def log_to_file(content):
    """Write log messages to a file with timestamps."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {content}\n")

def q_and_a(content):
    """Write log messages to a file with timestamps."""
    if content != "\n\n":
        with open(QA_FILE, "a", encoding="utf-8") as qna:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            qna.write(f"[{timestamp}] {content}\n")
    else:
        with open(QA_FILE, "a") as qna:
            qna.write(f"{content}")

async def on_ready(bot):
    """Event when the bot is online and ready."""
    # print(f"Logged in as {bot.user}")
    log_to_file(f"Bot is ready as {bot.user.name}")

async def on_message(bot, message):
    """Event when a message is sent in the server."""
    if not message.author.bot:  # Ignore bot messages
        log_to_file(f"Message by {message.author} in {message.channel}: {message.content}")
    await bot.process_commands(message)

async def qna_message(writer, user, bot, content):
    """Event when a conversation with Chatbot is done"""
    if writer == 1:
        q_and_a(f"Query/question by {user.author.name} in {user.channel}: {content}")
    else:
        q_and_a(f"Response by {bot.user.name} in {user.channel}: {content}")
        q_and_a("\n\n")

async def on_message_edit(bot, before, after):
    """Event when a message is edited."""
    if not before.author.bot:
        log_to_file(f"Message edited by {before.author} in {before.channel}: '{before.content}' -> '{after.content}'")

async def on_message_delete(bot, message):
    """Event when a message is deleted."""
    if not message.author.bot:
        log_to_file(f"Message deleted by {message.author} in {message.channel}: '{message.content}'")

async def on_member_join(bot, member):
    """Event when a new member joins the server."""
    log_to_file(f"Member joined: {member.name}#{member.discriminator}")

async def on_member_remove(bot, member):
    """Event when a member leaves the server."""
    log_to_file(f"Member left: {member.name}#{member.discriminator}")

async def on_reaction_add(bot, reaction, user):
    """Event when a reaction is added to a message."""
    log_to_file(f"Reaction added by {user} in {reaction.message.channel}: {reaction.emoji}")

async def on_reaction_remove(bot, reaction, user):
    """Event when a reaction is removed from a message."""
    log_to_file(f"Reaction removed by {user} in {reaction.message.channel}: {reaction.emoji}")
