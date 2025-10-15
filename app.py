import threading
from flask import Flask, request, abort, render_template
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURACIN ---
# Pega tu token del bot de BotFather aqu
BOT_TOKEN = "8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g" 
# El token de Telegram para verificar que las peticiones vienen de él
TELEGRAM_SECRET_TOKEN = "mi-token-super-secreto-123" # Token único para verificación

# --- INICIALIZACIN ---
app = Flask(__name__)
# El bot se inicializar dentro de la funcin main
application = None 
bot = None

# --- LGICA DEL BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envuelve el enlace a la pgina web cuando el usuario usa /start."""
    # Usamos ngrok o la IP local. ngrok es ms fcil para probar.
    # Asegrate de que este enlace sea accesible desde internet.
    web_url = "https://tu-enlace-de-ngrok-o-ip-pblica.com" 
    message = (
        f"Hola {update.effective_user.first_name}! 👋\n\n"
        "Pulsa el botn de abajo para abrir la interfaz de control:"
    )
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Abrir Panel de Control", web_app=WebAppInfo(url=web_url))]
    ]))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a cualquier otro mensaje."""
    await update.message.reply_text("Usa el comando /start para comenzar.")

# --- SERVIDOR WEB (FLASK) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return "El servidor del bot está funcionando!"

@app.route(f'/telegram/{BOT_TOKEN}', methods=['POST'])
def webhook():
    # Verificacin de seguridad para saber que la peticin viene de Telegram
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != TELEGRAM_SECRET_TOKEN:
        abort(403)
    
    # Procesa la actualizacin recibida
    update = Update.de_json(request.get_json(force=True), bot)
    application.create_task(application.process_update(update))
    
    return 'ok'

# --- FUNCIN PRINCIPAL ---
def main():
    global application, bot

    # 1. Crea la aplicacin del bot
    application = Application.builder().token(BOT_TOKEN).build()
    bot = application.bot

    # 2. Aade los manejadores de comandos y mensajes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 3. Inicia el bot en modo webhook
    # IMPORTANTE: Debes reemplazar la URL con la que te dé ngrok o tu IP pública
    webhook_url = f"https://tu-enlace-de-ngrok-o-ip-pública.com/telegram/{BOT_TOKEN}"
    
    # 4. Configura el webhook (esto se hará después con ngrok)
    # application.run_webhook(
    #     listen="0.0.0.0",
    #     port=5000,
    #     url_path=f"/telegram/{BOT_TOKEN}",
    #     webhook_url=webhook_url
    # )
    
    print("Bot configurado. Usa ngrok para exponer el puerto 5000 y luego configura el webhook.")
    print(f"URL del webhook: {webhook_url}")
    
    # Para desarrollo local, ejecuta Flask
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()