import os
import openai
import discord
from discord.ext import commands

# Set up OpenAI API key
openai.api_key = "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"

# Set up Discord bot
TOKEN = "MTA4NTgxNDg3MTc2NzEzODMzNQ.Gsp2eh.gBOUvaXJpF8A0XBmEU2OJlMqIFjhidSOpDuaAE"
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


# Set up GPT-4 completion function
async def gpt4_complete(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with the GPT-4 engine name when available
        messages=prompt,
    )
    message = response['choices'][0]['message']['content'].strip()
    return message

# Create a command for the Discord bot
@bot.command(name='gpt4', help='Ask GPT-4 a question')
async def gpt4(ctx, *, question: str):
    prompt = [{"role": "user", "content": f"{question}"}]
    response = await gpt4_complete(prompt)
    await ctx.send(response)

# Run the bot
bot.run(TOKEN)
