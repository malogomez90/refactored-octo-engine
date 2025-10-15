"""
Bot de Telegram - Version Final Simplificada
Sin conflictos, con manejo de errores mejorado
"""
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token del bot
BOT_TOKEN = "8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g"

# Verificar si el bot está funcionando
async def test_bot_connection():
    """Probar la conexión con el bot"""
    try:
        from telegram import Bot
        bot = Bot(BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Bot conectado exitosamente: @{me.username}")
        return True
    except Exception as e:
        print(f"❌ Error conectando con el bot: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    try:
        user = update.effective_user
        welcome_message = f"""
🤖 ¡Bienvenido {user.first_name}!

Tu bot personal está funcionando correctamente.

🎛️ **Panel Web:** http://127.0.0.1:5000
(Asegúrate de que el servidor web esté ejecutándose)

¿Qué te gustaría hacer?
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Ver Estado", callback_data="status")],
            [InlineKeyboardButton("ℹ️ Información", callback_data="info")],
            [InlineKeyboardButton("🆘 Ayuda", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        logger.info(f"Usuario {user.first_name} ({user.id}) ejecutó /start")
        
    except Exception as e:
        logger.error(f"Error en comando start: {e}")
        await update.message.reply_text("❌ Hubo un error. Intenta de nuevo.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejar botones presionados"""
    try:
        query = update.callback_query
        await query.answer()  # Responder al callback
        
        if query.data == "status":
            status_msg = """
📊 **Estado del Sistema**

✅ Bot: Funcionando perfectamente
🌐 Panel Web: http://127.0.0.1:5000  
📱 Telegram: Conectado
🔄 Última actualización: Ahora

Todo está operativo! 🚀
            """
            await query.edit_message_text(status_msg)
            
        elif query.data == "info":
            info_msg = """
ℹ️ **Información del Bot**

🤖 **Tu Bot Personal de Telegram**
- Desarrollado con Python
- Framework: python-telegram-bot
- Panel Web: Flask
- Estado: ✅ Activo

🌐 **Panel de Control**
URL: http://127.0.0.1:5000

📱 **Comandos Disponibles**
/start - Menú principal
/help - Lista de ayuda
/ping - Verificar funcionamiento
/status - Estado del sistema
            """
            await query.edit_message_text(info_msg)
            
        elif query.data == "help":
            help_msg = """
🆘 **Ayuda y Comandos**

**Comandos básicos:**
• /start - Mostrar menú principal
• /help - Mostrar esta ayuda
• /ping - Verificar que el bot responde
• /status - Ver estado del sistema

**Panel Web:**
• Abre: http://127.0.0.1:5000
• Controla el bot desde el navegador
• Ve estadísticas y configuración

**¿Problemas?**
1. Verifica que el bot esté ejecutándose
2. Asegúrate de tener internet
3. Comprueba que el token sea correcto

¡Escribe cualquier mensaje para probar! 💬
            """
            await query.edit_message_text(help_msg)
            
    except Exception as e:
        logger.error(f"Error en button_handler: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help"""
    try:
        help_text = """
🆘 **Ayuda - Bot Personal**

**📱 Comandos disponibles:**
• /start - Menú principal con botones
• /help - Esta ayuda
• /ping - Verificar funcionamiento  
• /status - Estado del sistema

**🌐 Panel Web:**
• URL: http://127.0.0.1:5000
• Control completo del bot
• Estadísticas en tiempo real

**💬 Funciones:**
• Responde a cualquier mensaje
• Botones interactivos
• Panel de administración web

¡Prueba escribiendo cualquier cosa! ✨
        """
        await update.message.reply_text(help_text)
        logger.info(f"Usuario ejecutó /help")
        
    except Exception as e:
        logger.error(f"Error en help_command: {e}")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ping"""
    try:
        await update.message.reply_text("🏓 ¡Pong! El bot está funcionando perfectamente ✅")
        logger.info("Comando ping ejecutado")
    except Exception as e:
        logger.error(f"Error en ping_command: {e}")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /status"""
    try:
        import datetime
        now = datetime.datetime.now().strftime("%H:%M:%S")
        
        status_text = f"""
📊 **Estado del Sistema**

✅ **Bot:** Funcionando
🌐 **Panel Web:** http://127.0.0.1:5000
📡 **Conexión:** Estable
🕐 **Hora:** {now}
🤖 **Versión:** 1.0

**¿Todo bien?** ¡Sí! 🎉

Usa /start para ver el menú completo.
        """
        await update.message.reply_text(status_text)
        logger.info("Comando status ejecutado")
        
    except Exception as e:
        logger.error(f"Error en status_command: {e}")

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejar mensajes de texto que no son comandos"""
    try:
        user_message = update.message.text.lower()
        user_name = update.effective_user.first_name
        
        # Respuestas dinámicas
        if any(word in user_message for word in ['hola', 'hello', 'hi', 'hey']):
            response = f"👋 ¡Hola {user_name}! ¿Cómo estás? Usa /start para ver el menú principal."
            
        elif any(word in user_message for word in ['panel', 'web', 'interfaz']):
            response = "🌐 El panel web está en: http://127.0.0.1:5000\n\n¡Ábrelo en tu navegador para controlar el bot!"
            
        elif any(word in user_message for word in ['ayuda', 'help', 'auxilio']):
            response = "🆘 Usa /help para ver todos los comandos disponibles, o /start para el menú principal."
            
        elif any(word in user_message for word in ['estado', 'status', 'funciona']):
            response = "✅ ¡Todo funcionando perfectamente! Usa /status para más detalles."
            
        elif any(word in user_message for word in ['gracias', 'thanks', 'genial', 'perfecto']):
            response = f"😊 ¡De nada {user_name}! Estoy aquí para ayudarte. ¿Necesitas algo más?"
            
        else:
            response = f"💬 Hola {user_name}, recibí tu mensaje: \"{update.message.text}\"\n\n✨ Usa /start para ver todas las opciones disponibles."
        
        await update.message.reply_text(response)
        logger.info(f"Mensaje procesado de {user_name}: {user_message}")
        
    except Exception as e:
        logger.error(f"Error en handle_text_message: {e}")
        await update.message.reply_text("❌ Hubo un error procesando tu mensaje. Intenta de nuevo.")

def main() -> None:
    """Función principal"""
    print("🚀 Iniciando Bot de Telegram...")
    print(f"🔑 Verificando token: {BOT_TOKEN[:15]}...")
    
    try:
        # Crear la aplicación
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Añadir manejadores
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ping", ping_command))
        application.add_handler(CommandHandler("status", status_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
        
        print("✅ Bot configurado correctamente")
        print("📱 Ve a Telegram y busca tu bot")
        print("💬 Envía /start para comenzar")
        print("🌐 Panel web: http://127.0.0.1:5000")
        print("🔄 Ejecutándose... (Ctrl+C para detener)")
        print("-" * 60)
        
        # Ejecutar el bot
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("🔧 Verifica tu conexión a internet y el token del bot")

if __name__ == '__main__':
    main()