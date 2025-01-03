import pickle
import os
import discord
from discord import Embed
from discord.ext import commands
import ollama
import asyncio
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor
from app_func import retrieve_relevant_chunks
import activity_log


load_dotenv()

# create discord intent
intents = discord.Intents.default()
intents.message_content = True

# bot identifier
bot = commands.Bot(command_prefix="/", intents=intents)

########################################################################################################################################################

## Discord channel/Bot events

# Add the event handlers from activity_log.py
@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")
    await activity_log.on_ready(bot)

@bot.event
async def on_message(message):
    await activity_log.on_message(bot, message)

@bot.event
async def on_message_edit(before, after):
    await activity_log.on_message_edit(bot, before, after)

@bot.event
async def on_message_delete(message):
    await activity_log.on_message_delete(bot, message)

@bot.event
async def on_member_join(member):
    await activity_log.on_member_join(bot, member)

@bot.event
async def on_member_remove(member):
    await activity_log.on_member_remove(bot, member)

@bot.event
async def on_reaction_add(reaction, user):
    await activity_log.on_reaction_add(bot, reaction, user)

@bot.event
async def on_reaction_remove(reaction, user):
    await activity_log.on_reaction_remove(bot, reaction, user)

########################################################################################################################################################

## Knowledge base creation and extraction

# Check if the pickle file exists
pickle_file = 'knowledge_embeddings.pkl'

if os.path.exists(pickle_file):
    print("Knowledge base exists")
    with open(pickle_file, 'rb') as f:
        knowledge_embeddings = pickle.load(f)
else:
    print("Knowledge base doesn't exist. Creating a new one...")
    with open('pre_work.py') as f:
        exec(f.read())
    with open(pickle_file, 'rb') as f:
        knowledge_embeddings = pickle.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

########################################################################################################################################################

## Bot commands

# /hello command answers the below text
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello! I am a bot designed to answer your questions about 'The Lord of the Rings' books. To ask a question, simply type '/ask' then your question. If you'd like to create a private chat thread, use '/private', and to summarize the recent response contents, type '/summarize' (Quick tip: Use /summarize in your private chat thread). Let’s explore Middle-earth together!")

@bot.command()
async def private(ctx):
    # Ensure the command is used in a text channel, not DM
    if isinstance(ctx.channel, discord.TextChannel):
        # Create a thread and restrict access to the user who invoked the command
        thread = await ctx.channel.create_thread(
            name=f"Private chat with {ctx.author.name}",
            # type=discord.ChannelType.public_thread,
            type = discord.ChannelType.private_thread,
        )
        # Delete the original command message ("/private") after 5 seconds
        await asyncio.sleep(5)
        await ctx.message.delete() # delete '/private' message from the public chat
        await thread.add_user(ctx.author)  # Add the user to the thread

        # await ctx.send(f"A private thread has been created for you: {thread.mention}")
        await thread.send(f"Hello {ctx.author.mention}! This is your private thread. It will auto-delete after 10 minutes of inactivity.")

        # Wait for 10 minutes (600 seconds) before deleting the thread
        await asyncio.sleep(600)  # Adjust the time as needed
        if thread and thread.last_message_id:  # Check if the thread still exists
            try:
                await thread.delete()
                print(f"Deleted thread: {thread.name}")
            except discord.errors.NotFound:
                print(f"Thread {thread.name} was already deleted.")


@bot.command(name="ask")
async def ask(ctx, *, message):
    loop = asyncio.get_event_loop()

    # logging message/query sent
    await activity_log.qna_message(1, ctx, bot, message)
    
    # Run the compute-intensive task in a thread pool
    def LLM_model():
        # print("Number of embeddings", len(knowledge_embeddings))
        relevant_chunks = retrieve_relevant_chunks(message, knowledge_embeddings)
        # print("Chunks: ", len(relevant_chunks))
        if relevant_chunks is None:
            return None, "The question/query is not related to the book. Perhaps ask something related to the LOTR book series?"
        else:
            print(message)
            context_ = " ".join(relevant_chunks)  # Combine top K chunks into a single context string
            context_prompt = f"""
            You must only respond to the {message} based on the provided {context_}. Do not make up answers, and do not use external or general knowledge. The relevant response should be conveyed concisely in no more than 1000 words.
            ```
            f"context_: {context_}\n Query: {message}"
            ```
            """

            response = ollama.chat(model='llama3.1', messages=[
                {"role": "system", "content": (
                f"You must only respond based on the provided {context_}. Do not make up answers, "
                "and do not use external or general knowledge."
                "The relevant response should be conveyed concisely in no more than 1000 words."
                )},
                {"role": "user", "content": context_prompt,}
            ])
            return response['message']['content'], None
        
    # Acknowledge user input and inform about processing
     # Send acknowledgment under the user's query
    processing_message = await ctx.reply("Processing your query, please wait...", mention_author=False)
  
    # Run the compute function in a thread pool
    result, error_message = await loop.run_in_executor(ThreadPoolExecutor(), LLM_model)

    # Delete the processing message
    await processing_message.delete()

    if error_message:
        print(error_message)
        await ctx.reply(error_message, mention_author=False)
        await activity_log.qna_message(0, ctx, bot, error_message)
    else:
        print("Relevant \n")
        print(result)
        # await ctx.send(result)
        await ctx.reply(result, mention_author=False)
        await activity_log.qna_message(0, ctx, bot, result)

@bot.command(name="summarize")
async def summarize(ctx):
    msgs = [ message.content async for message in ctx.channel.history(limit=10)]
    summarize_prompt = f"""
        summarize the following messages delimited by 5 backticks:
        ```
        {msgs}
        ```
    """

    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'system',
         'content': 'You are a helpful assistant who summarizes the provided messages concisely in no more than 1000 words.',
         },
         {'role': 'user', 
          'content': summarize_prompt,
        }
    ])
    print(response['message']['content'])
    await ctx.send(response['message']['content'])

########################################################################################################################################################

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

