from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from github import Github
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPO_NAME = "veradana1993-gif/-Los-Faroles-Menu"
FILE_PATH = "menu.json"

menu = {
    "primerPlato": "",
    "segundoPlato": "",
    "postre": "",
    "bebida": "",
    "precio": ""
}
