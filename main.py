# pip install pyTelegramBotAPI
# pip install telebot

import telebot
import datetime

# Замість 'YOUR_BOT_TOKEN' вставте свій токен бота, який ви отримали від BotFather
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Змінні для зберігання статусів акаунтів та часу останньої зміни
with open('status1.txt', mode="rt") as s1:
    akk_1 = s1.readline()
with open('status2.txt', mode="rt") as s2:
    akk_2 = s2.readline()
with open('time1.txt', mode="rt") as s3:
    last_change_time_1 = s3.readline()
with open('time2.txt', mode="rt") as s4:
    last_change_time_2 = s4.readline()

# Список користувачів, що отримують повідомлення
users = []


# Сисок користувачів, що можуть взаємодіяти
users_active = []
with open('users.txt', mode="rt") as users_active_file:
    for line in users_active_file:
        line = line.replace("\n", "")
        line = int(line)
        users_active.append(line)

# Функція для відправлення повідомлення про статус
def send_status_message(chat_id):
    message = f"Статус акаунту 1: {akk_1}\nСтатус акаунту 2: {akk_2}\n\nОстання зміна статусу акаунту 1: {last_change_time_1}\nОстання зміна статусу акаунту 2: {last_change_time_2}"
    bot.send_message(chat_id, message)

# Обробник команди /start або натискання на кнопку "старт"
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'старт')
def handle_start(message):
    global users
    if message.from_user.id not in users_active:
        bot.send_message(message.chat.id, "🚫Ви не маєте прав на виконання цієї дії🚫")
        return
    elif message.from_user.id in users:
        users.remove(message.from_user.id)
    users.append(message.from_user.id)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('акаунт 1', 'акаунт 2')
    markup.row('терміново', 'статус')
    bot.send_message(message.chat.id, "Привіт! \n \nЯ бот для зручного розподілу доступу до акаунтів в HelioScope \n \nКористуватися мною дуже просто: \n \nДля початку натисни на кнопку \"статус\". Так ти дізнаєшся, які акаунти наразі вільні \n \nЄ вільний акаунт? Ти можеш зайняти його, натиснувши відповідну кнопку (\"акаунт 1\" чи \"акаунт 2\") \n \nВсі твої колеги одразу отримають повідомлення, що цей акаунт вже зайнято! \n \nЗакінчив роботу? Натисни на цю ж кнопку ще раз, щоб твої колеги дізналися, що акаунт вже вільний і вони також можуть з ним попрацювати! \n \nЗнаходишся на об\'єкті і треба прямо зараз увійти в акаунт? Сміливо тисни кнопку \"терміново\"! Твої колеги отримають ДУЖЕ зрозуміле повідомлення про це! \n \nПриємної роботи!", reply_markup=markup)

# Обробник натискання кнопок
@bot.message_handler(func=lambda message: message.text in ['акаунт 1', 'акаунт 2'])
def handle_accounts(message):
    global akk_1, akk_2, last_change_time_1, last_change_time_2

    if message.from_user.id not in users_active:
        bot.send_message(message.chat.id, "🚫Ви не маєте прав на виконання цієї дії🚫")

    elif message.from_user.id not in users:
        bot.send_message(message.chat.id, "Натисніть спочатку СТАРТ в меню")

    elif message.text == 'акаунт 1':
        if akk_1 == "free":
            akk_1 = f"buzy_by_{message.from_user.username}"
            with open('status1.txt', mode="wt") as f1:
                f1.write(akk_1)
            last_change_time_1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('time1.txt', mode="wt") as f2:
                f2.write(last_change_time_1)
            send_status_message(message.chat.id)
            bot.send_message(message.chat.id, "👍Ви можете ввійти в аккаунт 1👍")
            user = message.from_user.username
            # Повідомлення іншим користувачам
            # Надсилання повідомлення всім іншим користувачам
            for user_id in users:  # Замініть users на список user_id інших користувачів
                if user_id != message.from_user.id:
                    bot.send_message(user_id, f"🔴{user} зайняв акаунт 1🔴")
        elif akk_1 == f"buzy_by_{message.from_user.username}":
            akk_1 = "free"
            with open('status1.txt', mode="wt") as f3:
                f3.write(akk_1)
            last_change_time_1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('time1.txt', mode="wt") as f4:
                f4.write(last_change_time_1)
            send_status_message(message.chat.id)
            bot.send_message(message.chat.id, "👋Ви вийшли з аккаунту 1👋")
            user = message.from_user.username
            # Повідомлення іншим користувачам
            # Надсилання повідомлення всім іншим користувачам
            for user_id in users:  # Замініть users на список user_id інших користувачів
                if user_id != message.from_user.id:
                    bot.send_message(user_id, f"🟢{user} звільнив акаунт 1🟢")
        else:
            bot.send_message(message.chat.id, f"😟Акаунт 1 зайнято користувачем {akk_1[8:]}, зачекайте😟")

    elif message.text == 'акаунт 2':
        if akk_2 == "free":
            akk_2 = f"buzy_by_{message.from_user.username}"
            with open('status2.txt', mode="wt") as f5:
                f5.write(akk_2)
            last_change_time_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('time2.txt', mode="wt") as f6:
                f6.write(last_change_time_2)
            send_status_message(message.chat.id)
            bot.send_message(message.chat.id, "👍Ви можете ввійти в аккаунт 2👍")
            user = message.from_user.username
            # Повідомлення іншим користувачам
            # Надсилання повідомлення всім іншим користувачам
            for user_id in users:  # Замініть users на список user_id інших користувачів
                if user_id != message.from_user.id:
                    bot.send_message(user_id, f"🔴{user} зайняв акаунт 2🔴")
        elif akk_2 == f"buzy_by_{message.from_user.username}":
            akk_2 = "free"
            with open('status2.txt', mode="wt") as f7:
                f7.write(akk_2)
            last_change_time_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('time2.txt', mode="wt") as f8:
                f8.write(last_change_time_2)
            send_status_message(message.chat.id)
            bot.send_message(message.chat.id, "👋Ви вийшли з аккаунту 2👋")
            user = message.from_user.username
            # Повідомлення іншим користувачам
            # Надсилання повідомлення всім іншим користувачам
            for user_id in users:  # Замініть users на список user_id інших користувачів
                if user_id != message.from_user.id:
                    bot.send_message(user_id, f"🟢{user} звільнив акаунт 2🟢")
        else:
            bot.send_message(message.chat.id, f"😟Акаунт 2 зайнято користувачем {akk_2[8:]}, зачекайте😟")

# Обробник натискання кнопки "терміново"
@bot.message_handler(func=lambda message: message.text == 'терміново')
def handle_urgent(message):
    user = message.from_user.username
    if message.from_user.id not in users_active:
        bot.send_message(message.chat.id, "🚫Ви не маєте прав на виконання цієї дії🚫")
    # Повідомлення іншим користувачам
    # Надсилання повідомлення всім іншим користувачам
    elif message.from_user.id not in users:
        bot.send_message(message.chat.id, "Натисніть спочатку СТАРТ в меню")
    else:
        for user_id in users:  # Замініть users на список user_id інших користувачів
            if user_id != message.from_user.id:
                bot.send_message(user_id, f"‼️ {user} терміново потрібен доступ до акаунту‼️")

# Обробник натискання кнопки "статус"
@bot.message_handler(func=lambda message: message.text == 'статус')
def handle_status(message):
    if message.from_user.id not in users_active:
        bot.send_message(message.chat.id, "🚫Ви не маєте прав на виконання цієї дії🚫")
    elif message.from_user.id not in users:
        bot.send_message(message.chat.id, "Натисніть спочатку СТАРТ в меню")
    else:
        send_status_message(message.chat.id)

# Обробник натискання невідомої команди
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "Не розпізнано команду. Використовуйте кнопки для взаємодії з ботом (квадратний ґудзик трохи нижче і правіше).")

# Запускаємо бота
bot.polling()
