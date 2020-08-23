import telebot
from telebot import types
import json

bot = telebot.TeleBot('1205043047:AAEhXjkWNG6UdE1zaa6YPuDJaKwe5ni0_50')

keyboard_menu = types.InlineKeyboardMarkup(row_width=2)
key_markets = types.InlineKeyboardButton(text='Площадки', callback_data='markets_query')
key_category = types.InlineKeyboardButton(text='Категории', callback_data='categories_query')
key_regions = types.InlineKeyboardButton(text='Регионы', callback_data='districts_query')
key_start_price = types.InlineKeyboardButton(text='Начальная стоимость', callback_data='start_price_query')
key_end_price = types.InlineKeyboardButton(text='Конечная стоимость', callback_data='end_price_query')
key_search = types.InlineKeyboardButton(text='Найти лоты', callback_data='search_query')
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

user_data = {}


def make_back_from_menu(call):
    alert_text = f"Вы настроили {call.message.text.split()[1]}!"
    bot.answer_callback_query(call.id, show_alert=True, text=alert_text)
    bot.edit_message_text(text="Настрой фильтр", chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard_menu)


def accepted(message):
    message = bot.send_message(chat_id=message.chat.id, text='Принято')
    bot.edit_message_text(text="Что-то еще настроим?", chat_id=message.chat.id, message_id=message.message_id,
                          reply_markup=keyboard_menu)


def get_price(message):
    if message.text.isdigit():
        accepted(message)
    else:
        message = bot.send_message(chat_id=message.chat.id, text='Не принято')
        bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                              message_id=message.message_id,
                              reply_markup=keyboard_menu)


def make_price(call, start_price=True):
    if start_price:
        message = bot.edit_message_text(text="Введи стартовую стоимость", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
    else:
        message = bot.edit_message_text(text="Введи конечную стоимость", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)

    bot.register_next_step_handler(message, get_price)


def make_text_query(call):
    message = bot.edit_message_text(text="Введи поисковой запрос", chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)
    bot.register_next_step_handler(message, accepted)


class User:

    def __init__(self):
        with open("template_params.json", 'r') as file:
            template_params = json.load(file)
        self.params = template_params.copy()
        self.changed = False
        self.webWorker = ''

    def make_menu_from_districts(self, call):
        keys_lst = []
        keyboard_filter_params = types.InlineKeyboardMarkup(row_width=2)

        for district in self.params.get("districts"):
            if self.params.get("districts").get(district).get("code") == call.data.split("_")[2]:
                selected_regions = self.params.get("districts").get(district).get("regions")
                break

        for region in self.params.get("regions"):
            if int(self.params.get("regions").get(region)[0]) in selected_regions:
                key = types.InlineKeyboardButton(text=region,
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
    bot.send_message(message.from_user.id, text="Добро пожаловать в Торги по банкротству РФ!")
    bot.send_message(message.from_user.id, text="Давай настроим фильтр?", reply_markup=keyboard_menu)

    user_data[message.chat.id] = User()
    # print("THE BEGIN: ", user_data[message.chat.id].params, "\n\n")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    current_user = user_data.get(call.message.chat.id)
    if current_user:
        if call.data == "markets_query" or call.data == "categories_query":
            current_user.make_menu(call)
        elif call.data == "districts_query":
            bot.edit_message_text(text='Выбери округ', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard_districts)
        elif "regions_query" in call.data:
            current_user.make_menu_from_districts(call)
        elif call.data == "start_price_query":
            make_price(call)
        elif call.data == "end_price_query":
            make_price(call, False)
        elif call.data == "search_query":
            bot.answer_callback_query(call.id, show_alert=True, text="В разработке!")
        elif call.data == "search_query_text":
            make_text_query(call)
        elif call.data == "back_menu":
            make_back_from_menu(call)
        elif call.data.split("_")[0] == "btnCategories" or call.data.split("_")[0] == "btnMarkets" \
            or call.data.split("_")[0] == "btnRegions":
            current_name = ''
            filter_parameter = call.data.split("_")[0][3:].lower()
            if call.data.split("_")[0] == "btnRegions":
                for district in current_user.params.get("districts"):
                    if call.data.split("_")[2] in current_user.params.get("districts").get(district).get("regions"):
                        additional_fp =
                        break

            current_params = current_user.params.get(f"{filter_parameter}")
            for k, v in current_params.items():
                if str(v[0]) == call.data.split("_")[1]:
                    current_name = k
                    break
            if not current_user.params.get(f"{filter_parameter}").get(current_name)[1]:
                current_user.params[f"{filter_parameter}"][current_name][1] = True
                current_user.make_menu(call)
            else:
                current_user.params[f"{filter_parameter}"][current_name][1] = False
                current_user.make_menu(call)

    else:
        bot.send_message(chat_id=call.message.chat.id, text='Введите /start')

    user_data[call.message.chat.id] = current_user


bot.polling(none_stop=True, interval=0)
