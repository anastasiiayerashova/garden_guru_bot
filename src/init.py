import os
from dotenv import load_dotenv

from utils import BotSettings
from tools import tools_list

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()

# model + params
chat_model = ChatOpenAI(model=BotSettings.MODEL_NAME.value,
                        temperature=BotSettings.TEMPERATURE.value)

# agent + tools
memory = MemorySaver()
agent = create_agent(model=chat_model, 
                     tools=tools_list, 
                     system_prompt=BotSettings.SYSTEM_PROMPT.value,
                     checkpointer=memory)

