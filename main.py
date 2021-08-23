import os
import mutagen
import telegram
import requests
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get('TOKEN')

def getdemo(update, context):
    chat_id = update.message.chat_id
    file_id = update.message['audio']['file_id']
    file = context.bot.get_file(file_id).download()
    if ".mp3" in file:
        audio = MP3(file)
        length = audio.info.length * 0.33
        l2 = (audio.info.length * 0.33) + 60
    if ".m4a" in file:
        audio = MP4(file)
        length = audio.info.length * 0.33
        l2 = (audio.info.length * 0.33) + 60
    if audio.info.length > l2:
        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + file + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 temp/output.ogg")
    else:
        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + file + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 temp/output.ogg")
    sendVoice(update.message.chat_id, "temp/output.ogg","")
        

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi, I am a simple Audio Cutter Bot !  I can send you a short piece of musics, The cut piece will be in the form of an voice message.")

def sendVoice(chat_id,file_name,text):
    url = "https://api.telegram.org/bot%s/sendVoice"%(TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'caption' : text}
    r= requests.post(url, files=files, data=data)
   
if __name__=='__main__':
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.audio, getdemo))
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
