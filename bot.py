#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
import urllib3
import json
import requests
import configparser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
urllib3.disable_warnings();
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

convert_dict = {}
convert_dict['{br}'] = '\n'
#Emoji Convert  
#http://apps.timwhitlock.info/emoji/tables/unicode#block-4-enclosed-characters
for i in range(63):
    convert_dict['{0}face:{1}{2}'.format('{', i, '}')] = (b'\xF0\x9F\x98' + bytes([0x81+i])).decode()

token, proxy= None, None
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get('Auth', 'Token')
    proxy = config.get('Proxy', 'Proxy')
except:
    if token is None:
        logger.fatal('parse config')
        exit()
    if proxy is None:
        logger.warn('proxy is not config')

def info(bot, update):
    if update.message.text.find(at_me) == -1:
        return
    update.message.reply_text('https://github.com/zwkno1/telegram_bot')

def chat(bot, update):
    print(update.message)
    if update.message.text.find(at_me) == -1:
        return
    msg = update.message.text.replace(at_me, '')
    
    if msg == 'info':
        update.message.reply_text('https://github.com/zwkno1/telegram_bot')
        return
    else:
        r = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=\"' + msg +'\"')
        chat_reply = json.loads(r.content.decode('utf-8'))['content']
        for k,v in convert_dict.items():
            chat_reply = chat_reply.replace(k,v)
        update.message.reply_text(chat_reply)

def main():
    bot = Bot(token=token, proxy=proxy)
    global at_me
    at_me = '@' + bot.getMe().username + ' '
    updater = Updater(bot=bot)
    updater.dispatcher.add_handler(CommandHandler('info', info))
    
    updater.dispatcher.add_handler(MessageHandler(Filters.text, chat))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

