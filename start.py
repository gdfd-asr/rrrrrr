import os
import time 
from config import *
import shutil

if os.path.exists('Bot.session-journal'):
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Bot.session-journal')
	os.remove(path)
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Bot.session')
	os.remove(path)
	time.sleep(1)
if os.path.exists('Bot.session'):
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Bot.session')
	os.remove(path)
	if os.path.exists('Bot_2.session'):
		path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Bot_2.session')
		os.remove(path)
	time.sleep(1)

from telethon.sync import TelegramClient

client = TelegramClient('Bot',api_id, api_hash)
client.start()
client.disconnect()
if os.path.exists('Bot.session-journal'):
    print('Error')
else:
    print('OK')
    shutil.copyfile("Bot.session", "Bot_2.session")
