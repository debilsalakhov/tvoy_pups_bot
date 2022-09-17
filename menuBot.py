from telebot import types
import uuid


class Menu:
    hash = {}
    cur_menu = {}
    extended_parameters = {}

    def __init__(self, name, buttons=None, parent=None):
        self.name = name
        self.buttons = buttons
        self.parent = parent
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        markup.add(*buttons)
        self.markup = markup
        self.__class__.hash[name] = self

    @classmethod
    def get_ext_par(cls, id):
        return cls.extended_parameters.get(id, None)

    @classmethod
    def set_ext_par(cls, parameter):
        id = uuid.uuid4().hex
        cls.extended_parameters[id] = parameter
        return id

    @classmethod
    def get_menu(cls, chat_id, name):
        menu = cls.hash.get(name)
        if menu is not None:
            cls.cur_menu[chat_id] = menu
        return menu

    @classmethod
    def get_cur_menu(cls, chat_id):
        return cls.cur_menu.get(chat_id)


# -------------------------------------------------------------------------
def goto_menu(bot, chat_id, name_menu):
    cur_menu = Menu.get_cur_menu(chat_id)
    if name_menu == 'Выход' and cur_menu is not None and cur_menu.parent is not None:
        target_menu = Menu.get_menu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.get_menu(chat_id, name_menu)

    if target_menu is not None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        return target_menu
    else:
        return None


# -------------------------------------------------------------------------
m_main = Menu('Главное меню', buttons=['Я люблю тебя ❤', '❤', 'Наши фоточки)', 'Что делаешь?'])
m_main_admin = Menu('Главное меню admin', buttons=['Я люблю тебя ❤', '❤', 'Наши фоточки)', 'Что делаешь?', '/admin_panel'])
m_admin_panel = Menu('admin_panel', buttons=['update_status', 'send_message', 'all_messages', 'last_messages', 'clean_all_messages', '/start'])
