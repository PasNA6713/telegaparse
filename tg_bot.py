import telebot
from telebot import types

bot = telebot.TeleBot('1225070960:AAEST2WsWFmScFepQBA6mOh-4cDQVQVoEE4')
flags = {
    'categories': {
        'Легковой транспорт': [0, False]
        , 'Грузовой и комм. транспорт': [1, False]
        , 'Спецтехника': [2, False]
        , 'Прочий транспорт': [3, False]
        , 'Автобусы, микроавтобусы': [4, False]
        , 'Авиатранспорт': [5, False]
        , 'Водный транспорт': [6, False]
        , 'Жилая недвижимость': [7, False]
        , 'Комм. недвижимость': [8, False]
        , 'Земельные участки': [9, False]
        , 'Гаражи, строения, сооружения': [10, False]
        , 'Задолженность физ. лиц': [11, False]
        , 'Задолженность юр. лиц': [12, False]
        , 'Смешанная задолженность': [13, False]
        , 'С/х здания и соружения': [14, False]
        , 'Животные и скот': [15, False]
        , 'С/х комплекс': [16, False]
        , 'С/х техника': [17, False]
        , 'С/х оборудование': [18, False]
        , 'Пром. оборудование': [19, False]
        , 'Деревообработка': [20, False]
        , 'Металлообработка': [21, False]
        , 'Пищевое оборудование': [22, False]
        , 'Складское и торг. оборуд.': [23, False]
        , 'Строительное оборудование': [24, False]
        , 'Другое оборудование': [25, False]
        , 'Мебель': [26, False]
        , 'Оргтехника': [27, False]
        , 'Бытовая техника': [28, False]
        , 'Драгоценные металлы, драг. камни и изделия из них': [29, False]
    }
    , 'regions': {
        'Белгородская область': [0, False]
        , 'Брянская область': [1, False]
        , 'Владимирская область': [2, False]
        , 'Воронежская область': [3, False]
        , 'Ивановская область': [4, False]
        , 'Калужская область': [5, False]
        , 'Костромская область': [6, False]
        , 'Курская область': [7, False]
        , 'Липецкая область': [8, False]
        , 'Московская область': [9, False]
        , 'Орловская область': [10, False]
        , 'Рязанская область': [11, False]
        , 'Смоленская область': [12, False]
        , 'Тамбовская область': [13, False]
        , 'Тверская область': [14, False]
        , 'Тульская область': [15, False]
        , 'Ярославская область': [16, False]
        , 'г. Москва': [17, False]
        , 'Республика Карелия': [18, False]
        , 'Республика Коми': [19, False]
        , 'Архангельская область': [20, False]
        , 'Вологодская область': [21, False]
        , 'Калининградская область': [22, False]
        , 'Ленинградская область': [23, False]
        , 'Мурманская область': [24, False]
        , 'Новгородская область': [25, False]
        , 'Псковская область': [26, False]
        , 'г. Санкт-Петербург': [27, False]
        , 'Ненецкий автономный округ': [28, False]
        , 'Республика Адыгея': [29, False]
        , 'Республика Калмыкия': [30, False]
        , 'Краснодарский край': [31, False]
        , 'Астраханская область': [32, False]
        , 'Волгоградская область': [33, False]
        , 'Ростовская область': [34, False]
        , 'Республика Крым': [35, False]
        , 'г. Севастополь': [36, False]
        , 'Республика Дагестан': [37, False]
        , 'Республика Ингушетия': [38, False]
        , 'Кабардино-Балкарская Республика': [39, False]
        , 'Карачаево-Черкесская Республика': [40, False]
        , 'Республика Северная Осетия - Алания': [41, False]
        , 'Чеченская Республика': [42, False]
        , 'Ставропольский край': [43, False]
        , 'Республика Башкортостан': [44, False]
        , 'Республика Марий Эл': [45, False]
        , 'Республика Мордовия': [46, False]
        , 'Республика Татарстан': [47, False]
        , 'Удмуртская Республика': [48, False]
        , 'Чувашская Республика - Чувашия': [49, False]
        , 'Кировская область': [50, False]
        , 'Нижегородская область': [51, False]
        , 'Оренбургская область': [52, False]
        , 'Пензенская область': [53, False]
        , 'Пермский край': [54, False]
        , 'Самарская область': [55, False]
        , 'Саратовская область': [56, False]
        , 'Ульяновская область': [57, False]
        , 'Курганская область': [58, False]
        , 'Свердловская область': [59, False]
        , 'Тюменская область': [60, False]
        , 'Челябинская область': [61, False]
        , 'Ханты-Мансийский автономный округ - Югра': [62, False]
        , 'Ямало-Ненецкий автономный округ': [63, False]
        , 'Республика Бурятия': [64, False]
        , 'Республика Алтай': [65, False]
        , 'Республика Тыва': [66, False]
        , 'Республика Хакасия': [67, False]
        , 'Алтайский край': [68, False]
        , 'Красноярский край': [69, False]
        , 'Иркутская область': [70, False]
        , 'Кемеровская область': [71, False]
        , 'Новосибирская область': [72, False]
        , 'Омская область': [73, False]
        , 'Томская область': [74, False]
        , 'Забайкальский край': [75, False]
        , 'Республика Саха (Якутия)': [76, False]
        , 'Приморский край': [77, False]
        , 'Хабаровский край': [78, False]
        , 'Амурская область': [79, False]
        , 'Камчатский край': [80, False]
        , 'Магаданская область': [81, False]
        , 'Сахалинская область': [82, False]
        , 'Еврейская автономная область': [83, False]
        , 'Чукотский автономный округ': [84, False]
    }
    , "markets": {
        'Всероссийская Электронная Торговая Площадка': [0, False]
        , 'Аукцион-центр': [1, False]
        , 'Центр реализации': [2, False]
        , 'Электронная торговая площадка портала Торги России': [3, False]
        , 'uTender': [4, False]
        , 'Центр дистанционных торгов': [5, False]
        , 'Сбербанк-АСТ': [6, False]
        , 'Новые информационные сервисы': [7, False]
        , 'Россия онлайн': [8, False]
        , 'Фабрикант': [9, False]
        , 'Межрегиональная электронная торговая система': [10, False]
        , 'B2B-Center': [11, False]
        , 'KARTOTEKA.RU': [12, False]
        , 'Аукционы Дальнего Востока': [13, False]
        , 'ПТП-Центр': [14, False]
        , 'Аукционы Сибири': [15, False]
        , 'Аукционный тендерный центр': [16, False]
        , 'Система электронных торгов и муниципальных аукционов "ВТБ-Центр"': [17, False]
        , 'АКОСТА info': [18, False]
        , 'Профит': [19, False]
        , 'Региональная Торговая площадка': [20, False]
        , 'Система Электронных Торгов Имуществом': [21, False]
        , 'Электронная торговая площадка ELECTRO-TORGI.RU': [22, False]
        , 'ЭТП "Пром-Консалтинг"': [23, False]
        , 'Property Trade': [24, False]
        , 'ТЕНДЕР ГАРАНТ': [25, False]
        , 'Электронная площадка «Вердиктъ»': [26, False]
        , 'МЕТА-ИНВЕСТ': [27, False]
        , 'Электронная торговая площадка "Регион"': [28, False]
        , 'Арбитат': [29, False]
        , 'Балтийская электронная площадка': [30, False]
        , 'Объединенная Торговая Площадка': [31, False]
        , 'ООО «Специализированная организация по проведению торгов – Южная Электронная Торговая Площадка»': [32, False]
        , 'Электронная торговая площадка Заказ РФ': [33, False]
        , 'Банкротство РТ': [34, False]
        , 'UralBidIn': [35, False]
        , 'Российский аукционный дом': [36, False]
        , 'Альфалот': [37, False]
        , 'Единая торговая электронная площадка': [38, False]
        , 'Уральская электронная торговая площадка': [39, False]
        , 'ЭТП "ЮГРА"': [40, False]
        , 'Электронная площадка ЭСП': [41, False]
        , 'Открытая торговая площадка': [42, False]
        , 'Электронная торговая площадка "Евразийская торговая площадка"': [43, False]
        , 'Ru-Trade24': [44, False]
        , 'АИСТ': [45, False]
        , 'Сибирская торговая площадка': [46, False]
        , 'Системы Электронных Торгов': [47, False]
        , 'ТендерСтандарт': [48, False]
        , 'Систематорг': [49, False]
    }
    , 'in_menu_pressed': {
        'Категории': False
        , 'Площадки': False
        , 'Регионы': False
        , 'Начальная стоимость': False
        , 'Конечная стоимость': False
        , 'Найти лоты': False
    }
}

keyboard_menu = types.InlineKeyboardMarkup(row_width=2)
key_markets = types.InlineKeyboardButton(text='Площадки', callback_data='markets_query')
key_category = types.InlineKeyboardButton(text='Категории', callback_data='category_query')
key_regions = types.InlineKeyboardButton(text='Регионы', callback_data='regions_query')
key_start_price = types.InlineKeyboardButton(text='Начальная стоимость', callback_data='start_price_query')
key_end_price = types.InlineKeyboardButton(text='Конечная стоимость', callback_data='end_price_query')
key_search = types.InlineKeyboardButton(text='Найти лоты', callback_data='search_query')
keyboard_menu.add(key_start_price, key_end_price, key_markets, key_regions, key_category)
keyboard_menu.add(key_search)


def make_menu_categories(call):
    keys_lst = []

    keyboard_category = types.InlineKeyboardMarkup(row_width=2)

    for item in flags.get("categories"):
        if flags["categories"][item][1]:
            btn_text = f"✅{item}"
        else:
            btn_text = item
        key = types.InlineKeyboardButton(text=btn_text,
                                         callback_data=f"btnCategory_{flags.get('categories').get(item)[0]}")
        keys_lst.append(key)
    key = types.InlineKeyboardButton(text="◀️Назад", callback_data='back_menu')
    keys_lst.append(key)
    keyboard_category.add(*keys_lst)
    bot.edit_message_text(text='Выбери категории', chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard_category)


def make_menu_regions(call):
    keys_lst = []

    keyboard_regions = types.InlineKeyboardMarkup(row_width=2)

    for item in flags.get("regions"):
        if flags["regions"][item][1]:
            btn_text = f"✅{item}"
        else:
            btn_text = item
        key = types.InlineKeyboardButton(text=btn_text,
                                         callback_data=f"btnRegions_{flags.get('regions').get(item)[0]}")
        keys_lst.append(key)

    keyboard_regions.add(*keys_lst)
    key = types.InlineKeyboardButton(text="◀️Назад", callback_data='back_menu')
    keyboard_regions.add(key)
    bot.edit_message_text(text='Выбери регионы', chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard_regions)


def make_menu_markets(call):
    keys_lst = []

    keyboard_markets = types.InlineKeyboardMarkup(row_width=1)

    for item in flags.get("markets"):
        if flags["markets"][item][1]:
            btn_text = f"✅{item}"
        else:
            btn_text = item
        key = types.InlineKeyboardButton(text=btn_text,
                                         callback_data=f"btnMarkets_{flags.get('markets').get(item)[0]}")
        keys_lst.append(key)

    keyboard_markets.add(*keys_lst)
    key = types.InlineKeyboardButton(text="◀️Назад", callback_data='back_menu')
    keyboard_markets.add(key)
    bot.edit_message_text(text='Выбери площадки', chat_id=call.message.chat.id, message_id=call.message.message_id,
                          reply_markup=keyboard_markets)


def make_back_from_menu(call):
    if call.message.text == "Выбери категории":
        bot.answer_callback_query(call.id, show_alert=True, text="Вы настроили категории!")
        bot.edit_message_text(text="Давай настроим фильтр?", chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_menu)
    elif call.message.text == "Выбери регионы":
        bot.answer_callback_query(call.id, show_alert=True, text="Вы настроили регионы!")
        bot.edit_message_text(text="Давай настроим фильтр?", chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_menu)
    elif call.message.text == "Выбери площадки":
        bot.answer_callback_query(call.id, show_alert=True, text="Вы настроили площадки!")
        bot.edit_message_text(text="Давай настроим фильтр?", chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_menu)
    else:
        bot.edit_message_text(text="Давай настроим фильтр?", chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_menu)


def make_start_price(call):
    message = bot.edit_message_text(text="Введи стартовую стоимость", chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)
    bot.register_next_step_handler(message, get_price)


def make_end_price(call):
    message = bot.edit_message_text(text="Введи конечную стоимость", chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)
    bot.register_next_step_handler(message, get_price)


def get_price(message):
    if message.text.isdigit():
        message = bot.send_message(chat_id=message.chat.id, text='Принято')
        bot.edit_message_text(text="Что-то еще настроим?", chat_id=message.chat.id,
                              message_id=message.message_id,
                              reply_markup=keyboard_menu)
    else:
        message = bot.send_message(chat_id=message.chat.id, text='Не принято')
        bot.edit_message_text(text="Введена некорректная стоимость! Введите ее заново", chat_id=message.chat.id,
                              message_id=message.message_id,
                              reply_markup=keyboard_menu)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global keyboard_menu

    if call.data == "markets_query":
        make_menu_markets(call)

    elif call.data == "category_query":
        make_menu_categories(call)

    elif call.data == "regions_query":
        make_menu_regions(call)

    elif call.data == "start_price_query":
        make_start_price(call)

    elif call.data == "end_price_query":
        make_end_price(call)

    elif call.data == "search_query":
        bot.answer_callback_query(call.id, show_alert=True, text="В разработке!")

    elif call.data == "back_menu":
        make_back_from_menu(call)

    elif call.data.split("_")[0] == "btnCategory":
        current_name = ''
        for k, v in flags.get("categories").items():
            if str(v[0]) == call.data.split("_")[1]:
                current_name = k
                break
        if not flags.get("categories").get(k)[1]:
            flags["categories"][current_name][1] = True
            make_menu_categories(call)
        else:
            flags["categories"][current_name][1] = False
            make_menu_categories(call)

    elif call.data.split("_")[0] == "btnRegions":
        current_name = ''
        for k, v in flags.get("regions").items():
            if str(v[0]) == call.data.split("_")[1]:
                current_name = k
                break
        if not flags.get("regions").get(k)[1]:
            flags["regions"][current_name][1] = True
            make_menu_regions(call)
        else:
            flags["regions"][current_name][1] = False
            make_menu_regions(call)

    elif call.data.split("_")[0] == "btnMarkets":
        current_name = ''
        for k, v in flags.get("markets").items():
            if str(v[0]) == call.data.split("_")[1]:
                current_name = k
                break
        if not flags.get("markets").get(k)[1]:
            flags["markets"][current_name][1] = True
            make_menu_markets(call)
        else:
            flags["markets"][current_name][1] = False
            make_menu_markets(call)


@bot.message_handler(commands=['start'])
def get_yes(message):
    bot.send_message(message.from_user.id, text="Добро пожаловать в бот!")
    bot.send_message(message.from_user.id, text="Давай настроим фильтр?", reply_markup=keyboard_menu)


bot.polling(none_stop=True, interval=0)
