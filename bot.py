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

}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🍲 Первые блюда", callback_data="primer")],
        [InlineKeyboardButton("🍛 Вторые блюда", callback_data="segundo")],
        [InlineKeyboardButton("🍰 Десерты", callback_data="postre")],
        [InlineKeyboardButton("✅ Опубликовать", callback_data="publicar")],
    ]

    await update.message.reply_text(
        "Выберите раздел меню:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    if query.data.startswith("p_"):
        menu["primerPlato"] = query.data.replace("p_", "")

        await query.edit_message_text(
            f"✅ Первое блюдо:\n\n{menu['primerPlato']}"
        )
        return
        if query.data.startswith("s_"):
    menu["segundoPlato"] = query.data.replace("s_", "")

    await query.edit_message_text(
        f"✅ Второе блюдо:\n\n{menu['segundoPlato']}"
    )
    return
    if query.data == "primer":
elif query.data == "segundo":

    keyboard = [
        [InlineKeyboardButton("Paella", callback_data="s_Paella")],
        [InlineKeyboardButton("Pollo al horno", callback_data="s_Pollo al horno")],
        [InlineKeyboardButton("Costillas en salsa", callback_data="s_Costillas en salsa")],
    ]

    await query.edit_message_text(
        "Выберите второе блюдо:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
        keyboard = [
            [InlineKeyboardButton("Gazpacho", callback_data="p_Gazpacho")],
            [InlineKeyboardButton("Sopa de marisco", callback_data="p_Sopa de marisco")],
            [InlineKeyboardButton("Crema de verduras", callback_data="p_Crema de verduras")],
        ]

        await query.edit_message_text(
            "Выберите первое блюдо:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
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
}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🍲 Первые блюда", callback_data="primer")],
        [InlineKeyboardButton("🍛 Вторые блюда", callback_data="segundo")],
        [InlineKeyboardButton("🍰 Десерты", callback_data="postre")],
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

async def save_menu():

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    file = repo.get_contents(FILE_PATH)

    data = json.loads(file.decoded_content.decode())

    data["menuDelDia"]["primerPlato"] = menu["primerPlato"]
    data["menuDelDia"]["segundoPlato"] = menu["segundoPlato"]
    data["menuDelDia"]["postre"] = menu["postre"]
    from datetime import datetime

dia = datetime.now().weekday()

if dia == 5:
    precio = "CERRADO"
elif dia == 6:
    precio = "17 €"
else:
    precio = "14 €"

data["menuDelDia"]["precio"] = precio

    repo.update_file(
        FILE_PATH,
        "Меню обновлено из Telegram",
        json.dumps(data, ensure_ascii=False, indent=2),
        file.sha,
    )
