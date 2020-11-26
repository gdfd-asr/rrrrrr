from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlighter import SQLighter
# инициализируем соединение с БД
db = SQLighter('db.db')
def kb0():
	markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
	item1 = KeyboardButton(text="Добавить канал")
	item2 = KeyboardButton(text="Удалить канал")
	item3 = KeyboardButton(text="Изменить канал")
	markup.add(item1,item2,item3)
	return markup

def back():
	markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
	item1 = KeyboardButton(text="Назад")
	markup.add(item1)
	return markup

def back_1():
	n = 0
	markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
	cotegory = db.get_cotegory()
	if len(cotegory)%2 == 0:
		for i in cotegory:
			item1 = KeyboardButton(str(cotegory[n]))
			n+=1
			if n == len(cotegory):
				break
			item2 = KeyboardButton(str(cotegory[n]))
			if n%2 == 1:
				markup.add(item1, item2)
	else:
		item3 = KeyboardButton(str(cotegory[-1]))
		cotegory.pop(-1)
		for i in cotegory:
			item1 = KeyboardButton(str(cotegory[n]))
			n+=1
			if n == len(cotegory):
				break
			item2 = KeyboardButton(str(cotegory[n]))
			if n%2 == 1:
				markup.add(item1, item2)
		markup.add(item3)
	item3 = KeyboardButton("Назад")
	markup.add(item3)


	return markup
