import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time

import sys, os
from dotenv import load_dotenv
# include .env file
load_dotenv(".env")
# now we can import from ./parser dir
sys.path.append('parser/')
from web_worker import *

# load telegram API key fron .env
bot = telebot.TeleBot(os.getenv("MY_KEY"))


# create base menu keyboard
keyboard_menu = types.InlineKeyboardMarkup(row_width=2)
key_markets = types.InlineKeyboardButton(text='Площадки', callback_data='markets_query')
key_category = types.InlineKeyboardButton(text='Категории', callback_data='categories_query')
key_regions = types.InlineKeyboardButton(text='Регионы', callback_data='districts_query')
key_start_price = types.InlineKeyboardButton(text='Начальная стоимость', callback_data='start_price_query')
key_end_price = types.InlineKeyboardButton(text='Текущая стоимость', callback_data='end_price_query')
key_search = types.InlineKeyboardButton(text='Найти лоты', callback_data='search')
key_text = types.InlineKeyboardButton(text='Поиск по словам', callback_data='search_query_text')
keyboard_menu.add(key_start_price, key_end_price, key_markets, key_regions, key_category, key_text)
keyboard_menu.add(key_search)
keyboard_districts = types.InlineKeyboardMarkup(row_width=1)
key_1 = types.InlineKeyboardButton(text='Центральный федеральный округ', callback_data='regions_query_1')
key_2 = types.InlineKeyboardButton(text='Северо-Западный федеральный округ', callback_data='regions_query_2')
key_3 = types.InlineKeyboardButton(text='Южный федеральный округ', callback_data='regions_query_3')
key_4 = types.InlineKeyboardButton(text='Северо-Кавказский федеральный округ', callback_data='regions_query_4')
key_5 = types.InlineKeyboardButton(text='Приволжский федеральный округ', callback_data='regions_query_5')
key_6 = types.InlineKeyboardButton(text='Уральский федеральный округ', callback_data='regions_query_6')
key_7 = types.InlineKeyboardButton(text='Сибирский федеральный округ', callback_data='regions_query_7')
key_8 = types.InlineKeyboardButton(text='Дальневосточный федеральный округ', callback_data='regions_query_8')
keyboard_districts.add(key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8)
keyboard_prices_start = types.InlineKeyboardMarkup(row_width=2)
key_1 = types.InlineKeyboardButton(text='Стартовая цена (от)', callback_data='start_query_from')
key_2 = types.InlineKeyboardButton(text='Стартовая цена (до)', callback_data='start_query_to')
keyboard_prices_start.add(key_1, key_2)
keyboard_prices_current = types.InlineKeyboardMarkup(row_width=2)
key_1 = types.InlineKeyboardButton(text='Текущая цена (от)', callback_data='current_query_from')
key_2 = types.InlineKeyboardButton(text='Текущая цена (до)', callback_data='current_query_to')
keyboard_prices_current.add(key_1, key_2)


#load filter params template
with open("filter_template.json", 'r', encoding='utf-8') as file2:
	web_worker = WebWorker(json.load(file2))


@bot.message_handler(commands=['start'])
def get_start(message):
	"""start message handler"""
	bot.send_message(message.from_user.id, text="Добро пожаловать в Торги по банкротству РФ!", reply_markup=keyboard_menu)




def print_lot(lot, chat_id):
	"""send lot info to user"""
	# check errors
	if isinstance(lot, dict) == False:
		return None

	# make message text
	full_description = lot.get('description').get('full')[:1200]+"..."
	msg = f"<strong>Цена - {lot['cost']['current']}, {lot['description']['title']}</strong>" + '\n\n'\
	f"{lot['bidding_type']}" + '\n\n'\
	f"{full_description}" + '\n\n' \
	f"Место осмотра: {lot['region']}" + '\n\n'\
	f"Дата проведения торгов: {lot['date']['bidding']}" + '\n\n'\
	f"Дата начала представления заявок на участие: {lot['date']['start_bid']}" + '\n\n'\
	f"Дата окончания представления заявок на участие: {lot['date']['end_bid']}" + '\n\n'\
	f"Начальная цена, руб.: {lot['cost']['current']}" + '\n\n'\
	f"Шаг цены: {lot['cost']['step']}"

	# make album with photo
	media = [InputMediaPhoto(i) for i in lot["pictures"] if lot["pictures"]]
	if media:
		bot.send_media_group(chat_id=chat_id, media=media[:5])
	bot.send_message(chat_id=chat_id, text = msg)

	"""contact button"""
	keyboard_contacts = types.InlineKeyboardMarkup()
	key_to_buy = types.InlineKeyboardButton(text='Связаться', callback_data="adm")
	keyboard_contacts.add(key_to_buy)
	bot.send_message(text='Связаться с агентом', chat_id=chat_id, reply_markup=keyboard_contacts)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	# "search" pressed
	if call.data == "search":
		if web_worker._lots_info:
			for i in web_worker.get_lots_info():
				print_lot(i, call.message.chat.id)
			# load menu keyboard
			bot.send_message(call.message.chat.id, text="Еще немного лотов?", reply_markup=keyboard_menu)
		else:
			bot.send_message(call.message.chat.id, text="Кажется, лоты закончились :(")

	else:
		# "contact" is processed here







bot.polling(none_stop=True)