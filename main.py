#!/usr/bin/python3

import sys
import time
import os
import os.path
import re
import time
import random
import mutagen
import string
import json
import urllib.request
import html.parser
import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from telegram.error import NetworkError, Unauthorized
from pprint import pprint

update_id = None
thumb = "temp/thumb.jpg"
extraoptions = ""
extraoptions2 = "--force-ipv4"

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get('TOKEN')
else:
    TOKEN = ""
if 'MODULES' in os.environ:
    MODULES = os.environ.get('MODULES')
else:
    MODULES = 'voice'

f = open("db/random.txt", "w+")
f.write(str(random.randint(10,30)))
f.close()

VERSION = "0.9.4"

def isenabled(chat_id, module):
    blacklist = open("blacklist.txt", "r").read()
    modenabled = False
    for x in MODULES.split(','):
        if x == module:
            modenabled = True
    if str(chat_id) in blacklist:
        modenabled = False
    if "*" in blacklist:
        modenabled = False
    return modenabled
            

def handle(bot):
    blacklist = open("blacklist.txt", "r").read()
    if not "*" in blacklist:
        global update_id
        for update in bot.get_updates(offset=update_id, timeout=10):
            update_id = update.update_id + 1
            if update.effective_message:
                try:
                    botlang = update.effective_message.from_user.language_code
                    if "de" in botlang:
                        botlang = "de"
                    else:
                        botlang = "c"
                except:
                    botlang = "c"
                done = False
                bottag = bot.getMe()["username"]
                f = open("db/random.txt", "r")
                rnumber = int(f.read())
                f.close()
                chat_type = update.effective_message.chat.type
                chat_id = update.effective_message.chat_id
                isAdmin = False
                if not str(chat_id) in blacklist:
                    try:
                        admins = bot.getChatAdministrators(chat_id)
                        for user in admins:
                            try:
                                if str(user['user']['username']).replace("u'", "").replace("'", "") == bottag:
                                    isAdmin = True
                            except:
                                pass
                    except:
                        pass
                    def start():
                        f = open("lang/" + botlang + "/start")
                        s = f.read()
                        f.close()
                        if bottag == "e43bot":
                            s = s.replace("%%name%%", "E43")
                        else:
                            if botlang == "c":
                                s = s.replace("%%name%%", bot.getMe().first_name + ", ein Klon von E43")
                        try:
                            fileid = bot.getUserProfilePhotos(bot.getMe().id).photos[0][0].file_id
                            bot.sendPhoto(chat_id,fileid,s)
                        except:
                            os.system("convert e43.png -resize 512x512 temp/thumb.jpg")
                            bot.sendPhoto(chat_id,open("temp/thumb.jpg", "rb"),s)
                            os.system("rm -f temp/thumb.jpg")
                    if chat_type == "private" or "group" in chat_type:
                        try:
                            if chat_type == "private":
                                f = open("db/chatids.txt", "r")
                            else:
                                f = open("db/chatids2.txt", "r")
                            x = f.read()
                            f.close()
                            f = open("db/subsoff.txt", "r")
                            y = f.read()
                            f.close()
                            if not str(chat_id) in x:
                                try:
                                    if chat_type == "private":
                                        f = open("db/chatids.txt", "a+")
                                    else:
                                        f = open("db/chatids2.txt", "a+")
                                    f.write(str(chat_id) + ":" + update.effective_message.from_user.username + "\n")
                                    f.close()
                                except:
                                    if chat_type == "private":
                                        f = open("db/chatids.txt", "a+")
                                    else:
                                        f = open("db/chatids2.txt", "a+")
                                    f.write(str(chat_id) + "\n")
                                    f.close()
                            if str(chat_id) in y:
                                lines = y.split("\n")
                                if chat_type == "private":
                                    f = open("db/chatids.txt", "w")
                                else:
                                    f = open("db/chatids2.txt", "w")
                                for line in lines:
                                    if not str(chat_id) in line:
                                        f.write(line)
                                f.close()
                        except:
                            pass
                    if update.effective_message.text:
                        if "start" in update.effective_message['text']:
                            markup = InlineKeyboardMarkup([InlineKeyboardButton("📬 Share", url=https://github.com/nertflix/button-creator-bot)])
                            try:
                                bot.sendMessage(chat_id, "Hey !  I am a simple Audio Cutter Bot !  I can send you a short piece of musics, The cut piece will be in the form of an voice message.", reply_to_message_id=update.effective_message.message_id, reply_markup=markup) 
                            except:
                                pass
                    if update.effective_message.audio and isenabled(chat_id, "voice"):
                        try:
                            fileid = update.effective_message.audio.file_id
                            print(fileid)
                            getfile = bot.get_file(fileid).download()
                            filename = getfile
                            if ".mp3" in filename:
                                audio = MP3(filename)
                                length = audio.info.length * 0.33
                                l2 = (audio.info.length * 0.33) + 60
                            if ".m4a" in filename:
                                audio = MP4(filename)
                                length = audio.info.length * 0.33
                                l2 = (audio.info.length * 0.33) + 60
                            if audio.info.length > l2:
                                os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 temp/output.ogg")
                            else:
                                os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 temp/output.ogg")
                            sendVoice(update.effective_message.chat_id, "temp/output.ogg","")
                        except:
                            pass

def sendVoice(chat_id,file_name,text):
    url = "https://api.telegram.org/bot%s/sendVoice"%(TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'caption' : text}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

print('Listening ...')

def main():
    global update_id
    bot = telegram.Bot(TOKEN)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            handle(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            update_id += 1

if __name__ == '__main__':
    main()
