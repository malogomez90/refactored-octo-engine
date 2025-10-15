import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Reemplaza 'TU_TOKEN_AQUI' con el token que te dio @BotFather
BOT_TOKEN = "TU_TOKEN_AQUI"

# La URL donde se ejecutará tu aplicación web localmente
# Por ahora usaremos localhost, más adelante veremos cómo hacerla pública
WEB_APP_URL = "http://127.0.0.1:5000"

async def start(update: Update, context: CallbackContext) -> None:
    """Se ejecuta cuando el usuario usa el comando /start."""
    keyboard = [
        [InlineKeyboardButton("Abrir Panel de Control", url=WEB_APP_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "¡Hola! Soy tu bot personal. Haz clic en el botón de abajo para abrir el panel de control.",
        reply_markup=reply_markup
    )

def main() -> None:
    """Función principal para ejecutar el bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Añadimos el manejador para el comando /start
    application.add_handler(CommandHandler("start", start))

    print("Bot de Telegram iniciado...")
    application.run_polling()

if __name__ == "__main__":
    main()
