import telebot
from telebot import types
import json

bot = telebot.TeleBot('1205043047:AAEhXjkWNG6UdE1zaa6YPuDJaKwe5ni0_50')

keyboard_menu = types.InlineKeyboardMarkup(row_width=2)
key_markets = types.InlineKeyboardButton(text='Площадки', callback_data='markets_query')
key_category = types.InlineKeyboardButton(text='Категории', callback_data='categories_query')
key_regions = types.InlineKeyboardButton(text='Регионы', callback_data='regions_query')
key_start_price = types.InlineKeyboardButton(text='Начальная стоимость', callback_data='start_price_query')
key_end_price = types.InlineKeyboardButton(text='Конечная стоимость', callback_data='end_price_query')
key_search = types.InlineKeyboardButton(text='Найти лоты', callback_data='search_query')
key_text = types.InlineKeyboardButton(text='Поиск по словам', callback_data='search_query_text')
keyboard_menu.add(key_start_price, key_end_price, key_markets, key_regions, key_category, key_text)
keyboard_menu.add(key_search)

with open("template_params.json", 'r') as file:
    template_params = json.load(file) 

user_data = {}

class User:

    def __init__(self):
        self.params = template_params
        self.changed = False
        self.webWorker = ''

    def make_menu(self, call):
        keys_lst = []
        filter_parameter = call.data.split("_")[0]
        row_width = 2

        if call.data == "markets_query":
            row_width = 1

        keyboard_category = types.InlineKeyboardMarkup(row_width=row_width)

        for item in self.params.get(filter_parameter):
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
        keyboard_category.add(*keys_lst)
        bot.edit_message_text(text='Выбери параметр', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard_category)


    def make_back_from_menu(self, call): 
        alert_text = f"Вы настроили {call.message.text.split()[1]}!" 
        bot.answer_callback_query(call.id, show_alert=True, text=alert_text)
        bot.edit_message_text(text="Настрой фильтр", chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=keyboard_menu)

    def accepted(self, message):
        message = bot.send_message(chat_id=message.chat.id, text='Принято')
        bot.edit_message_text(text="Что-то еще настроим?", chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard_menu)

    
    def get_price(self, message):
        if message.text.isdigit():
            self.accepted(self, message)
        else:
            message = bot.send_message(chat_id=message.chat.id, text='Не принято')
            bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                                  message_id=message.message_id,
                                  reply_markup=keyboard_menu)

    def make_price(self, call, start_price=True):
        if start_price:
            message = bot.edit_message_text(text="Введи стартовую стоимость", chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
             message = bot.edit_message_text(text="Введи конечную стоимость", chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.register_next_step_handler(message, self.get_price)

    def make_text_query(self, call):
        message = bot.edit_message_text(text="Введи поисковой запрос", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(message, self.accepted)

@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.from_user.id, text="Добро пожаловать в Торги по банкротству РФ!")
    bot.send_message(message.from_user.id, text="Давай настроим фильтр?", reply_markup=keyboard_menu)
              
    user_data[message.chat.id] = User()

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    current_user = user_data.get(call.message.chat.id)
    if current_user:      
        if call.data == "regions_query" or call.data == "markets_query" or call.data == "categories_query":
            current_user.make_menu(call)    
        elif call.data == "start_price_query":
            current_user.make_price(call)
        elif call.data == "end_price_query":
            current_user.make_price(call, False)   
        elif call.data == "search_query":
            bot.answer_callback_query(call.id, show_alert=True, text="В разработке!")
        elif call.data == "search_query_text":
            current_user.make_text_query(call)  
        elif call.data == "back_menu":
            current_user.make_back_from_menu(call)
        elif call.data.split("_")[0] == "btnCategories" or call.data.split("_")[0] == "btnRegions" or call.data.split("_")[0] == "btnMarkets":
            current_name = ''
            filter_parameter = call.data.split("_")[0][3:].lower()
            current_params = user_data.get(current_user.params).get(f"{filter_parameter}")
            for k, v in current_params.items():
                if str(v[0]) == call.data.split("_")[1]:
                    current_name = k
                    break
            if not user_data.get(current_user.params).get(f"{filter_parameter}").get(current_name)[1]:
                user_data[current_user.params][f"{filter_parameter}"][current_name][1] = True
                current_user.make_menu(call)
            else:
                user_data[current_user.params][f"{filter_parameter}"][current_name][1] = False
                current_user.make_menu(call)    
    else:
        bot.send_message(chat_id=call.message.chat.id, text='Введите /start')
    
    print(user_data, '\n')   


bot.polling(none_stop=True, interval=0)

