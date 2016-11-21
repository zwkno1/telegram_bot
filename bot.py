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
    if update.message.text.find('@zwk_bot ') != 0:
        return
    update.message.reply_text('https://github.com/zwkno1')

def chat(bot, update):
    if update.message.text.find('@zwk_bot ') != 0:
        return
    print(update.message)
    r = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=\"' + update.message.text +'\"')
    chat_reply = json.loads(r.content.decode('utf-8'))['content']
    chat_reply = chat_reply.replace('{br}', '\n')
    update.message.reply_text(chat_reply)
    #bot.sendMessage(chat_id=update.message.chat_id, text=chat_reply)

def main():
    updater = Updater(bot = Bot(token=token, proxy=proxy))
    updater.dispatcher.add_handler(CommandHandler('info', info))
    
    updater.dispatcher.add_handler(MessageHandler(Filters.text, chat))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

