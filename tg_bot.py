import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import time

from tg_post import *

import sys, os
from dotenv import load_dotenv
load_dotenv(".env")
sys.path.append('parser/')
from web_worker import *


bot = telebot.TeleBot(os.getenv("BOT_KEY"))

keyboard_menu = types.InlineKeyboardMarkup(row_width=2)
key_markets = types.InlineKeyboardButton(text='Площадки', callback_data='markets_query')
key_category = types.InlineKeyboardButton(text='Категории', callback_data='categories_query')
key_regions = types.InlineKeyboardButton(text='Регионы', callback_data='districts_query')
key_start_price = types.InlineKeyboardButton(text='Начальная стоимость', callback_data='start_price_query')
key_end_price = types.InlineKeyboardButton(text='Текущая стоимость', callback_data='end_price_query')
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

keyboard_prices_start = types.InlineKeyboardMarkup(row_width=2)
key_1 = types.InlineKeyboardButton(text='Стартовая цена (от)', callback_data='start_query_from')
key_2 = types.InlineKeyboardButton(text='Стартовая цена (до)', callback_data='start_query_to')
keyboard_prices_start.add(key_1, key_2)

keyboard_prices_current = types.InlineKeyboardMarkup(row_width=2)
key_1 = types.InlineKeyboardButton(text='Текущая цена (от)', callback_data='current_query_from')
key_2 = types.InlineKeyboardButton(text='Текущая цена (до)', callback_data='current_query_to')
keyboard_prices_current.add(key_1, key_2)

user_data = {}


def like_telegraph(lot, id):
    try:
        picture = lot["pictures"]
    except Exception as e:
        picture = ""

    full_description = lot['description']['full']
    if len(full_description) > 2817:
        full_description = ""

    msg = f"<strong>Цена - {lot['cost']['current']}, {lot['description']['title']}</strong>" + '\n\n'\
    f"{lot['bidding_type']}" + '\n\n'\
    f"{full_description}" + '\n\n' \
    f"Место осмотра: {lot['region']}" + '\n\n'\
    f"Дата проведения торгов: {lot['date']['bidding']}" + '\n\n'\
    f"Дата начала представления заявок на участие: {lot['date']['start_bid']}" + '\n\n'\
    f"Дата окончания представления заявок на участие: {lot['date']['end_bid']}" + '\n\n'\
    f"Начальная цена, руб.: {lot['cost']['current']}" + '\n\n'\
    f"Шаг цены: {lot['cost']['step']}"

    media = [InputMediaPhoto(i) for i in picture]
    if media:
        bot.send_media_group(chat_id=id, media=media[:5])
    return msg


def draw(lots_info_list, id):
    keyboard_search = types.InlineKeyboardMarkup(row_width=1)
    key_find = types.InlineKeyboardButton(text='Да', callback_data='search_query')
    keyboard_search.add(key_find)

    for i in lots_info_list:
        bot.send_message(chat_id=id, text=like_telegraph(i, id), parse_mode='html')
        msg = bot.send_message(chat_id=id, text="Контакты")

        keyboard_contacts = types.InlineKeyboardMarkup(row_width=2)
        key_to_buy = types.InlineKeyboardButton(text='Задать вопрос или купить', callback_data="adm")
        keyboard_contacts.add(key_to_buy)

        bot.edit_message_text(text='Контакты', chat_id=id, message_id=msg.message_id,
                              reply_markup=keyboard_contacts)
    if lots_info_list:
        msg = bot.send_message(chat_id=id, text="Загрузить еще лоты")
        bot.edit_message_text(text='Загрузить еще лоты?', chat_id=id, message_id=msg.message_id, reply_markup=keyboard_search)
        time.sleep(1)
    else:
        time.sleep(2)
        bot.send_message(chat_id=id, text="Все лоты по фильтру загружены!🎈")
        bot.send_message(id, text="Настройте новый фильтр", reply_markup=keyboard_menu)


def make_back_from_menu(call):
    alert_text = f"Вы настроили {call.message.text.split()[1]}!"
    bot.answer_callback_query(call.id, show_alert=True, text=alert_text)
    bot.edit_message_text(text="Настрой фильтр", chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard_menu)


def accepted(message):
    message = bot.send_message(chat_id=message.chat.id, text='Принято')
    bot.edit_message_text(text="Что-то еще настроим?", chat_id=message.chat.id, message_id=message.message_id,
                          reply_markup=keyboard_menu)


class User:

    def __init__(self):
        with open("template_params.json", 'r', encoding='utf-8') as file:
            template_params = json.load(file)
        with open("filter_template2.json", 'r', encoding='utf-8') as file2:
            filter_params = json.load(file2)
        self.params = template_params.copy()
        self.filter = filter_params.copy()
        self.changed = False
        self.webWorker = ""

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
    bot.send_message(message.from_user.id, text="Добро пожаловать в Торги по банкротству РФ!")
    bot.send_message(message.from_user.id, text="Давай настроим фильтр?", reply_markup=keyboard_menu)

    user_data[message.chat.id] = User()
    # print("THE BEGIN: ", user_data[message.chat.id].params, "\n\n")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    current_user = user_data.get(call.message.chat.id)
    print(call.message.chat.id)
    print(call.data)
    if current_user:
        if call.data == "markets_query" or call.data == "categories_query":
            current_user.make_menu(call)

        elif call.data == "districts_query":
            bot.edit_message_text(text='Выбери округ', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard_districts)

        elif "regions_query" in call.data:
            current_user.make_menu_from_districts(call)

        elif call.data == "start_price_query":
            bot.edit_message_text(text='Выбери', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard_prices_start)

        elif call.data == "end_price_query":
            bot.edit_message_text(text='Выбери', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard_prices_current)

        elif "from" in call.data or "to" in call.data:
            current_user.make_price(call)

        elif call.data == "search_query":
            for district in current_user.params.get("districts"):
                for region in current_user.params.get("districts").get(district).get("regions"):
                    if str(region) in current_user.filter.get("regions"):
                        if current_user.params.get("districts").get(district).get("code") not in current_user.filter["districts"]:
                            current_user.filter["districts"].append(
                                current_user.params.get("districts").get(district).get("code"))
                            continue

            if current_user.changed or current_user.webWorker == "":
                current_user.webWorker = WebWorker(current_user.filter)
                current_user.changed = False
            drawn = current_user.webWorker.get_lots_info(draw)
            drawn(id = call.message.chat.id)

        elif call.data == "search_query_text":
            current_user.make_text_query(call)

        elif call.data == "back_menu":
            current_user.changed = True
            make_back_from_menu(call)

        elif call.data == "adm":
            keyboard_to_admin = types.InlineKeyboardMarkup(row_width=1)
            key_to_admin = types.InlineKeyboardButton(text='Задать вопрос или купить', url="https://t.me/olegBurn2154")
            keyboard_to_admin.add(key_to_admin)
            url = call.data.split("_")[1]
            bot.send_message(chat_id=call.message.chat.id, text="Открыть чат с продавцом", reply_markup=keyboard_to_admin)
            bot.send_message(chat_id=695410130, text=url)

        elif call.data.split("_")[0] == "btnCategories" or call.data.split("_")[0] == "btnMarkets" \
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

    user_data[call.message.chat.id] = current_user


bot.polling(none_stop=True, interval=0)
