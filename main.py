import os
import sys
import telegram
import json
import requests
import time
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from telegram.ext import Updater, MessageHandler, Filters, Handler
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


TOKEN = os.environ.get('BOT_TOKEN')


def handle(bot):
    if update.effective_message.audio:
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

