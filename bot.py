from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from github import Github
from datetime import datetime
import json
import os

TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPO_NAME = "veradana1993-gif/-Los-Faroles-Menu"
FILE_PATH = "menu.json"

menu = {
    "primerPlato": [],
    "segundoPlato": [],
    "postre": [],
}

estado = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🍲 Первые блюда", callback_data="primer")],
        [InlineKeyboardButton("🍛 Вторые блюда", callback_data="segundo")],
        [InlineKeyboardButton("🍰 Десерты", callback_data="postre")],
        [InlineKeyboardButton("✅ Опубликовать", callback_data="publicar")],
    ]

    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "primer":
        estado[query.from_user.id] = "primer"
        await query.edit_message_text(
            "🍲 Отправьте первые блюда.\n\nКаждое блюдо с новой строки."
        )
        return

    if query.data == "segundo":
        estado[query.from_user.id] = "segundo"
        await query.edit_message_text(
            "🍛 Отправьте вторые блюда.\n\nКаждое блюдо с новой строки."
        )
        return

    if query.data == "postre":
        estado[query.from_user.id] = "postre"
        await query.edit_message_text(
            "🍰 Отправьте десерты.\n\nКаждый десерт с новой строки."
        )
        return

    if query.data == "publicar":
        await save_menu()
        await query.edit_message_text("✅ Меню опубликовано!")
    async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in estado:
        await update.message.reply_text(
            "Нажмите /start и выберите раздел меню."
        )
        return

    platos = [
        linea.strip()
        for linea in update.message.text.split("\n")
        if linea.strip()
    ]

    if estado[user_id] == "primer":
        menu["primerPlato"] = platos
        await update.message.reply_text("✅ Первые блюда сохранены.")

    elif estado[user_id] == "segundo":
        menu["segundoPlato"] = platos
        await update.message.reply_text("✅ Вторые блюда сохранены.")

    elif estado[user_id] == "postre":
        menu["postre"] = platos
        await update.message.reply_text("✅ Десерты сохранены.")

    del estado[user_id]
    async def save_menu():

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    file = repo.get_contents(FILE_PATH)

    data = json.loads(file.decoded_content.decode("utf-8"))

    data["menuDelDia"]["primerPlato"] = menu["primerPlato"]
    data["menuDelDia"]["segundoPlato"] = menu["segundoPlato"]
    data["menuDelDia"]["postre"] = menu["postre"]

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
        "Menú actualizado desde Telegram",
        json.dumps(data, ensure_ascii=False, indent=2),
        file.sha,
    )
    def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))

    print("✅ Bot Los Faroles запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
