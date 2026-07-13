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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🍲 Первые блюда", callback_data="primer")],
        [InlineKeyboardButton("🍛 Вторые блюда", callback_data="segundo")],
        [InlineKeyboardButton("🍰 Десерты", callback_data="postre")],
        [InlineKeyboardButton("🥤 Напитки", callback_data="bebida")],
        [InlineKeyboardButton("💶 Цена", callback_data="precio")],
        [InlineKeyboardButton("✅ Опубликовать", callback_data="publicar")],
    ]

    await update.message.reply_text(
        "Выберите раздел меню:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "primer":

        keyboard = [
            [InlineKeyboardButton("Gazpacho", callback_data="p_Gazpacho")],
            [InlineKeyboardButton("Sopa de marisco", callback_data="p_Sopa de marisco")],
            [InlineKeyboardButton("Crema de verduras", callback_data="p_Crema de verduras")],
        ]

        await query.edit_message_text(
            "Выберите первое блюдо:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
