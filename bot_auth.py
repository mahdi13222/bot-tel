import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

# define constant parameters from env file
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# instantiate a Client object to get an authorized bot session
app = Client(
    "myBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

app.run()
