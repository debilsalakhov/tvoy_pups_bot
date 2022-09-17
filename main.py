import telebot
from telebot import types
import menuBot
from menuBot import Menu
import pandas as pd
import apihelper
import SECRET


apihelper.ENABLE_MIDDLEWARE = True
apihelper.SESSION_TIME_TO_LIVE = 5 * 60
bot = telebot.TeleBot(SECRET.BOT_TOKEN)  # @tvoy_pups_bot


# -------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def get_start_command(message):
    chat_id = message.chat.id
    txt_message = f'Привет, зайка ❤\nКак видишь, я не твой настоящий пупсик, но ты можешь писать мне, когда его нет рядом и он не может ответить. В принципе, можешь представить, что я это он)\nя тебя очень сильно люблю ❤❤❤'

    if message.from_user.id == SECRET.ADMIN_ID:
        bot.send_message(chat_id, text=txt_message, reply_markup=Menu.get_menu(chat_id, 'Главное меню admin').markup)
    else:
        df = pd.read_csv('users.csv')
        df.loc[-1, ['user_name']] = message.from_user.username
        df.loc[-2, ['user_id']] = message.from_user.id
        df.to_csv('users.csv', index=False)
        bot.send_message(chat_id, text=txt_message, reply_markup=Menu.get_menu(chat_id, 'Главное меню').markup)

    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAMIYwtn2fAnCspbwUeaUHct2JvQguUAAmEgAALb32BILg0K73F7-LwpBA')  # memoji чмок


# -------------------------------------------------------------------------
@bot.message_handler(commands=['admin_panel'])
def get_admin_panel_command(message):
    chat_id = message.chat.id
    menuBot.goto_menu(bot, chat_id, 'admin_panel')


# -------------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def get_txt_message(message):
    chat_id = message.chat.id
    ms_text = message.text
    if ms_text == 'Я люблю тебя ❤':
        bot.send_message(chat_id, text='Я тебя тоже очень сильно люблю зайка ❤❤❤')
    elif ms_text == '❤':
        bot.send_message(chat_id, text='❤')
    elif ms_text == 'Наши фоточки)':
        df = pd.read_csv('file_id_table_photo.csv')
        random_row = df.sample()
        file_id = random_row.iloc[0, 0]
        bot.send_photo(chat_id, photo=file_id)
    elif ms_text == 'send_message':
        msg = bot.send_message(chat_id, text='please write user id')
        bot.register_next_step_handler(msg, msg_from_bot_1)
    elif ms_text == 'update_status':
        msg = bot.send_message(chat_id, 'please write your actual status')
        bot.register_next_step_handler(msg, update_status)
    elif ms_text == 'Что делаешь?':
        df = pd.read_csv('status.csv')
        status = df.iloc[0, 0]
        bot.send_message(chat_id, text=status)
    elif ms_text == 'all_messages':
        df = pd.read_csv('all_messages.csv')
        for index, row in df.iterrows():
            bot.send_message(chat_id, text=row['message'])
    elif ms_text == 'last_messages':
        df = pd.read_csv('last_messages.csv')
        for index, row in df.iterrows():
            bot.send_message(chat_id, text=row['message'])
        df_empty = df[0:0]
        df_empty.to_csv('last_messages.csv', index=False)
    elif ms_text == 'clean_all_messages':
        df = pd.read_csv('all_messages.csv')
        df_empty = df[0:0]
        df_empty.to_csv('all_messages.csv', index=False)
        bot.send_message(chat_id, 'all messages history was cleaned')
    else:
        df_all = pd.read_csv('all_messages.csv')
        df_all.loc[-1, ['message']] = ms_text
        df_all.to_csv('all_messages.csv', index=False)
        df_last = pd.read_csv('last_messages.csv')
        df_last.loc[-1, ['message']] = ms_text
        df_last.to_csv('last_messages.csv', index=False)
        bot.send_message(chat_id, 'Я не понял, что ты от меня хочешь, поэтому отправил это сообщение твоему настоящему пупсику')


# -------------------------------------------------------------------------
def update_status(message):
    df = pd.read_csv('status.csv')
    df.loc[0, ['status']] = message.text
    df.to_csv('status.csv', index=False)
    bot.send_message(message.chat.id, text='your status was updated')


# -------------------------------------------------------------------------
def msg_from_bot_1(message):
    global user_id
    user_id = message.text
    msg = bot.send_message(message.chat.id, text='please write your message')
    bot.register_next_step_handler(msg, msg_from_bot_2)


# -------------------------------------------------------------------------
def msg_from_bot_2(message):
    bot.send_message(user_id, f'{message.text}')
    bot.send_message(message.chat.id, 'message was sent successfully')


# -------------------------------------------------------------------------
# def append_table_csv(file_id: str):
#     df = pd.read_csv('file_id_table_photo.csv')
#     df.loc[-1, ['file_id']] = file_id
#     df.to_csv('file_id_table_photo.csv', index=False)
#
#
# # ---------------------------------------
# @bot.message_handler(content_types=['photo'])
# def give_file_id(message):
#     chat_id = message.chat.id
#     append_table_csv(message.photo[2].file_id)
#     bot.send_message(chat_id, text=message.photo[2].file_id)


# ---------------------------------------

bot.polling(none_stop=True, interval=0)
