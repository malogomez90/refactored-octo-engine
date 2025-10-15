"""
Bot de Telegram - Versión Profesional
"""
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    CallbackQueryHandler, ContextTypes, filters
)
from src.config import Config
from src.database.models import db, get_or_create_user, log_message, User, Message, BotStats

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """Clase principal del bot de Telegram"""
    
    def __init__(self, app=None):
        self.app = app
        self.application = None
        
    def init_app(self, app):
        """Inicializar bot con app de Flask"""
        self.app = app
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        try:
            user = update.effective_user
            
            # Registrar/actualizar usuario en DB
            db_user = get_or_create_user(user)
            log_message(update)
            
            welcome_message = f"""
🤖 ¡Bienvenido {user.first_name}!

Tu bot personal está funcionando en modo profesional.

🎛️ **Panel de Administración Web**
Accede a todas las funciones avanzadas desde el panel web.

📊 **Funciones disponibles:**
• Gestión de usuarios
• Estadísticas en tiempo real  
• Envío de mensajes masivos
• Configuración avanzada
• Logs y monitoreo

¿Qué te gustaría hacer?
            """
            
            # Determinar URL del panel web
            panel_url = Config.WEBHOOK_URL or "http://127.0.0.1:5000"
            
            keyboard = [
                [InlineKeyboardButton("🎛️ Panel Web", web_app=WebAppInfo(url=panel_url))],
                [InlineKeyboardButton("📊 Estadísticas", callback_data="stats")],
                [InlineKeyboardButton("ℹ️ Información", callback_data="info")],
                [InlineKeyboardButton("🆘 Ayuda", callback_data="help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
            logger.info(f"Usuario {user.first_name} ({user.id}) ejecutó /start")
            
        except Exception as e:
            logger.error(f"Error en start_command: {e}")
            await update.message.reply_text("❌ Error interno. Contacta al administrador.")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats - Solo para admins"""
        try:
            user_id = update.effective_user.id
            
            # Verificar si es admin
            if user_id not in Config.ADMIN_USER_IDS and Config.ADMIN_USER_IDS:
                await update.message.reply_text("❌ Comando solo para administradores.")
                return
            
            # Obtener estadísticas de la DB
            total_users = User.query.count()
            active_users = User.query.filter_by(is_active=True).count()
            total_messages = Message.query.count()
            
            stats_text = f"""
📊 **Estadísticas del Bot**

👥 **Usuarios:**
• Total: {total_users}
• Activos: {active_users}
• Administradores: {len(Config.ADMIN_USER_IDS)}

💬 **Mensajes:**
• Total recibidos: {total_messages}
• Promedio por usuario: {total_messages/total_users if total_users > 0 else 0:.1f}

🤖 **Bot:**
• Estado: ✅ Activo
• Modo: {'🚀 Producción' if Config.is_production() else '🔧 Desarrollo'}
• Última actualización: {datetime.now().strftime('%H:%M:%S')}

🌐 **Panel Web:** {Config.WEBHOOK_URL or 'http://127.0.0.1:5000'}
            """
            
            await update.message.reply_text(stats_text)
            logger.info(f"Admin {user_id} consultó estadísticas")
            
        except Exception as e:
            logger.error(f"Error en stats_command: {e}")
            await update.message.reply_text("❌ Error obteniendo estadísticas.")
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar botones"""
        try:
            query = update.callback_query
            await query.answer()
            
            if query.data == "stats":
                # Estadísticas públicas (limitadas)
                total_users = User.query.count()
                total_messages = Message.query.count()
                
                stats_msg = f"""
📊 **Estadísticas Públicas**

👥 Usuarios registrados: {total_users}
💬 Mensajes procesados: {total_messages}
🤖 Estado: ✅ Funcionando perfectamente
🕐 Última actualización: {datetime.now().strftime('%H:%M:%S')}

🌐 **Panel Web Disponible**
Usa el botón del menú principal para acceder.
                """
                await query.edit_message_text(stats_msg)
                
            elif query.data == "info":
                panel_url = Config.WEBHOOK_URL or "http://127.0.0.1:5000"
                info_msg = f"""
ℹ️ **Información del Bot**

🤖 **Bot Personal Profesional**
• Nombre: @{Config.BOT_USERNAME}
• Versión: 2.0 Professional
• Framework: python-telegram-bot
• Base de datos: {'PostgreSQL' if 'postgres' in Config.DATABASE_URL else 'SQLite'}

🌐 **Panel de Administración**
• URL: {panel_url}
• Funciones: Control total del bot
• Acceso: Desde Telegram o navegador

⚙️ **Características**
✅ Persistencia de datos
✅ Estadísticas avanzadas  
✅ Panel web responsivo
✅ Deploy profesional en la nube
✅ Logs y monitoreo
✅ Seguridad HTTPS

🚀 **Entorno:** {'Producción' if Config.is_production() else 'Desarrollo'}
                """
                await query.edit_message_text(info_msg)
                
            elif query.data == "help":
                help_msg = """
🆘 **Ayuda - Bot Profesional**

**👤 Comandos de Usuario:**
• /start - Menú principal
• /help - Esta ayuda
• /ping - Verificar funcionamiento

**👨‍💼 Comandos de Admin:**
• /stats - Estadísticas completas
• /broadcast - Mensaje masivo
• /users - Gestionar usuarios

**🌐 Panel Web:**
• Control completo del bot
• Estadísticas en tiempo real
• Gestión de usuarios
• Configuración avanzada
• Logs del sistema

**🔧 Funciones Avanzadas:**
• Base de datos persistente
• Respaldo automático
• Monitoreo 24/7
• Escalabilidad automática

**🚨 Soporte:**
Contacta a los administradores para ayuda técnica.
                """
                await query.edit_message_text(help_msg)
                
        except Exception as e:
            logger.error(f"Error en button_handler: {e}")
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enviar mensaje masivo - Solo admins"""
        try:
            user_id = update.effective_user.id
            
            if user_id not in Config.ADMIN_USER_IDS and Config.ADMIN_USER_IDS:
                await update.message.reply_text("❌ Comando solo para administradores.")
                return
            
            if not context.args:
                await update.message.reply_text("ℹ️ Uso: /broadcast <mensaje>")
                return
            
            message_text = " ".join(context.args)
            active_users = User.query.filter_by(is_active=True).all()
            
            sent_count = 0
            failed_count = 0
            
            await update.message.reply_text(f"📤 Enviando mensaje a {len(active_users)} usuarios...")
            
            for user in active_users:
                try:
                    await context.bot.send_message(chat_id=user.id, text=message_text)
                    sent_count += 1
                except Exception:
                    failed_count += 1
            
            result_msg = f"""
✅ **Broadcast Completado**

📤 Enviados: {sent_count}
❌ Fallidos: {failed_count}
📊 Total usuarios: {len(active_users)}

Mensaje: "{message_text[:50]}{'...' if len(message_text) > 50 else ''}"
            """
            
            await update.message.reply_text(result_msg)
            logger.info(f"Admin {user_id} envió broadcast: {sent_count} enviados, {failed_count} fallidos")
            
        except Exception as e:
            logger.error(f"Error en broadcast_command: {e}")
            await update.message.reply_text("❌ Error enviando broadcast.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        try:
            user = update.effective_user
            message_text = update.message.text.lower()
            
            # Registrar usuario y mensaje
            get_or_create_user(user)
            log_message(update)
            
            # Respuestas inteligentes
            if any(word in message_text for word in ['hola', 'hello', 'hi', 'hey']):
                response = f"👋 ¡Hola {user.first_name}! Usa /start para ver todas las opciones disponibles."
                
            elif any(word in message_text for word in ['panel', 'web', 'admin']):
                panel_url = Config.WEBHOOK_URL or "http://127.0.0.1:5000"
                response = f"🌐 Panel de administración: {panel_url}\n\n¡Úsalo para controlar completamente tu bot!"
                
            elif any(word in message_text for word in ['stats', 'estadisticas', 'números']):
                response = "📊 Usa /start y presiona 'Estadísticas' para ver los datos del bot."
                
            elif any(word in message_text for word in ['ayuda', 'help', 'auxilio']):
                response = "🆘 Usa /help para ver todos los comandos, o /start para el menú interactivo."
                
            else:
                response = f"💬 Mensaje recibido, {user.first_name}. Usa /start para ver todas las opciones disponibles del bot profesional."
            
            await update.message.reply_text(response)
            logger.info(f"Mensaje procesado de {user.first_name} ({user.id})")
            
        except Exception as e:
            logger.error(f"Error en handle_message: {e}")
            await update.message.reply_text("❌ Error procesando mensaje.")
    
    def setup_handlers(self):
        """Configurar manejadores del bot"""
        if not self.application:
            return
        
        # Comandos
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        
        # Botones
        self.application.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Mensajes
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        logger.info("✅ Manejadores del bot configurados")
    
    def create_application(self):
        """Crear aplicación del bot"""
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()
        return self.application


# Instancia global del bot
telegram_bot = TelegramBot()