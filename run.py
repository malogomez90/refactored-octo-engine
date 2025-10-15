"""
Punto de entrada principal de la aplicación
"""
import os
from dotenv import load_dotenv
from src.web.app import create_app, start_bot_background

# Cargar variables de entorno
load_dotenv()

# Crear aplicación
app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando Bot de Telegram Profesional...")
    
    # Iniciar bot en background
    start_bot_background()
    
    # Configuración del servidor
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🌐 Servidor web iniciado en: http://{host}:{port}")
    print(f"🤖 Bot de Telegram: @{os.getenv('BOT_USERNAME', 'antiviralbot')}")
    print(f"⚙️ Entorno: {'Desarrollo' if debug else 'Producción'}")
    print("-" * 60)
    
    # Ejecutar aplicación
    app.run(host=host, port=port, debug=debug)