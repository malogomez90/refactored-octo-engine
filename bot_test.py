"""
Bot de Telegram - Versión de Prueba Local
Esta versión no usa WebApp para evitar problemas con HTTP
"""
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración
BOT_TOKEN = "8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start del bot"""
    user = update.effective_user
    message = (
        f"¡Hola {user.first_name}! 👋\n\n"
        "Bienvenido a tu bot personal.\n\n"
        "🎛️ **Panel de Control disponible en:**\n"
        "http://127.0.0.1:5000\n\n"
        "Para usar el panel:\n"
        "1. Abre otra terminal\n"
        "2. Ejecuta: python web_server.py\n"
        "3. Ve a la URL en tu navegador\n\n"
        "⚡ Para la versión completa con botón integrado, necesitas ngrok (HTTPS)"
    )
    
    # Botones simples sin WebApp
    keyboard = [
        [InlineKeyboardButton("ℹ️ Información", callback_data="info")],
        [InlineKeyboardButton("📊 Estado", callback_data="status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    print(f"Usuario {user.first_name} ({user.id}) usó /start")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los botones presionados"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "info":
        info_text = """
ℹ️ **Información del Bot**

🤖 Bot personal de Telegram
🌐 Panel web: http://127.0.0.1:5000
📡 Estado: ✅ Activo
🔧 Versión: 1.0

**Comandos:**
/start - Menú principal
/help - Ayuda
/panel - Link al panel web
        """
        await query.edit_message_text(info_text, parse_mode='Markdown')
    
    elif query.data == "status":
        status_text = """
📊 **Estado del Sistema**

✅ Bot: Funcionando
🌐 Servidor: Listo para iniciar
📱 Conexión: Estable
⚡ Uptime: Activo

Usa /panel para abrir el control web
        """
        await query.edit_message_text(status_text, parse_mode='Markdown')

async def panel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /panel para mostrar el link del panel"""
    panel_text = """
🎛️ **Panel de Control**

Para acceder al panel web:

1️⃣ **Abrir nueva terminal y ejecutar:**
   ```
   python web_server.py
   ```

2️⃣ **Abrir en el navegador:**
   http://127.0.0.1:5000

3️⃣ **Para acceso desde Telegram (requiere HTTPS):**
   - Instala ngrok: https://ngrok.com
   - Ejecuta: `ngrok http 5000`
   - Usa la URL HTTPS que te proporcione

🔗 Panel local: http://127.0.0.1:5000
    """
    await update.message.reply_text(panel_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help del bot"""
    help_text = """
🤖 **Comandos disponibles:**

/start - Menú principal del bot
/help - Mostrar esta ayuda
/info - Información detallada
/panel - Acceso al panel web
/ping - Verificar que el bot responde

📱 **Panel Web:**
Usa /panel para instrucciones de acceso

🚀 **Inicio rápido:**
1. Escribe /start
2. En otra terminal: python web_server.py
3. Ve a: http://127.0.0.1:5000
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /info del bot"""
    info_text = """
ℹ️ **Información Detallada**

🤖 **Bot de Telegram Personal**
- Versión: 1.0
- Framework: python-telegram-bot
- Servidor: Flask

🌐 **Panel Web**
- URL local: http://127.0.0.1:5000
- Funciones: Control, estadísticas, mensajes

⚙️ **Estado Actual**
- ✅ Bot: Activo
- 🔄 Modo: Polling (desarrollo)
- 📡 Conexión: Estable
    """
    await update.message.reply_text(info_text, parse_mode='Markdown')

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ping para verificar que el bot responde"""
    await update.message.reply_text("🏓 ¡Pong! El bot está funcionando correctamente ✅")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes que no son comandos"""
    message_text = update.message.text.lower()
    
    if 'hola' in message_text or 'hello' in message_text:
        await update.message.reply_text("👋 ¡Hola! Usa /start para ver el menú principal.")
    elif 'panel' in message_text or 'web' in message_text:
        await update.message.reply_text("🎛️ Usa /panel para acceder al panel de control.")
    elif 'ayuda' in message_text or 'help' in message_text:
        await update.message.reply_text("ℹ️ Usa /help para ver todos los comandos disponibles.")
    else:
        await update.message.reply_text(
            "👋 ¡Hola! Usa /start para comenzar o /help para ver los comandos disponibles."
        )

def main():
    """Función principal"""
    print("🚀 Iniciando bot de Telegram...")
    print(f"🔑 Token configurado: {BOT_TOKEN[:10]}...")
    
    # Crear la aplicación
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("panel", panel_command))
    application.add_handler(CommandHandler("ping", ping_command))
    
    # Manejador para botones
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Manejador para mensajes de texto que no son comandos
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot configurado correctamente")
    print("📱 Ve a Telegram y busca tu bot")
    print("💬 Envía /start para comenzar")
    print("🌐 Para el panel web, ejecuta en otra terminal: python web_server.py")
    print("🔄 Bot ejecutándose... (Ctrl+C para detener)")
    print("-" * 50)
    
    # Ejecutar el bot con polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()