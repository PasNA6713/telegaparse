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

load telegram API key fron .env
bot = telebot.TeleBot(os.getenv("MY_KEY"))
# bot = telebot.TeleBot("1205043047:AAEhXjkWNG6UdE1zaa6YPuDJaKwe5ni0_50")

# all user's data using the TG-bot
user_data = {}

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

# function for loading of lot's info
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
	bot.send_message(chat_id=chat_id, text = msg, parse_mode="html")

	"""contact button"""
	keyboard_contacts = types.InlineKeyboardMarkup()

	user_data[chat_id].params["urls"][user_data.get(chat_id).counter] = lot.get("marketplace").get("url")
	user_data[chat_id].counter += 1

	key_to_buy = types.InlineKeyboardButton(text='Связаться', callback_data=f"adm_{user_data.get(chat_id).counter}")
	keyboard_contacts.add(key_to_buy)
	bot.send_message(text='Связаться с агентом', chat_id=chat_id, reply_markup=keyboard_contacts)


# function of a button "Назад" from menu
def make_back_from_menu(call):
    alert_text = f"Вы настроили {call.message.text.split()[1]}!"
    bot.answer_callback_query(call.id, show_alert=True, text=alert_text)
    bot.edit_message_text(text="Настрой фильтр", chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard_menu)

# simple alert function
def accepted(message):
    message = bot.send_message(chat_id=message.chat.id, text='Принято')
    bot.edit_message_text(text="Что-то еще настроим?", chat_id=message.chat.id, message_id=message.message_id,
                          reply_markup=keyboard_menu)

# one of users of TG-bot
class User:

    def __init__(self):
        with open("template_params.json", 'r', encoding='utf-8') as file:
            template_params = json.load(file)
        with open("filter_template.json", 'r', encoding='utf-8') as file2:
            filter_params = json.load(file2)
        self.params = template_params.copy()
        self.filter = filter_params.copy()
        self.changed = False
        self.web_worker = ""
        self.counter = 0

    def get_price_start_from(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["start_price"]["from"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_start)

    def get_price_start_to(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["start_price"]["to"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_start)

    def get_price_current_from(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["current_price"]["from"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_current)

    def get_price_current_to(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["current_price"]["to"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_current)

    def get_text_query(self, message):
        self.filter["search_text"] = message.text
        accepted(message)

    def make_price(self, call):
        if call.data.split("_")[0] == "start":
            if call.data.split("_")[2] == "from":
                text = "Введи стартовую стоимость (от)"
                message = bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                                message_id=call.message.message_id)
                bot.register_next_step_handler(message, self.get_price_start_from)
            else:
                text = "Введи стартовую стоимость (до)"
                message = bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                                message_id=call.message.message_id)
                bot.register_next_step_handler(message, self.get_price_start_to)
        else:
            if call.data.split("_")[2] == "from":
                text = "Введи текущую стоимость (от)"
                message = bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                                message_id=call.message.message_id)
                bot.register_next_step_handler(message, self.get_price_current_from)
            else:
                text = "Введи текущую стоимость (до)"
                message = bot.edit_message_text(text=text, chat_id=call.message.chat.id,
                                                message_id=call.message.message_id)
                bot.register_next_step_handler(message, self.get_price_current_to)

    def make_text_query(self, call):
        message = bot.edit_message_text(text="Введи поисковой запрос", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
        bot.register_next_step_handler(message, self.get_text_query)

    def make_menu_from_districts(self, call):
        keys_lst = []
        keyboard_filter_params = types.InlineKeyboardMarkup(row_width=2)

        for district in self.params.get("districts"):
            if "query" in call.data:
                if self.params.get("districts").get(district).get("code") == call.data.split("_")[2]:
                    selected_regions = self.params.get("districts").get(district).get("regions")
                    break
            else:
                for district in self.params.get("districts"):
                    if int(call.data.split("_")[1]) in self.params.get("districts").get(district).get("regions"):
                        selected_regions = self.params.get("districts").get(district).get("regions")

        for region in self.params.get("regions"):
            if int(self.params.get("regions").get(region)[0]) in selected_regions:
                if self.params.get("regions").get(region)[1]:
                    btn_text = f"✅{region}"
                else:
                    btn_text = region
                key = types.InlineKeyboardButton(text=btn_text,
                                                 callback_data=f"btnRegions_{self.params.get('regions').get(region)[0]}")

                keys_lst.append(key)

        key = types.InlineKeyboardButton(text="◀️Назад", callback_data='back_menu')
        keys_lst.append(key)
        keyboard_filter_params.add(*keys_lst)
        bot.edit_message_text(text='Выбери параметр', chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_filter_params)

    def make_menu(self, call):
        keys_lst = []

        filter_parameter = call.data.split("_")[0]

        if "btn" in filter_parameter:
            filter_parameter = filter_parameter[3:].lower()
        row_width = 2

        if call.data == "markets_query" or "btnMarkets" in call.data:
            row_width = 1

        keyboard_filter_params = types.InlineKeyboardMarkup(row_width=row_width)
        for item in self.params.get(filter_parameter).keys():
            if self.params.get(filter_parameter).get(item)[1]:
                btn_text = f"✅{item}"
            else:
                btn_text = item
            buf = self.params.get(filter_parameter).get(item)[0]
            callback_data = f"btn{filter_parameter.capitalize()}_{buf}"
            key = types.InlineKeyboardButton(text=btn_text,
                                             callback_data=callback_data)
            keys_lst.append(key)
        key = types.InlineKeyboardButton(text="◀️Назад", callback_data='back_menu')
        keys_lst.append(key)
        keyboard_filter_params.add(*keys_lst)
        bot.edit_message_text(text='Выбери параметр', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=keyboard_filter_params)


@bot.message_handler(commands=['start'])
def get_start(message):
	"""start message handler"""
	bot.send_message(message.from_user.id, text="Добро пожаловать в Торги по банкротству РФ!", reply_markup=keyboard_menu)
	user_data[message.chat.id] = User()
	user_data[message.chat.id].params["username"] = message.from_user.username
	print(message.chat.id)
	print(message.from_user.username)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	# "search" pressed
	current_user = user_data.get(call.message.chat.id)
	# if user has pressed start (checking)
	if current_user:
		if call.data == "search":
			for district in current_user.params.get("districts"):

				for region in current_user.params.get("districts").get(district).get("regions"):

					if str(region) in current_user.filter.get("regions"):

						if current_user.params.get("districts").get(district).get("code") not in current_user.filter[
							"districts"]:
							current_user.filter["districts"].append(

								current_user.params.get("districts").get(district).get("code"))

							continue

			if current_user.changed or current_user.web_worker == "":
				current_user.web_worker = WebWorker(current_user.filter)

				current_user.changed = False

				if current_user.web_worker._lots_info:
					for i in current_user.web_worker.get_lots_info():
						print_lot(i, call.message.chat.id)

					# load menu keyboard
					bot.send_message(call.message.chat.id, text="Еще немного лотов?", reply_markup=keyboard_menu)
				else:
					bot.send_message(call.message.chat.id, text="Кажется, лоты закончились :(")

		# if was pressed "Категории" or "Площадки"
		elif call.data == "markets_query" or call.data == "categories_query":

			current_user.make_menu(call)


		# if was pressed "Регионы"
		elif call.data == "districts_query":

			bot.edit_message_text(text='Выбери округ', chat_id=call.message.chat.id, message_id=call.message.message_id,

								  reply_markup=keyboard_districts)

		# after was pressed "Регионы" and pressed an each appeared button
		elif "regions_query" in call.data:

			current_user.make_menu_from_districts(call)

		# if was pressed "Начальная стоимость"
		elif call.data == "start_price_query":

			bot.edit_message_text(text='Выбери', chat_id=call.message.chat.id, message_id=call.message.message_id,

								  reply_markup=keyboard_prices_start)

		# if was pressed "Текущая стоимость"
		elif call.data == "end_price_query":

			bot.edit_message_text(text='Выбери', chat_id=call.message.chat.id, message_id=call.message.message_id,

								  reply_markup=keyboard_prices_current)

		# if was pressed after "Начальная/Текущая стоимость" and after pressed an each button
		elif "from" in call.data or "to" in call.data:

			current_user.make_price(call)

		# if was pressed "Поиск по словам"
		elif call.data == "search_query_text":

			current_user.make_text_query(call)

		# if was pressed "Назад"
		elif call.data == "back_menu":

			current_user.changed = True

			make_back_from_menu(call)

		# if was pressed "Связаться"
		elif "adm" in call.data:

			keyboard_to_admin = types.InlineKeyboardMarkup(row_width=1)

			key_to_admin = types.InlineKeyboardButton(text='Агент', url="https://t.me/olegBurn2154")

			keyboard_to_admin.add(key_to_admin)

			url_number = int(call.data.split("_")[1]) - 1

			url = current_user.params.get("urls").get(url_number)

			bot.send_message(chat_id=call.message.chat.id, text="📞️", reply_markup=keyboard_to_admin)

			bot.send_message(chat_id=548919987, text=url)
			bot.send_message(chat_id=548919987, text=current_user.params.get("username"))

		# if was pressed an each cell after pressed "Категории", "Площадки", "Регионы"
		elif call.data.split("_")[0] == "btnCategories" or call.data.split("_")[0] == "btnMarkets" \
 \
				or call.data.split("_")[0] == "btnRegions":

			additional_fp = ''

			current_name = ''

			filter_parameter = call.data.split("_")[0][3:].lower()

			if call.data.split("_")[0] == "btnRegions":

				for district in current_user.params.get("districts"):

					if int(call.data.split("_")[1]) in current_user.params.get("districts").get(district).get(

							"regions"):
						additional_fp = current_user.params.get("districts").get(district).get("regions")

						break

			if not additional_fp:

				current_params = current_user.params.get(f"{filter_parameter}")

				for k, v in current_params.items():

					if str(v[0]) == call.data.split("_")[1]:
						current_name = k

						break

				if not current_user.params.get(f"{filter_parameter}").get(current_name)[1]:

					current_user.params[f"{filter_parameter}"][current_name][1] = True

					if current_user.params[f"{filter_parameter}"][current_name][0] not in current_user.filter[

						f"{filter_parameter}"]:
						current_user.filter[f"{filter_parameter}"].append(

							current_user.params[f"{filter_parameter}"][current_name][0])

					current_user.make_menu(call)

				else:

					current_user.params[f"{filter_parameter}"][current_name][1] = False

					if current_user.params[f"{filter_parameter}"][current_name][0] in current_user.filter[

						f"{filter_parameter}"]:
						current_user.filter[f"{filter_parameter}"].remove(

							current_user.params[f"{filter_parameter}"][current_name][0])

					current_user.make_menu(call)

			else:

				current_params = current_user.params.get("regions")

				for k, v in current_params.items():

					if str(v[0]) == call.data.split("_")[1] and int(v[0]) in additional_fp:
						current_name = k

						break

				if not current_user.params.get("regions").get(current_name)[1]:

					current_user.params["regions"][current_name][1] = True

					if current_user.params["regions"][current_name][0] not in current_user.filter["regions"]:
						current_user.filter["regions"].append(current_user.params["regions"][current_name][0])

					current_user.make_menu_from_districts(call)

				else:

					current_user.params["regions"][current_name][1] = False

					if current_user.params["regions"][current_name][0] in current_user.filter["regions"]:
						current_user.filter["regions"].remove(current_user.params["regions"][current_name][0])

					current_user.make_menu_from_districts(call)
	else:
		bot.send_message(chat_id=call.message.chat.id, text='Введите /start')

	# update all current user's data
	user_data[call.message.chat.id] = current_user






bot.polling(none_stop=True)

# 196556991
