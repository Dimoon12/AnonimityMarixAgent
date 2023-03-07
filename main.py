import simplematrixbotlib as botlib
import hashlib
import secrets


#cred.txt НикБота:Пароль:Комната куда бот отправляет сообщения с других чатов
# сервер  вписывать внизу
with open("cred.txt", "r") as f:
    login, password, mainroom = f.read().split(":", maxsplit=2)

#настройки библиотеки и запуск бота
PREFIX = '!'
config = botlib.Config()
config.encryption_enabled = True
config.emoji_verify = True
config.ignore_unverified_devices = True

creds = botlib.Creds("https://cuteworld.space", f"{login}", f"{password}")
bot = botlib.Bot(creds, config)



#создать новую соль
def keyreset():
    global salt
    salt=secrets.token_hex(128)

keyreset()
@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)
    global salt
    #Разбор собщения о появлении сообщения пользователя для дальнейшей обработки
    message = str(message).split(":", 2)
    server = message[1].strip()
    username = message[0].strip()
    message = message[2].strip()
    #Проверка на то что сообщение не бота
    if match.is_not_from_this_bot():
        # Проверка на то что сообещение родилось не в основной комнате
        if room.room_id == mainroom:
            pass
        else:
            if message == "keyreset":
                #Глобально сбросить соль и следовательно идентефикаторы
                keyreset()
                await bot.api.send_markdown_message(room, "**Идентификатор сброшен!**")
            else:
                #Слепить имя пользователя и соль
                IdAssemble=bytes(username+salt, 'utf-8')
                hashed=hashlib.sha256(IdAssemble).hexdigest()
                await bot.api.send_markdown_message(mainroom, f"{message} \nОтпечаток: {hashed}")
bot.run()