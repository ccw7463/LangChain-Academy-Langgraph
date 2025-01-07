import sys
import random
from operator import add
from dataclasses import dataclass
from typing import Literal, Annotated
from typing_extensions import TypedDict
from IPython.display import Image, display
from ml_collections import ConfigDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, RemoveMessage, trim_messages
from langgraph.graph.message import add_messages
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from pydantic import BaseModel, field_validator, ValidationError
from utils.util import *
ShortTermMemory = MemorySaver()
LongTermMemory = InMemoryStore()
set_env()
llm = ChatOpenAI(model="gpt-4o")