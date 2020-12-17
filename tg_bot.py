import sys, os
import json
import time
import telebot
from dotenv import load_dotenv
from loguru import logger
from telebot import types
from telebot.types import InputMediaPhoto


# settings for logging
logger.add("debug.log", format="{time}  {message}", level="DEBUG", rotation="500 MB", compression="zip", encoding='utf-8')

# include .env file
load_dotenv()
# now we can import from ./parser dir
sys.path.append('parser/')
from web_worker import *

# load telegram API key fron .env
bot = telebot.TeleBot(os.getenv("MY_KEY"))

# all user's data using the TG-bot
user_data = {}

# admin_chat_id
# ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_ID = os.getenv("MY_TG_ID")

# create base menu keyboard
keyboard_menu = types.InlineKeyboardMarkup(row_width=2)
key_category = types.InlineKeyboardButton(text='📝Категории', callback_data='categories_query')
key_regions = types.InlineKeyboardButton(text=f'🌍Регионы', callback_data='districts_query')
key_section = types.InlineKeyboardButton(text=f'⚙️Секции', callback_data='sections_query')
key_start_price = types.InlineKeyboardButton(text='💲Начальная стоимость', callback_data='start_price_query')
key_end_price = types.InlineKeyboardButton(text='💲Текущая стоимость', callback_data='end_price_query')
key_search = types.InlineKeyboardButton(text=f'🔍Найти лоты', callback_data='search')
key_text = types.InlineKeyboardButton(text='🔤Поиск по словам', callback_data='search_query_text')
keyboard_menu.add(key_start_price, key_end_price, key_regions, key_category, key_section, key_text)
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

keyboard_lots = types.InlineKeyboardMarkup(row_width=1)
key_long_descrip = types.InlineKeyboardButton(text="⏬Подробнее")
key_search_2 = types.InlineKeyboardButton(text='⬇️Загрузить еще', callback_data='search')
keyboard_lots.add(key_search_2)

clear_filters = types.InlineKeyboardButton(text=f'❌Очистить фильтр', callback_data='clear_filter')
keyboard_menu.add(clear_filters)

keyboard_section = types.InlineKeyboardMarkup(row_width=1)
key_1 = types.InlineKeyboardButton(text="Все секции", callback_data="sectionbtn_1")
key_2 = types.InlineKeyboardButton(text="Банкротство", callback_data="sectionbtn_2")
key_3 = types.InlineKeyboardButton(text="Арестованное им.", callback_data="sectionbtn_3")
key_4 = types.InlineKeyboardButton(text="Залоговое им.", callback_data="sectionbtn_4")
key_5 = types.InlineKeyboardButton(text="Непрофильные активы", callback_data="sectionbtn_5")
key_6 = types.InlineKeyboardButton(text="Коммерческие торги", callback_data="sectionbtn_6")
key_7 = types.InlineKeyboardButton(text="Гос. и мун. торги", callback_data="sectionbtn_7")
key_8 = types.InlineKeyboardButton(text="Прямая продажа/лизинг", callback_data="sectionbtn_8")
keyboard_section.add(key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8)


# function for loading of lot's info
def print_lot(lot, chat_id):
    """send lot info to user"""
    # check errors
    if not isinstance(lot, dict):
        return None

    flag = lot.get("cost").get("flag")
    if flag == "up":
        flag = "🟢🔺"
    elif flag == "down":
        flag = "🔴🔻"
    elif flag == "commercial":
        flag = "🟠"

    # make message text
    full_description_short = lot.get('description').get('full')[:200] + "..."
    full_description_long = lot.get('description').get('full')[:1200] + "..."

    msg_short = flag + f"<strong> {lot['cost']['current']}, {lot['description']['title']}</strong> " + '\n\n' + f"Место осмотра: {lot.get('region')}" + '\n\n' + \
                f"{lot['bidding_type']}" + '\n\n' f"{full_description_short}" + '\n\n'

    # two message for button "Подробнее" (one of it can be empty)
    msg_short_for_msg_long = flag + f"<strong> {lot['cost']['current']}₽, {lot['description']['title']}</strong> " + '\n\n' + f"Место осмотра: {lot['region']}" + \
                             f"{lot['bidding_type']}" + '\n\n' \
                                                        f"{full_description_long}" + '\n\n'

    msg_long = f"Дата проведения торгов: {lot['date']['bidding']}" + '\n\n' \
                                                                     f"Дата начала представления заявок на участие: {lot['date']['start_bid']}" + '\n\n' \
                                                                                                                                                  f"Дата окончания представления заявок на участие: {lot['date']['end_bid']}" + '\n\n' \
                                                                                                                                                                                                                                f"Начальная цена, руб.: {lot['cost']['current']}" + '\n\n' \
                                                                                                                                                                                                                                                                                    f"Шаг цены: {lot['cost']['step']}"
    # make album with photo
    media = [InputMediaPhoto(i) for i in lot["pictures"] if lot["pictures"]]
    if media:
        bot.send_media_group(chat_id=chat_id, media=media[:5])

    """contact button"""
    keyboard_contacts = types.InlineKeyboardMarkup()
    user_data[chat_id].params["urls"][user_data.get(chat_id).counter] = lot.get("marketplace").get("url")
    user_data[chat_id].params["description_long"][user_data.get(chat_id).counter] = msg_short_for_msg_long + msg_long
    user_data[chat_id].counter += 1
    key_to_buy = types.InlineKeyboardButton(text='📞Связаться', callback_data=f"adm_{user_data.get(chat_id).counter}")
    key_descr = types.InlineKeyboardButton(text='⏬Подробнее', callback_data=f"descr_{user_data.get(chat_id).counter}")
    keyboard_contacts.add(key_to_buy, key_descr)
    time.sleep(1)
    bot.send_message(chat_id=chat_id, text=msg_short, reply_markup=keyboard_contacts, parse_mode="html")


# function of a button "Применить" from menu
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
            self.filter["start price"]["from"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_start)

    def get_price_start_to(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["start price"]["to"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_start)

    def get_price_current_from(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["current price"]["from"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_current)

    def get_price_current_to(self, message):
        if message.text.isdigit():
            accepted(message)
            self.filter["current price"]["to"] = message.text
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_prices_current)

    def get_text_query(self, message):
        self.filter["search text"] = message.text
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
        key_accept = types.InlineKeyboardButton(text="👌Применить", callback_data='back_menu')
        keys_lst = []
        keyboard_filter_params = types.InlineKeyboardMarkup(row_width=2)
        keyboard_filter_params.add(key_accept)

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
        keyboard_filter_params.add(*keys_lst)
        bot.edit_message_text(text='Выбери параметр', chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_filter_params)

    def make_section(self, call):
        message = bot.edit_message_text(text="Выберите параметр", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=keyboard_section)

    def make_menu(self, call):
        key_accept = types.InlineKeyboardButton(text="👌Применить", callback_data='back_menu')
        keys_lst = []
        filter_parameter = call.data.split("_")[0]

        if "btn" in filter_parameter:
            filter_parameter = filter_parameter[3:].lower()
        row_width = 2

        if call.data == "btnMarkets" in call.data:
            row_width = 1

        keyboard_filter_params = types.InlineKeyboardMarkup(row_width=2)
        keyboard_filter_params.add(key_accept)

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
        keyboard_filter_params.add(*keys_lst)
        bot.edit_message_text(text='Выбери параметр', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=keyboard_filter_params)


@bot.message_handler(commands=['start'])
def get_start(message):
    """start message handler"""
    bot.send_photo(chat_id=message.from_user.id, photo="https://torgi-blog.com/wp-content/uploads/2018/09/1748-01.png",
                   caption="https://torgi.gov.ru/index.html")
    bot.send_message(message.from_user.id, text="Добро пожаловать в Торги по банкротству РФ!",
                     reply_markup=keyboard_menu)
    user_data[message.chat.id] = User()

    username = message.from_user.username
    if not username:
        first_name = message.from_user.first_name
        if not first_name:
            first_name = ""
        last_name = message.from_user.last_name
        if not last_name:
            last_name = ""
        username = first_name + " " + last_name

    user_data[message.chat.id].params["username"] = username
    logger.debug(f"New user: {message.chat.id} - {username}")


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    current_user = user_data.get(call.message.chat.id)

    # if user has pressed start (checking)
    if current_user:
        # if was pressed "Найти лоты"
        if call.data == "search":
            # try:
            # Making a filter for webWorker by checking all pressed regions on tg-bot menu keyboard
            for district in current_user.params.get("districts"):
                for region in current_user.params.get("districts").get(district).get("regions"):
                    if str(region) in current_user.filter.get("regions"):
                        if current_user.params.get("districts").get(district).get("code") not in \
                                current_user.filter["districts"]:
                            current_user.filter["districts"].append(
                                current_user.params.get("districts").get(district).get("code"))
                            continue

            if current_user.changed or current_user.web_worker == "":
                current_user.web_worker = WebWorker(filter_params=current_user.filter)
                current_user.changed = False

            if current_user.web_worker._lots_info:
                parsed_lots = current_user.web_worker.get_lots_info()
                try:
                    for i in parsed_lots:
                        print_lot(i, call.message.chat.id)
                except IndexError:
                    bot.send_message(call.message.chat.id, text="Кажется, лоты закончились :(")

                # load menu keyboard
                bot.send_message(call.message.chat.id, text="Еще немного лотов?", reply_markup=keyboard_lots)
                bot.send_message(call.message.chat.id, text="Изменить параметры фильтра?",
                                 reply_markup=keyboard_menu)
            else:
                bot.send_message(call.message.chat.id, text="Кажется, лоты закончились :(")

            logger.debug(f"query url for {call.message.chat.id}-{current_user.params.get('username')}: {get_url(current_user.filter)}")
            logger.debug(f"filter for {call.message.chat.id}-{current_user.params.get('username')}: {current_user.filter}")

            # except Exception as e:
            # logger.error(f"IN SEARCH BLOCK: {e}")
            # bot.send_message(call.message.chat.id, text="Слишком много запросов...Попробуйте позже, пожалуйста",
            #                      reply_markup=keyboard_menu)

        # if was pressed "Регионы"
        elif call.data == "districts_query":
            bot.edit_message_text(text='Выбери округ', chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=keyboard_districts)

        # after was pressed "Регионы" and pressed an each appeared button
        elif "regions_query" in call.data:
            current_user.make_menu_from_districts(call)

        # if was pressed "Категории"
        elif call.data == "categories_query":
            current_user.make_menu(call)

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

        # if was pressed "Применить"
        elif call.data == "back_menu":
            current_user.changed = True
            make_back_from_menu(call)

        # if was pressed "Связаться"
        elif "adm" in call.data:
            keyboard_to_admin = types.InlineKeyboardMarkup(row_width=1)
            key_to_admin = types.InlineKeyboardButton(text='Написать', url="https://t.me/Agentbankrot")
            key_to_admin_call = types.InlineKeyboardButton(text='Позвонить', callback_data='call')
            keyboard_to_admin.add(key_to_admin)
            keyboard_to_admin.add(key_to_admin_call)

            if len(call.data.split("_")) == 2:
                url_number = int(call.data.split("_")[1]) - 1
            else:
                url_number = int(call.data.split("_")[1])
            url = current_user.params.get("urls").get(url_number)

            bot.send_message(chat_id=call.message.chat.id, text="📞️", reply_markup=keyboard_to_admin)

            username = current_user.params.get("username")
            text_msg = "https://t.me/" + str(username) + " : " + str(url)

            bot.send_message(chat_id=ADMIN_ID, text="Интересуется пользователь: " + text_msg)
            logger.debug(f"Сообщение ADMIN: " + text_msg)

        # if was pressed "Позвонить"
        elif call.data == "call":
            bot.send_message(chat_id=call.message.chat.id, text="[+79523972045](tel:+79523972045)",
                             parse_mode='Markdown')

        # if was pressed "Очистить фильтр"
        elif call.data == "clear_filter":
            current_user.changed = True
            with open("template_params.json", 'r', encoding='utf-8') as file:
                current_user.params = json.load(file)
            with open("filter_template.json", 'r', encoding='utf-8') as file2:
                current_user.filter = json.load(file2)

            bot.answer_callback_query(call.id, show_alert=True, text="Вы очистили фильтр!")

        # if wass pressed "Подробнее"
        elif "descr" in call.data:
            url_number = int(call.data.split("_")[1]) - 1
            long_descr = current_user.params.get("description_long").get(url_number)
            keyboard_contacts = types.InlineKeyboardMarkup(row_width=1)
            key_to_buy = types.InlineKeyboardButton(text='📞Связаться',
                                                    callback_data=f"adm_{url_number}_desc")
            keyboard_contacts.add(key_to_buy)

            time.sleep(1)
            bot.send_message(chat_id=call.message.chat.id, text=long_descr, parse_mode='html',
                             reply_markup=keyboard_contacts)
            bot.send_message(call.message.chat.id, text="Изменить параметры фильтра?",
                             reply_markup=keyboard_menu)

        elif call.data == "sections_query":
            current_user.make_section(call)
        # if was pressed an each item on section keyboard
        elif "sectionbtn" in call.data:
            number_of_button = int(call.data.split("_")[1])
            choose_section = ""
            if number_of_button == 2:
                choose_section = "bankrupt"
            elif number_of_button == 3:
                choose_section = "arrest"
            elif number_of_button == 4:
                choose_section = "zalog"
            elif number_of_button == 5:
                choose_section = "non-core"
            elif number_of_button == 6:
                choose_section = "commercial"
            elif number_of_button == 7:
                choose_section = "privatization"
            elif number_of_button == 8:
                choose_section = "confiscate"

            current_user.filter["section"] = choose_section
            current_user.changed = True
            make_back_from_menu(call)

        # if was pressed an each cell after pressed "Категории", "Площадки", "Регионы"
        elif call.data.split("_")[0] == "btnCategories" or \
                call.data.split("_")[0] == "btnMarkets" or \
                call.data.split("_")[0] == "btnRegions":

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


@logger.catch
def main():
    bot.polling(none_stop=True, interval=1)



try:
    main()
except requests.exceptions.ConnectionError:
    pass
except urllib3.exceptions.MaxRetryError:
    pass
except socket.timeout:
    pass
except urllib3.exceptions.ReadTimeoutError:
    pass
except requests.exceptions.ReadTimeout:
    pass
except OSError:
    pass
except urllib3.exceptions.NewConnectionError:
    pass

while True:
    pass