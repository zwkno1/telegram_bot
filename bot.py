#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
import urllib3
import json
import requests
import configparser
import redis
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
urllib3.disable_warnings();
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

class message_handler:
    def __init__(self, host = 'localhost', port = 6379, db = 0):
        self._db = redis.StrictRedis(host=host, port=port, db=db)
        with open('message_handler.lua') as f1, open('rank.lua') as f2:
            script1 = f1.read()
            self._lua_sha_1 = self._db.script_load(script1)
            script2 = f2.read()
            self._lua_sha_2 = self._db.script_load(script2)

    def _key(self, message):
        return message.chat.type + ':' + str(message.chat_id)

    def _msgkey(self, message):
        return 'message:' + self._key(message) + ':' + str(message.from_user.id)

    def handle_message(self, message):
        user = str(message.from_user.id)
        name = message.from_user.first_name + ' ' + message.from_user.last_name
        print(self._msgkey(message))
        self._db.evalsha(self._lua_sha_1, 4, self._key(message), user, message, name)

    def static(self, message):
        ret = self._db.llen(self._msgkey(message))
        if ret is not None:
            return str(ret)
        return '0'

    def rank(self, message):
        try:
            ret = self._db.evalsha(self._lua_sha_2, 1, self._key(message))
        except:
            return 'error'

        result = ''
        if ret is not None:
            for i in range(len(ret)):
                if i%2 == 0: 
                    if ret[i] is not None:
                        result = result + ret[i].decode('utf-8') + ' : '
                    else:
                        result = result + 'xxx : '
                else:
                    result = result + ret[i].decode('utf-8') + '\n'
            return result
        return 'empty'

    def history(self, message, count = 1):
        ret = self._db.lrange(self._msgkey(message), -count, -1)
        result = ''
        if ret is not None:
            for i in range(len(ret)):
                result = result + '{0})\n'.format(i+1) + ret[i].decode('utf-8') + '\n' 
        result = result + 'total {0} messages.\n'.format(len(ret))
        return result
            
class emoji_converter:
    def __init__(self):
        self._convert_dict = {}
        self._convert_dict['{br}'] = '\n'
        #Emoji Convert  
        #http://apps.timwhitlock.info/emoji/tables/unicode#block-4-enclosed-characters
        for i in range(63):
            self._convert_dict['{0}face:{1}{2}'.format('{', i, '}')] = (b'\xF0\x9F\x98' + bytes([0x81+i])).decode()

    def convert(self, text):
        for k,v in self._convert_dict.items():
            text = text.replace(k,v)
        return text

converter = emoji_converter()
at_me = ''
handler = message_handler()

def check_auth(update):
    print(update.message)
    if update.message.chat.type != 'private' and update.message.text.find(at_me) == -1:
        return False
    msg = update.message.text.replace(at_me, '')
    msg = re.sub('\s*' + at_me +'\s*', '', update.message.text)
    update.message.text = msg
    return True

def auth(method):
    def wrapper(bot, update, *args):
        if check_auth(update):
            return method(bot, update, *args)
    return wrapper

@auth
def info(bot, update):
    update.message.reply_text('https://github.com/zwkno1/telegram_bot')

@auth
def static(bot, update):
    reply = handler.static(update.message)
    update.message.reply_text(reply)

@auth
def history(bot, update):
    reply = handler.history(update.message)
    update.message.reply_text(reply)

@auth
def rank(bot, update):
    reply = handler.rank(update.message)
    update.message.reply_text(reply)

def chat(bot, update):
    handler.handle_message(update.message)
    if not check_auth(update):
        return
    msg = update.message.text
    if msg == 'info':
        update.message.reply_text('https://github.com/zwkno1/telegram_bot')
        return
    else:
        r = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=\"' + msg +'\"')
        chat_reply = json.loads(r.content.decode('utf-8'))['content']
        chat_reply = converter.convert(chat_reply)
        update.message.reply_text(chat_reply)
        return 

def main():
    token, proxy= None, None
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        token = config.get('Auth', 'Token')
        proxy = config.get('Proxy', 'Proxy')
    except:
        pass

    if token is None:
        logger.fatal('token is not config')
        exit()
    if proxy is None:
        logger.warn('proxy is not config')
    
    bot = Bot(token=token, proxy=proxy)
    global at_me
    at_me = '@' + bot.getMe().username 

    updater = Updater(bot=bot)

    updater.dispatcher.add_handler(CommandHandler('info', info))
    updater.dispatcher.add_handler(CommandHandler('static', static))
    updater.dispatcher.add_handler(CommandHandler('history', history))
    updater.dispatcher.add_handler(CommandHandler('rank', rank))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, chat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

