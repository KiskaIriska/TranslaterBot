import telebot
import config
from telebot import types
from googletrans import Translator
from googletrans import LANGUAGES

#указать свой токен вместо config.token
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["help"])
def helping(message):
    bot.send_message(message.chat.id,
                     "Выбери пункт /translate, чтобы перевести текст или пункт /languages, чтобы посмотреть доступные языки")


@bot.message_handler(commands=["languages"])
def languages(message):
    all_languages = ''
    for lang in LANGUAGES:
        all_languages = all_languages + '\n' + lang + ' - ' + LANGUAGES[lang]
    bot.send_message(message.chat.id,
                     all_languages)


@bot.message_handler(commands=["translate"])
def select_translate(message):
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="RU_EN", callback_data="RU_EN")
    but_2 = types.InlineKeyboardButton(text="EN_RU", callback_data="EN_RU")
    but_3 = types.InlineKeyboardButton(text="Translate", callback_data="Translate")
    key.add(but_1, but_2, but_3)
    bot.send_message(message.chat.id, "Выберите язык для перевода:", reply_markup=key)


@bot.callback_query_handler(func=lambda c: True)
def inlin(c):
    if c.data == "RU_EN":
        bot.send_message(c.message.chat.id, "Напиши текст")
        bot.register_next_step_handler(c.message, translate_ru_en)
    elif c.data == "EN_RU":
        bot.send_message(c.message.chat.id, "Напиши текст")
        bot.register_next_step_handler(c.message, translate_en_ru)
    #переводит на любой язык, внесенный в список languages, исходный язык определяется автоматически
    elif c.data == "Translate":
        bot.send_message(c.message.chat.id,
                         "Введите требуемый язык перевода на английском, либо воспользуйтесь /languages, чтобы посмотреть доступные языки")
        bot.register_next_step_handler(c.message, choose_language)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, " + message.chat.first_name + ", я помогу перевести нужный текст")


@bot.message_handler(content_types=["text"])
def dialog(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Привет, " + message.chat.first_name)
    elif message.text == "Как дела?" or message.text == "Как дела":
        bot.send_message(message.chat.id, "Отлично")


def translate_ru_en(message):
    trans = Translator()
    text = message.text
    t = trans.translate(
        text, sourse='ru', dest='en')
    bot.send_message(message.chat.id,
                     'Исходный язык: ' + t.src + ' Язык перевода: ' + t.dest + '\n' + t.origin + '->' + t.text)


def translate_en_ru(message):
    trans = Translator()
    text = message.text
    t = trans.translate(
        text, sourse='en', dest='ru')
    bot.send_message(message.chat.id,
                     'Исходный язык: ' + t.src + ' Язык перевода: ' + t.dest + '\n' + t.origin + '->' + t.text)

# проверка выбранного языка
def choose_language(message):
    lan = message.text
    all_languages = ''
    for lang in LANGUAGES:
        all_languages = all_languages + '\n' + lang + ' - ' + LANGUAGES[lang]
    str = all_languages.find(lan)
    if (str == -1):
        bot.send_message(message.chat.id,
                         'Неверно указан язык, попробуйте еще раз или воспользуйтесь /languages, чтобы посмотреть доступные языки')
    else:
        bot.send_message(message.chat.id, 'Напиши текст')
        bot.register_next_step_handler(message, translating, lan)

#перевод
def translating(message, lan):
    try:
        trans = Translator()
        text = message.text
        t = trans.translate(text, dest=lan)
        bot.send_message(message.chat.id,
                         'Исходный язык: ' + t.src + ' Язык перевода: ' + t.dest + '\n' + t.origin + '->' + t.text)
    except Exception as e:
        bot.send_message(message.chat.id,
                         'Ошибка')


bot.polling(none_stop=True)