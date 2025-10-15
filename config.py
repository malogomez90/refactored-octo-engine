# Configuración del Bot de Telegram
import os
from dotenv import load_dotenv

# Cargar variables de entorno (opcional)
load_dotenv()

# Token del bot (obtenido de @BotFather)
BOT_TOKEN = "8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g"

# Token secreto para verificar webhooks
TELEGRAM_SECRET_TOKEN = "mi-token-super-secreto-123"

# URL base de la aplicación web (se actualizará con ngrok)
WEB_APP_URL = "https://tu-enlace-de-ngrok.com"

# Configuración del servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

# Modo de desarrollo
DEBUG_MODE = True