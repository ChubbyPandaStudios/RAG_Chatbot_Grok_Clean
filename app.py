
# imports for running Chatbot
import os
import gradio as gr
from xai_sdk import Client
from xai_sdk.chat import user
from dotenv import load_dotenv

# pull custom image assets (purple thunderbolt)
#gr.set_static_paths(paths=["assets/"])

# load XAI_API_Key from .env file
load_dotenv()

# get api key from the environment, securely
api_key = os.getenv("XAI_API_KEY")

# check to see if api key is working properly.
# will comment out code block later but keep for documenting purposes
'''
if api_key:
    print("API key loaded successfully (first 10 chars):", api_key[:10] + "...")
else:
    print("ERROR: API key not found! Check your .env file.")
    #ran successful API is active now
'''

#create grok client
client = Client(api_key = api_key)

#print("Grok client initialized — ready to chat!")

def grok_chat(message, history):
    # Start new conversation
    conversation = client.chat.create(model="grok-4")

    # Safely add previous user messages from history
    for turn in history:
        if isinstance(turn, (list, tuple)) and len(turn) > 0 and turn[0]:
            conversation.append(user(turn[0]))

    # Add the current user message
    conversation.append(user(message))

    # Stream response
    partial_response = ""
    for full_response, chunk in conversation.stream():
        if chunk.content:
            partial_response += chunk.content
            yield partial_response

# creating chat interface with gradio, calls grok_chat function
# full UI plus fetching through grok API
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.ChatInterface(
        fn=grok_chat,                   # grok_chat function defined above
        title="🗲 Grok-4 Chatbot (Basic)",
        description="A simple chat with Grok-4 using the xAI API by Andrew Dykeman",
        examples=["Explain CNN's like you are an expert computer vision tutor", 
                  "Explain quantum computing as if your are an expert tutor in the field",
                  "Who is the true expert, Elliot or Andrew?"],
        chatbot = gr.Chatbot(
            height = 600,
            avatar_images = (None, "https://x.ai/favicon.ico") #avatar_images = (None, "assets/chat_icon.png") changed to url
        )
    )

# Launch the app
demo.launch()

'''Completed flow, chat icon is now a statis url instead of downlowded asset,
hugging face was failing to sync because of the png files in assets. The PNG files allowed for more customization,
but continued having issues with whhen syncing to huggingface'''

#checking