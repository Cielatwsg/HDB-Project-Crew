import os
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken
import streamlit as st
from crewai_tools import BrowserbaseLoadTool
from crewai_tools import WebsiteSearchTool
from datetime import datetime

#load_dotenv('.env')

if load_dotenv('.env'):
    #for local development 
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else: 
    OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
#client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key = OPENAI_KEY)

def tool_websearch(url):
    browsertool = BrowserbaseLoadTool(url)
    return [browsertool]

def tool_websearch2(url):
    webtool = WebsiteSearchTool(url)
    return [webtool]

def get_today_date():
    # Get today's date
    today = datetime.now().date()
    return today

# This function is for calculating the tokens given the "message"
# ⚠️ This is simplified implementation that is good enough for a rough estimation
def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))
