import telebot
import sqlite3
from telebot import types
import requests
import json

TOKEN = '6523571953:AAGoTAnmjz4m3uTfB7DrqY-Cn2W6Dtjmnxs'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_first_message(message):
    user_id = message.chat.id
    username = message.from_user.username

    conn = sqlite3.connect('user_actions.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user_actions (user_id INTEGER, action_performed INTEGER, phone TEXT, telega TEXT, name TEXT, idlieds TEXT, com1 TEXT, com2 TEXT)")
    cursor.execute("SELECT * FROM user_actions WHERE user_id=? AND telega=?", (user_id, username))
    result = cursor.fetchone()
    
    if not result:
        reply_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Да', callback_data='yes', color="green")
        button2 = types.InlineKeyboardButton('Нет', callback_data='no', color="red")
        reply_markup.row(button1, button2)
        bot.send_message(user_id, f"{username} Вас приветствует <<ПромТрейдИнвест>>!")
        bot.send_message(user_id, f"Есть ли у Вас грохоты на производстве?", reply_markup=reply_markup)

        cursor.execute("INSERT INTO user_actions (user_id, action_performed, telega) VALUES (?, ?, ?)", (user_id, 1, username))
        conn.commit()
        webhook = 'https://ooo-promtreydinvest.bitrix24.ru/rest/279/krv77xyjn6k6hd13/'

        data = {
            'fields': {
                'SOURCE_ID': 'UC_Z21M33',
                #'COMMENTS': sex,
                #'EMAIL': [{ "VALUE": q7_option5, "VALUE_TYPE": "WORK" }],
                #'PHONE': [{ "VALUE": q7_option4, "VALUE_TYPE": "WORK" }],
                #'POST': q7_option6,
                'ASSIGNED_BY_ID': 2025,
                'UF_CRM_1711078661443': user_id,
                'UF_CRM_1711078671157': username
                #'UF_CRM_1709090565': mes1
            }
        }

        response = requests.post(f'{webhook}/crm.lead.add', headers={'Content-Type': 'application/json'}, data=json.dumps(data))

        if response.status_code == 200:
            result = response.json()['result']
            print(result, 'смотри есть айди')
            conn = sqlite3.connect('user_actions.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE user_actions SET idlieds = ? WHERE user_id = ?", (result, user_id))
            conn.commit()

            
           
            
        else:
            print('Произошла ошибка:', response.text)

    cursor.close()
    conn.close()

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    user_id = call.message.chat.id
    
    if call.data == 'yes':
        '''
        new_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Песок', callback_data='sand')
        button2 = types.InlineKeyboardButton('Гравий', callback_data='gravel')
        new_markup.row(button1, button2)
        
        bot.send_message(user_id, "Какие материалы просеиваете?", reply_markup=new_markup)
        
       
        new_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Щебень', callback_data='gravel'),
        button2 = types.InlineKeyboardButton('Песок', callback_data='sand'),
        button3 = types.InlineKeyboardButton('Песчано-гравийная смесь (ПГС)', callback_data='sand_gravel_mix'),
        button4 = types.InlineKeyboardButton('Железорудное сырье (ЖРС)', callback_data='iron_ore'),
        button5 = types.InlineKeyboardButton('Ферросплавы', callback_data='ferroalloys'),
        button6 = types.InlineKeyboardButton('Калийные удобрения', callback_data='potash_fertilizers'),
        button7 = types.InlineKeyboardButton('Известняк', callback_data='limestone'),
        button8 = types.InlineKeyboardButton('Уголь энергетический, кокс', callback_data='coal_coke'),
        button9 = types.InlineKeyboardButton('Кварцевые материалы', callback_data='quartz_materials')
        new_markup.row(button1, button2,button3, button4,button5, button6,button7, button8,button9)
        bot.send_message(user_id, "Какие материалы просеиваете?", reply_markup=new_markup)
        '''
        new_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Песок', callback_data='sand')
        button2 = types.InlineKeyboardButton('Щебень', callback_data='gravel')
        button3 = types.InlineKeyboardButton('ПГС', callback_data='sand_gravel_mix')
        button4 = types.InlineKeyboardButton('ЖРС', callback_data='iron_ore')
        button5 = types.InlineKeyboardButton('Ферросплавы', callback_data='ferroalloys')
        button6 = types.InlineKeyboardButton('Калийные удобрения', callback_data='potash_fertilizers')
        button7 = types.InlineKeyboardButton('Известняк', callback_data='limestone')
        button8 = types.InlineKeyboardButton('Уголь кокс', callback_data='coal_coke')
        button9 = types.InlineKeyboardButton('Кварцевые материалы', callback_data='quartz_materials')

        new_markup.row(button1, button2)
        new_markup.row(button3, button4)
        new_markup.row(button5, button6)
        new_markup.row(button7, button8)
        new_markup.add(button9)

        bot.send_message(user_id, "Какие материалы просеиваете?", reply_markup=new_markup)
        
    elif call.data == 'no':
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        bot.answer_callback_query(call.id, text="Желаем Вам приятно посещения выстовки")
    elif call.data in ['sand', 'gravel', 'sand_gravel_mix', 'iron_ore', 'ferroalloys', 'potash_fertilizers', 'limestone', 'coal_coke', 'quartz_materials']:
        conn = sqlite3.connect('user_actions.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user_actions SET com1 = ? WHERE user_id = ?", (call.data, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        new_markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Низкая производительность грохота', callback_data='e1')
        button2 = types.InlineKeyboardButton('Залипание, забивание сеток и сит', callback_data='e2')
        button3 = types.InlineKeyboardButton('Частый поломки сетки', callback_data='e3')
        button4 = types.InlineKeyboardButton('Нет проблем', callback_data='e4')
        button5 = types.InlineKeyboardButton('Брак фракции', callback_data='e5')
        new_markup.row(button3)
        new_markup.row(button2)
        new_markup.row(button1)
        new_markup.row(button5)
        
        new_markup.row(button4)
        bot.send_message(user_id, "С какими проблемами сталкиваетесь при просеве?", reply_markup=new_markup)
    elif call.data in ['e1', 'e2', 'e3', 'e4', 'e5']:
        if call.data == 'e1':
            bot.send_message(user_id, "**Решение**: Установите сита с Е рифлением, чтобы увеличить скорость просева **Выгода**: Прирост производительности +15%")
            conn = sqlite3.connect('user_actions.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE user_actions SET com2 = ? WHERE user_id = ?", ('**Решение**: Установите сита с Е рифлением, чтобы увеличить скорость просева **Выгода**: Прирост производительности +15%', user_id))
            conn.commit()
            cursor.close()
            conn.close()
        elif call.data == 'e2':
            bot.send_message(user_id, "**Решение**: Установите на грохот самоочищающиеся сита **Выгода**: 100% чистая поверхность просева. Прирост производительности грохота на 40%")
            conn = sqlite3.connect('user_actions.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE user_actions SET com2 = ? WHERE user_id = ?", ('**Решение**: Установите на грохот самоочищающиеся сита **Выгода**: 100% чистая поверхность просева. Прирост производительности грохота на 40%', user_id))
            conn.commit()
            cursor.close()
            conn.close()
        elif call.data == 'e3':
            bot.send_message(user_id, "**Решение**: Используйте сита, изготовленные из пружинной проволоки, марка стали 45-70 **Выгода**: В 2 раза реже остановки грохота для замены сит. Снижение на 50% расходов на закуп сеток ")
            conn = sqlite3.connect('user_actions.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE user_actions SET com2 = ? WHERE user_id = ?", ('**Решение**: Используйте сита, изготовленные из пружинной проволоки, марка стали 45-70 **Выгода**: В 2 раза реже остановки грохота для замены сит. Снижение на 50% расходов на закуп сеток ', user_id))
            conn.commit()
            cursor.close()
            conn.close()
        elif call.data == 'e5':
            bot.send_message(user_id, "**Решение**: Применяйте сита с D или Е рифлением. Возможно использование арфобразных сеток на ячейках менее 30мм **Выгода**: 100% Повышение класса готовой продукции. Фракция материала в норме")
            conn = sqlite3.connect('user_actions.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE user_actions SET com2 = ? WHERE user_id = ?", ('**Решение**: Применяйте сита с D или Е рифлением. Возможно использование арфобразных сеток на ячейках менее 30мм **Выгода**: 100% Повышение класса готовой продукции. Фракция материала в норме', user_id))
            conn.commit()
            cursor.close()
            conn.close()
        conn = sqlite3.connect('user_actions.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_actions WHERE user_id=?", (user_id,))
        result1 = cursor.fetchone()
        print('Смотри--> ',result1[5])
        webhook = 'https://ooo-promtreydinvest.bitrix24.ru/rest/279/krv77xyjn6k6hd13/'

        data = {
            'ID': result1[5],
            'fields': {
                'COMMENTS': f'{result1[6]}  \n {result1[7]}'
            }
        }
        response = requests.post(f'{webhook}/crm.lead.update', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        result2 = response.json()
        print('На месте')
        print(result2)
        conn.commit()
        cursor.close()
        conn.close()
                      
        bot.send_message(user_id, "Ждем Вас в павильон №1, зал 3, стенд С6053. Решим Ваши проблемы с грохотом")
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_contact = types.KeyboardButton("Отправить контакт", request_contact=True)
        reply_markup.add(button_contact)

        bot.send_message(user_id, f"Нажмите на кнопку 'Отправить контакт', чтобы поделиться своим номером телефона.", reply_markup=reply_markup)
    elif request_contact == True:
        bot.send_message(user_id, "Спасибо за предоставления контакта. Мы в социальных сетях https://taplink.cc/pti54")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.chat.id
    contact_info = message.contact
    username = message.from_user.username
    phone_number = contact_info.phone_number
    # Обновляем запись в базе данных с телефонным номером пользователя
    conn = sqlite3.connect('user_actions.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_actions SET phone = ?, telega = ? WHERE user_id = ?", (phone_number,username, user_id))
    conn.commit()

    cursor.close()
    conn.close()
    conn = sqlite3.connect('user_actions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_actions WHERE user_id=?", (user_id,))
    result1 = cursor.fetchone()
    print('Смотри--> ',result1[5])
    webhook = 'https://ooo-promtreydinvest.bitrix24.ru/rest/279/krv77xyjn6k6hd13/'

    data = {
            'ID': result1[5],
            'fields': {
                'PHONE': [{ "VALUE": result1[2], "VALUE_TYPE": "WORK" }],
            }
    }
    response = requests.post(f'{webhook}/crm.lead.update', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    result2 = response.json()
    print('На месте')
    print(result2)
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(user_id, "Спасибо за предоставленный контакт. Мы в социальных сетях https://taplink.cc/pti54")
bot.polling()
