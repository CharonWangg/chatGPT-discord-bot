import os
from .revchatgpt import CustomChatbot
from dotenv import load_dotenv
from src import personas
from typing import Union
from asgiref.sync import sync_to_async

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENGINE = os.getenv("GPT_ENGINE")
CHAT_MODEL = os.getenv("CHAT_MODEL")

def get_chatbot_model(model_name: str) -> CustomChatbot:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if model_name == "GPT4":
        return CustomChatbot(api_key=openai_api_key, engine="gpt-4")
    return CustomChatbot(api_key=openai_api_key, engine=ENGINE)

chatbot = get_chatbot_model(CHAT_MODEL)

async def official_handle_response(message) -> str:
    return await sync_to_async(chatbot.ask)(message)

async def unofficial_handle_response(message) -> str:
    async for response in chatbot.ask(message):
        responseMessage = response["message"]

    return responseMessage

# resets conversation and asks chatGPT the prompt for a persona
async def switch_persona(persona) -> None:
    chatbot.reset()
    await sync_to_async(chatbot.ask)(personas.PERSONAS.get(persona))

