import os
import json
import logging
import base64
from github import Github
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --------------------------------------------------
# Настройка логирования
# --------------------------------------------------

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Переменные окружения Render
# --------------------------------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REPO_NAME = "veradana1993-gif/-Los-Faroles-Menu"
MENU_FILE = "menu.json"

# --------------------------------------------------
# Состояния ConversationHandler
# --------------------------------------------------

EDIT_PRICE = 1
EDIT_PRIMERO = 2
EDIT_SEGUNDO = 3
EDIT_POSTRE = 4

# --------------------------------------------------
# GitHub
# --------------------------------------------------

github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)

# --------------------------------------------------
# Загрузка menu.json
# --------------------------------------------------

def load_menu():

    try:

        with open(MENU_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:

        menu = {
            "menuDelDia": {
                "precio": "14 €",
                "primerPlato": "Gazpacho",
                "segundoPlato": "Paella",
                "bebida": "Bebida incluida",
                "postre": "Postre casero"
            }
        }

        save_local_menu(menu)

        return menu

# --------------------------------------------------
# Сохранение локально
# --------------------------------------------------

def save_local_menu(menu):

    with open(MENU_FILE, "w", encoding="utf-8") as file:
        json.dump(
            menu,
            file,
            indent=4,
            ensure_ascii=False,
        )

# --------------------------------------------------
# Загрузка в GitHub
# --------------------------------------------------

def upload_to_github(menu):

    content = json.dumps(
        menu,
        indent=4,
        ensure_ascii=False,
    )

    github_file = repo.get_contents(MENU_FILE)

    repo.update_file(
        github_file.path,
        "Actualizar menú",
        content,
        github_file.sha,
    )

# --------------------------------------------------
# Загружаем меню в память
# --------------------------------------------------

menu = load_menu()
# --------------------------------------------------
# Главное меню
# --------------------------------------------------

def main_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "🍽 Ver menú",
                callback_data="show_menu",
            )
        ],

        [
            InlineKeyboardButton(
                "✏️ Editar menú",
                callback_data="edit_menu",
            )
        ],

        [
            InlineKeyboardButton(
                "🌐 Abrir web",
                url="https://los-faroles-menu.onrender.com",
            )
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# --------------------------------------------------
# Команда /start
# --------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Bienvenido a Los Faroles\n\n"
        "Seleccione una opción:"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
    )


# --------------------------------------------------
# Показать меню
# --------------------------------------------------

async def show_menu(query):

    data = menu["menuDelDia"]

    text = (
        "🍽 MENÚ DEL DÍA\n\n"
        f"💶 Precio: {data['precio']}\n\n"
        f"🥗 Primero:\n{data['primerPlato']}\n\n"
        f"🍖 Segundo:\n{data['segundoPlato']}\n\n"
        f"🥤 {data['bebida']}\n\n"
        f"🍰 Postre:\n{data['postre']}"
    )

    await query.edit_message_text(
        text=text,
        reply_markup=main_keyboard(),
    )


# --------------------------------------------------
# Обработка кнопок
# --------------------------------------------------

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "show_menu":

        await show_menu(query)

        return

    if query.data == "edit_menu":

        await query.edit_message_text(
            "💶 Introduce el nuevo precio:"
        )

        return EDIT_PRICE
     # ==============================
# ОБРАБОТКА КНОПОК МЕНЮ
# ==============================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📋 Ver menú del día",
                callback_data="menu"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Reservar mesa",
                callback_data="reserva"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🍽️ Los Faroles\n\n¿Qué quieres hacer?",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "menu":

        try:

            with open(
                "menu.json",
                "r",
                encoding="utf-8"
            ) as file:

                menu = json.load(file)


            texto = (
                "🍽️ MENÚ DEL DÍA\n\n"
                f"🥗 Primero:\n{menu['primero']}\n\n"
                f"🍖 Segundo:\n{menu['segundo']}\n\n"
                f"🍰 Postre:\n{menu['postre']}\n\n"
                "🥤 Bebida incluida\n\n"
                "💶 Precio:\n"
                f"{menu['precio']}€"
            )


            await query.edit_message_text(texto)


        except Exception:

            await query.edit_message_text(
                "❌ No se pudo cargar el menú"
            )


    elif query.data == "reserva":

        await query.edit_message_text(
            "📞 Para reservar llama al restaurante."
        )
# ==============================
# COMANDOS Y ARRANQUE DEL BOT
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Bienvenido a Los Faroles\n\n"
        "🍽️ Para ver nuestro menú del día pulsa /menu"
    )


# ==============================
# CONFIGURACIÓN PRINCIPAL
# ==============================

def main():

    app = Application.builder().token(
        
8956988765:AAFtDe1IBjmTpfApW1JaljgSa2AdjmRLDVc
    ).build()


    # Comandos

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "menu",
            menu_command
        )
    )


    # Botones

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )


    print(
        "🤖 Bot Los Faroles iniciado..."
    )


    app.run_polling()



# ==============================
# EJECUTAR
# ==============================

if __name__ == "__main__":
    main()
