# import libraries
import streamlit as st
import config as secrets
import os, json, chardet
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import tool
import ChatOpenAI

# streamlit secrets
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
OPENAI_ORGANIZATION = st.secrets['OPENAI_ORGANIZATION']
system_prompt = st.secrets['system_prompt']
TAVILY_API=st.secrets['TAVILY_API']

llm = ChatOpenAI(model_name="gpt-4o", 
                 temperature=0.5, 
                 openai_api_key=OPENAI_API_KEY, 
                 organization=OPENAI_ORGANIZATION)