from telethon import TelegramClient, events
import os.path
import configparser
import openai
import json
from re import M
import telebot, sys, time
from telebot import types
import datetime
import os
from random import randint

config = configparser.ConfigParser()
config.read(c + "config.ini", encoding="UTF-8")

s = os.path.abspath(__file__)
c = s.replace(os.path.basename(os.path.abspath(__file__)), "")
API_TOKEN = config["Params"]["token"]
bot = telebot.TeleBot(API_TOKEN)
openai.api_key = config["Params"]["key"]


global dicti
dicti = {"pfrase": config["Params"]["Pfrase"],
         "perepfrase": False,
         "counterPhoto": -1}


def telegram_parser(send_message_func=None, loop=None):
    
    api_id = config["Params"]["api_id"]
    api_hash = config["Params"]["api_hash"]
    
    channel_source = []
    for i in config["channel_source"]:
        channel_source.append(config["channel_source"][i])
    

    session = c+'gazp'

    client = TelegramClient(session, api_id, api_hash, loop=loop)
    client.start()

    @client.on(events.NewMessage(chats=channel_source))
    async def handler(event):
        if send_message_func is None:
            
            # media_group = []
            # text = 'some caption for album'
            # for num in range(3):
            #     media_group.append(InputMediaPhoto(open('%d.png' % num, 'rb'), 
            #                            caption = text if num == 0 else ''))
            # bot.send_media_group(chat_id = 5434593118, media = media_group)
            # bot.send_media_group(chat_id = 761607360, media = media_group)
            
            if event.photo:
                dicti["counterPhoto"] += 1
                await event.download_media(c+"Photos/"+str(dicti["counterPhoto"])+".png")
            
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": dicti["pfrase"]+" '"+ event.raw_text+ "'"}
                # {"role": "user", "content": event.raw_text}
            ]
            )
            
            # bot.send_media_group(5434593118, [telebot.types.InputMediaPhoto(open(c+ "Resources/1.png", "rb")),
            #                            telebot.types.InputMediaPhoto(open(c+ "Resources/2.png", "rb")),
            #                            telebot.types.InputMediaPhoto(open(c+ "Resources/3.png", "rb")),
            #                            telebot.types.InputMediaPhoto(open(c+ "Resources/4.png", "rb")),
            #                            telebot.types.InputMediaPhoto(open(c+ "Resources/5.png", "rb"))],)
            
            
            # bot.send_photo(5434593118, open(c+"Photos/1.png", "rb"), caption=completion.choices[0].message.content)
            
            
            
            # dicti["counterPhoto"] = -1
            # path = os.path.join(c+"Photos")
            # shutil.rmtree(path)
            # os.mkdir(c+"Photos")
            bot.send_message(config["Admins"]["1"], text=completion.choices[0].message.content)
            bot.send_message(config["Admins"]["2"], text=completion.choices[0].message.content)
            
            
            
        
        else:
            await send_message_func(f'@Testesttee\n{event.raw_text}')
            
            
    return client        


if __name__=='__main__':
    while True:
        try:
            client = telegram_parser()
            client.run_until_disconnected()
        except Exception as e:
            bot.send_message(config["Admins"]["1"], text=str(e))
            print(e)
            with open(c+ "errors.json", 'r') as f:
                data = json.load(f)
                dtn = datetime.datetime.now()
                data.append(
                    {"date": dtn.strftime('%d-%m-%Y %H:%M'), "Exception": str(e)})
            f.close()
            with open(c+ "errors.json", "w") as f:
                json.dump(data, f)
            f.close()
            
                
            time.sleep(5)
            continue




# @bot.message_handler(commands=["start"])
# def start(command):
#     # dicti = {"pfrase": "перефразируй"}
#     bot.send_message(command.from_user.id, text="Здаров")
    
# @bot.message_handler(commands=["admin"])
# def admin(command):
#     if str(command.from_user.id) == config["Admins"]["1"]:
#         keyboard = types.InlineKeyboardMarkup()
        
#         key = types.InlineKeyboardButton(text="Заменить фразу для бота перед сообщением", callback_data='pfrase')
#         keyboard.add(key)
        
#         question = "Что сделать?"
#         bot.send_message(command.from_user.id, text=question, reply_markup=keyboard)
#     else:
#         bot.send_message(5434593118, text="Здаров")

# @bot.message_handler(content_types=["text"])
# def func(message):
#     # global comment
#     if dicti["perepfrase"] == True:
#         dicti["pfrase"] = message.text
#         dicti["perepfrase"] = False
#     else:
#         print("ok")

# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
    
#     if call.data == "pfrase":
#         bot.send_message(call.from_user.id, text="Напиши фразу, которая будет стоять перед постом")
#         dicti["perepfrase"] = True


# scp ~/VScode/Python/Fun/Parser_bot_Dima/main.py devastrator101@45.8.230.170:/home/devastrator101/reposter_bot
# scp ~/VScode/Python/Fun/Parser_bot_Dima/config.ini devastrator101@45.8.230.170:/home/devastrator101/reposter_bot
# scp ~/VScode/Python/Fun/Parser_bot_Dima/errors.json devastrator101@45.8.230.170:/home/devastrator101/reposter_bot

# scp ~/VScode/Python/Fun/Parser_bot_Dima/Test/main.py xippi-xard@195.133.44.175:/home/xippi-xard/reposter_bot
# scp ~/VScode/Python/Fun/Parser_bot_Dima/Test/config.ini xippi-xard@195.133.44.175:/home/xippi-xard/reposter_bot
# scp ~/VScode/Python/Fun/Parser_bot_Dima/Test/gazp.session xippi-xard@195.133.44.175:/home/xippi-xard/reposter_bot
# scp ~/VScode/Python/Fun/Parser_bot_Dima/Test/gazp.session-journal xippi-xard@195.133.44.175:/home/xippi-xard/reposter_bot
# scp ~/VScode/Python/Fun/Parser_bot_Dima/Test/errors.json xippi-xard@195.133.44.175:/home/xippi-xard/reposter_bot