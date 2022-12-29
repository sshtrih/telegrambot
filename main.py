import re
import telebot

from bot import CalculatorBot

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboa import Keyboa
from res import BOT_TOKEN

users = {}

# keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
#
# keyboard_subject = telebot.types.ReplyKeyboardMarkup(True, True)
#
# keyboard_achievement = telebot.types.ReplyKeyboardMarkup(True, True)
#
# keyboard_search = telebot.types.ReplyKeyboardMarkup(True, True)

bot = telebot.TeleBot(BOT_TOKEN)


def add_point(mess):
    if mess.text.startswith('/'):
        eval(mess.text[1:])(mess)
        return
    if re.search(r'[а-яА-Я]+ *- *\d{2}', mess.text):
        sub_point = re.split(r' *- *', mess.text)
        if users[mess.chat.id].new_search.add_point(*sub_point):
            bot.send_message(mess.chat.id, '✅ Добавлено')
        else:
            bot.send_message(mess.chat.id, '❌ Что-то не так.')
    else:
        bot.send_message(mess.chat.id, '❗Вы ошиблись в названии предмета')
    bot.register_next_step_handler(mess, add_point)


def create_user_request(chat_id):
    users[chat_id] = CalculatorBot()


@bot.message_handler(commands=['new_request'])
def new_request(message):
    users[message.chat.id].new_request()
    bot.send_message(message.chat.id, 'Данные сброшены, вы можете ввести новые')


@bot.message_handler(commands=['start'])
def start(message):
    create_user_request(message.chat.id)
    users[message.chat.id].start()
    mess = f'👋🏻 Привет, я помогу тебе подобрать вуз.\nВот список команд для продолжения:'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    help(message)


@bot.message_handler(commands=['help'])
def help(message):
    commands = f''' \nℹ /help - список всех команд
                    \n🔠 /subject - добавить предмет и балл за ЕГЭ
                    \n🏆 /achievement - добавить дополнительные достижения
                    \n🔎 /search - подобрать вуз
                    \n🆕 /new_request - найти вуз по новым параметрам
                    \n🏙 /place - выбрать субъект РФ
                    '''
    bot.send_message(message.chat.id, commands, parse_mode='html')


@bot.message_handler(commands=['direction'])
def direction(message):
    pass


@bot.message_handler(commands=['place'])
def place(message, n=0, edit_flag=True):
    with open('places_with_code.txt', 'r') as file:
        all_places = [{locality.strip(): code} for code, locality in (row.split(':') for row in file)]
    if n + 10 > len(all_places):
        items = [{'⏪ Назад': f'back-{n - 10}'}]

    elif n < 10:
        items = [{'Вперёд ⏩': f'next-{n + 10}'}]
    else:
        items = [{'⏪ Назад': f'back-{n - 10}'}, {'Вперёд ⏩': f'next-{n + 10}'}]

    keyboard_flipping = Keyboa(items=items, items_in_row=2).keyboard
    mess = 'Пожалуйста выберите один из нескольких субъектов или введите название сами'
    kb_places = Keyboa(items=all_places[n:n + 10], items_in_row=2).keyboard
    keyboard = Keyboa.combine(keyboards=(kb_places, keyboard_flipping))
    if edit_flag:
        res = bot.send_message(message.from_user.id, text=mess,
                               reply_markup=keyboard)
        users[message.from_user.id].message_id = res.id
    else:
        bot.edit_message_text(text=mess, chat_id=message.from_user.id,
                              message_id=users[message.from_user.id].message_id,
                              reply_markup=keyboard)


@bot.message_handler(commands=['subject'])
def subject(message):
    users[message.chat.id].get_subject()
    mess = f'Чтобы ввести баллы нужно сначала указать название предмета, а за тем через пробел балл ЕГЭ' \
           f'\n\n<u>Вот пример</u>:\n<b>Математика - 90</b>\n\n' \
           f'<u>Cписок предметов:</u>\n<b>{users[message.chat.id].subjects}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.register_next_step_handler(message, add_point)


def add_achievement(message):
    if message.text.startswith('/'):
        eval(message.text[1:])(message)
        return
    if users[message.chat.id].new_search.add_flag(message.text):
        bot.send_message(message.chat.id, '✅ Добавлено')
    else:
        bot.send_message(message.chat.id, '❌ Вы ошиблись')
    bot.register_next_step_handler(message, add_achievement)


@bot.message_handler(commands=['achievement'])
def achievement(message):
    mess = f'''Чтобы ввести дополнительное достижение, укажите одно или несколько из трёх достижений:
    \n🥇 Медаль\n🏃 ГТО\n🤝🏼 Волонтерство '''
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.register_next_step_handler(message, add_achievement)


@bot.message_handler(commands=['search'])
def search(message, n=0):
    if not users[message.from_user.id].response_status:
        users[message.from_user.id].get_active_subject()
        mess = f'⏳<b>Поиск вуза по параметрам:</b>\n\n<b>Предметы:</b>'
        for i in users[message.from_user.id].active_subject:
            mess += "\n" + ' - '.join(i)
        users[message.from_user.id].get_active_achievement()
        mess += '\n\n<b>Дополнительные достижения:</b>'
        for i in users[message.from_user.id].active_achievement:
            mess += '\n' + "".join(i)
        bot.send_message(message.from_user.id, mess, parse_mode='html')
        users[message.from_user.id].search()
        users[message.from_user.id].response_status = True
    mess = users[message.from_user.id].show_search_result(n)
    if not mess:
        users[message.from_user.id].response_status = False
        bot.send_message(message.from_user.id, users[message.from_user.id].search_result)
        bot.register_next_step_handler(message, add_point)
    else:
        if mess[0]:
            for i in mess[0]:
                bot_mess = f'🏫 <b>{i[0]}</b>\n\n<u>➡ Направление:</u>\n<b>{i[1]}</b>\n\n' \
                           f'🎓 <u>Профиль:</u>\n<b>{i[2]}</b>\n\n' \
                           f'🧩 <u>Подразделение:</u>\n<b>{i[3]}</b>\n\n' \
                           f'🔢 <u>Код направления:</u>\n<b>{i[4]}</b>\n\n' \
                           f'💯 <u>Проходной балл в прошлом году:</u>\n<b>{i[5]}</b>'
                bot.send_message(message.from_user.id, bot_mess, parse_mode='html')
                bot.send_photo(message.from_user.id, open(f'image/{i[0]}.png', 'rb'))
                n += 1
            if not mess[1]:
                btn_more = InlineKeyboardButton('Показать ещё', callback_data=str(n))
                inline_kb1 = InlineKeyboardMarkup().add(btn_more)
                bot.send_message(message.from_user.id, 'Чтобы увидеть ещё, нажмите на кнопку:',
                                 reply_markup=inline_kb1)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if re.match(r'^\d{4}', call.data):
        users[call.from_user.id].new_search.open_places_console()
        users[call.from_user.id].add_place(call.data)
    elif call.data[:4] == 'next':
        place(call, int(call.data[5:]), False)
    elif call.data[:4] == 'back':
        place(call, int(call.data[5:]), False)
    else:
        search(call, int(call.data))


bot.infinity_polling()
