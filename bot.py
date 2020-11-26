import asyncio
import sys
import os
import time 
from googletrans import Translator

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from telethon.sync import TelegramClient
from telethon import TelegramClient,events, sync
from telethon import functions
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.client.users import UserMethods

from sqlighter import SQLighter
import keyboards as kb
from config import *

translator = Translator()

class reg(StatesGroup):
	STATE_0 = State()
	STATE_1 = State()
	STATE_2 = State()
	STATE_3 = State()
	STATE_4 = State()
	STATE_5 = State()

# инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

if os.path.exists('Bot.session-journal'):
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Bot.session-journal')
	os.remove(path)
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Bot.session')
	os.remove(path)
	time.sleep(1)

#client = TelegramClient('Bot',api_id, api_hash)
	
# инициализируем соединение с БД
db = SQLighter('db.db')

async def rer(cotegory):
	r = await client.get_dialogs()
	for i in r:
		if cotegory == i.title:
			return True
	return False

@dp.message_handler(commands=['start'], content_types=types.ContentTypes.TEXT)
async def process_admin_command(message: types.Message, state: FSMContext):
	if(not db.subscriber_exists(message.from_user.id)):
		db.add_db(message.from_user.id,message.from_user.first_name)
	if admin_id == message.from_user.id:
		await message.answer('Добро пожаловать! Доступные для вас команды', reply_markup=kb.kb0())

@dp.message_handler(commands=['set'], content_types=types.ContentTypes.TEXT)
async def process_admin_command(message: types.Message, state: FSMContext):
	if admin_id == message.from_user.id:
		if message['chat']['title'] in db.get_filter():
			db.chat_id(message['chat']['id'],message['chat']['title'])
			await message.answer('Настройка бота закончена')
		else:
			await message.answer('Ошибка настройки бота, такого канала получения нет')
		

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def first_test_state_case_met(message: types.Message, state: FSMContext):
	response = message.text.lower()
	try:
		if admin_id == message.from_user.id:
			if response == 'добавить канал':
				await message.answer('Введите имя канала из которого будут браться сообщения', reply_markup=kb.back())
				await reg.STATE_1.set()
			elif response == 'удалить канал':
				await message.answer('Введите имя канала', reply_markup=kb.back_1())
				await reg.STATE_2.set()
			elif response == 'изменить канал':
				await message.answer('Введите имя канала для которого хотите поменять получаймый канал', reply_markup=kb.back_1())
				await reg.STATE_4.set()
			else:
				await message.answer('Такой команды нет', reply_markup=kb.kb0())
		else:
			await message.answer('Такой команды нет')
	except Exception as e:
		print(e)
		await message.reply('ошибка', reply=False, reply_markup=kb.kb0())
		await state.finish()

@dp.message_handler(state=reg.STATE_4, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
	response = message.text
	try:
		if response.lower() == 'назад':
			await message.reply('Возвращаю в панель управления', reply=False, reply_markup=kb.kb0())
			await state.finish()
		else:
			if db.subscriber_cotegory(response):
				if await rer(response):
					await state.update_data(cotegory=response)
					await message.reply(f'Введите новый канал в который будут отправляться сообщения из {response}', reply=False, reply_markup=kb.back())
					await reg.STATE_5.set()
				else:
					await message.reply('Вы не подписаны на данный канал')
			else:
				await message.reply('Данный канал не добавлен,введите другой или добавте его')
	except Exception as e:
		print(e)
		await message.reply('ошибка', reply=False, reply_markup=kb.kb0())
		await state.finish()

@dp.message_handler(state=reg.STATE_5, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
	response = message.text
	try:
		if response.lower() == 'назад':
			await message.reply('Возвращаю в панель управления', reply=False, reply_markup=kb.kb0())
			await state.finish()
		else:
			data = await state.get_data()
			cotegory = data['cotegory']
			await message.reply(f'Для канала получение {cotegory} обнавлён канал получатель {response}', reply=False,reply_markup=kb.kb0())
			await message.reply(f'Обязательно добавить бота в {response} и напишите /set')
			db.update_cotegory(cotegory, response)
			await state.finish()	

	except Exception as e:
		print(e)
		await message.reply('ошибка', reply=False, reply_markup=kb.kb0())
		await state.finish()

@dp.message_handler(state=reg.STATE_2, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
	response = message.text
	try:
		if response.lower() == 'назад':
			await message.reply('Возвращаю в панель управления', reply=False, reply_markup=kb.kb0())
			await state.finish()
		else:
			if db.subscriber_cotegory(response):
				await message.reply(f'Канал {response} удалён', reply=False, reply_markup=kb.kb0())
				db.dekete_cotegory(response)
				await state.finish()
			else:
				await message.reply('Такой канал вы не добавляли')
	except Exception as e:
		print(e)
		await message.reply('ошибка', reply=False, reply_markup=kb.kb0())
		await state.finish()

@dp.message_handler(state=reg.STATE_1, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
	response = message.text
	try:
		if response.lower() == 'назад':
			await message.reply('Возвращаю в панель управления', reply=False, reply_markup=kb.kb0())
			await state.finish()
		else:
			if (not db.subscriber_cotegory(response)):
				if await rer(response):
					await state.update_data(cotegory=response)
					await message.reply('Введите канал в который будут отправляться сообщения(не забудьте добавить бота в этот канал и написать /start)', reply=False, reply_markup=kb.back())
					await reg.STATE_3.set()
				else:
					await message.reply('Вы не подписаны на данный канал')
			else:
				await message.reply('Данный канал уже добавлен, удалите его или введите другой')
	except Exception as e:
		print(e)
		await message.reply('ошибка', reply=False, reply_markup=kb.kb0())
		await state.finish()
		 
@dp.message_handler(state=reg.STATE_3, content_types=types.ContentTypes.TEXT)
async def fname_step(message: types.Message, state: FSMContext):
	response = message.text
	try:
		if response.lower() == 'назад':
			await message.reply('Возвращаю в панель управления', reply=False, reply_markup=kb.kb0())
			await state.finish()
		else:
			data = await state.get_data()
			cotegory = data['cotegory']
			await message.reply(f'Канал получение {cotegory} добавлен и канал получатель {response}', reply=False,reply_markup=kb.kb0())
			db.add_cotegory(cotegory, response)
			await state.finish()	

	except Exception as e:
		print(e)
		await message.reply('ошибка', reply=False, reply_markup=kb.kb0())
		await state.finish()

async def shutdown(dispatcher: Dispatcher):
	await dispatcher.storage.close()
	await dispatcher.storage.wait_closed()
	
"""@client.on(events.NewMessage())
async def normal_handler(event):
	try:
		some_id = event.chat_id
		r = await client.get_entity(PeerChannel(some_id))
	except Exception as e:
		some_id = (-1)*(event.chat_id)
		r = await client.get_entity(PeerChat(some_id))
		pass
	s = event.raw_text
	t = db.get_cotegory()
	r = r.title
	if r in t:
		chat_id = db.channe_id(r)
		re = event.media
		try:
			result = translator.translate(str(s),src='en',dest='ru')
			result = result.text
			if result != s:
				result = f'Оригинал текста:\n{s}\nПеревод:\n{result}'
		except Exception as e:
			print(e)
			result = s
			pass
		if re != None:
			await client.download_media(message=re, file= f'photo.jpg')
			await bot.send_photo(chat_id, open('photo.jpg', 'rb'),result)
			path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'photo.jpg')
			os.remove(path)
		else:
			await bot.send_message(chat_id,result)"""


#async def starte():
#	await client.run_until_disconnected()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	#client.start()
	#loop.create_task(starte())
	db.create_base()
	executor.start_polling(dp, on_shutdown=shutdown)
	executor.start_polling(dp, skip_updates=True)