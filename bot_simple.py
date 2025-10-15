"""
Bot de Telegram - Versión Simple para Pruebas
Este archivo es para probar el bot sin webhook, usando polling
"""
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración
BOT_TOKEN = "8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g"
WEB_APP_URL = "http://127.0.0.1:5000"  # Cambia esto por tu URL de ngrok cuando esté listo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start del bot"""
    user = update.effective_user
    message = (
        f"¡Hola {user.first_name}! 👋\n\n"
        "Bienvenido a tu bot personal.\n"
        "Usa el botón de abajo para abrir el panel de control:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎛️ Abrir Panel de Control", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)
    print(f"Usuario {user.first_name} ({user.id}) usó /start")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help del bot"""
    help_text = """
🤖 **Comandos disponibles:**

/start - Iniciar el bot y abrir panel de control
/help - Mostrar esta ayuda
/info - Información sobre el bot

📱 **Panel Web:**
Usa /start para acceder al panel de control web
    """
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /info del bot"""
    info_text = """
ℹ️ **Información del Bot**

Este es tu bot personal de Telegram con panel web.
Desarrollado con python-telegram-bot y Flask.

🌐 Panel web disponible en: http://127.0.0.1:5000
📡 Estado: Activo
    """
    await update.message.reply_text(info_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes que no son comandos"""
    await update.message.reply_text(
        "👋 ¡Hola! Usa /start para comenzar o /help para ver los comandos disponibles."
    )

def main():
    """Función principal"""
    print("🚀 Iniciando bot de Telegram...")
    
    # Crear la aplicación
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Añadir manejadores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    
    # Manejador para mensajes de texto que no son comandos
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot configurado correctamente")
    print(f"🌐 Panel web disponible en: {WEB_APP_URL}")
    print("📱 Inicia una conversación con tu bot en Telegram")
    print("🔄 Bot ejecutándose... (Ctrl+C para detener)")
    
    # Ejecutar el bot con polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()