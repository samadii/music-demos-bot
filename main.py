import os
import telegram
import logging
import requests
import time
import mutagen
from mutagen.mp3 import MP3
from telegram.ext import Updater, Bot, MessageHandler, Filters, Handler

TOKEN = os.environ.get('BOT_TOKEN')
