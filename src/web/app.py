"""
Aplicación Web - Panel de Administración Profesional
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta
from src.config import get_config
from src.database.models import init_db, db, User, Message, BotStats
from src.bot.telegram_bot import telegram_bot
import asyncio
import threading


def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    
    # Configuración
    config_class = get_config()
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = config_class.get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    init_db(app)
    telegram_bot.init_app(app)
    
    # Rutas principales
    @app.route('/')
    def dashboard():
        """Dashboard principal"""
        try:
            # Estadísticas básicas
            total_users = User.query.count()
            active_users = User.query.filter_by(is_active=True).count()
            total_messages = Message.query.count()
            admin_users = User.query.filter_by(is_admin=True).count()
            
            # Usuarios recientes (últimos 7 días)
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_users = User.query.filter(User.created_at >= week_ago).count()
            
            # Mensajes recientes (últimos 7 días)
            recent_messages = Message.query.filter(Message.created_at >= week_ago).count()
            
            stats = {
                'total_users': total_users,
                'active_users': active_users,
                'total_messages': total_messages,
                'admin_users': admin_users,
                'recent_users': recent_users,
                'recent_messages': recent_messages,
                'avg_messages_per_user': round(total_messages / total_users, 1) if total_users > 0 else 0
            }
            
            return render_template('dashboard.html', stats=stats)
            
        except Exception as e:
            print(f"Error en dashboard: {e}")
            return render_template('dashboard.html', stats={})
    
    @app.route('/api/stats')
    def api_stats():
        """API de estadísticas"""
        try:
            total_users = User.query.count()
            active_users = User.query.filter_by(is_active=True).count()
            total_messages = Message.query.count()
            
            return jsonify({
                'success': True,
                'data': {
                    'total_users': total_users,
                    'active_users': active_users,
                    'total_messages': total_messages,
                    'timestamp': datetime.now().isoformat()
                }
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/users')
    def api_users():
        """API de usuarios"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            users = User.query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'success': True,
                'data': {
                    'users': [user.to_dict() for user in users.items],
                    'total': users.total,
                    'pages': users.pages,
                    'current_page': page
                }
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/messages')
    def api_messages():
        """API de mensajes"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            messages = Message.query.order_by(Message.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'success': True,
                'data': {
                    'messages': [msg.to_dict() for msg in messages.items],
                    'total': messages.total,
                    'pages': messages.pages,
                    'current_page': page
                }
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/broadcast', methods=['POST'])
    def api_broadcast():
        """API para enviar mensajes masivos"""
        try:
            data = request.get_json()
            message = data.get('message', '').strip()
            
            if not message:
                return jsonify({
                    'success': False,
                    'error': 'Mensaje no puede estar vacío'
                }), 400
            
            # Obtener usuarios activos
            active_users = User.query.filter_by(is_active=True).all()
            
            # Simular envío (en una implementación real, aquí llamarías al bot)
            # Por ahora solo devolvemos estadísticas simuladas
            
            return jsonify({
                'success': True,
                'data': {
                    'message': message,
                    'sent_to': len(active_users),
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/users')
    def users_page():
        """Página de gestión de usuarios"""
        return render_template('users.html')
    
    @app.route('/messages')
    def messages_page():
        """Página de mensajes"""
        return render_template('messages.html')
    
    @app.route('/settings')
    def settings_page():
        """Página de configuración"""
        config_info = {
            'bot_username': config_class.BOT_USERNAME,
            'environment': 'Producción' if config_class.is_production() else 'Desarrollo',
            'database': 'PostgreSQL' if 'postgres' in config_class.DATABASE_URL else 'SQLite',
            'webhook_url': config_class.WEBHOOK_URL or 'No configurado',
            'host': config_class.HOST,
            'port': config_class.PORT
        }
        return render_template('settings.html', config=config_info)
    
    @app.route('/health')
    def health_check():
        """Health check para el deploy"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0',
            'database': 'connected' if db else 'disconnected'
        })
    
    # Webhook para Telegram (si está configurado)
    if config_class.WEBHOOK_URL:
        @app.route(f'/webhook/{config_class.BOT_TOKEN}', methods=['POST'])
        def webhook():
            """Webhook de Telegram"""
            try:
                # Verificación de seguridad
                if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != config_class.WEBHOOK_SECRET:
                    return 'Unauthorized', 403
                
                # Procesar update de Telegram
                # Aquí iría la lógica del webhook
                return 'OK'
                
            except Exception as e:
                print(f"Error en webhook: {e}")
                return 'Error', 500
    
    return app


def run_bot_polling():
    """Ejecutar bot en modo polling (para desarrollo)"""
    if telegram_bot.application:
        print("🤖 Iniciando bot en modo polling...")
        telegram_bot.application.run_polling(drop_pending_updates=True)


def start_bot_background():
    """Iniciar bot en background"""
    telegram_bot.create_application()
    
    # En desarrollo, usar polling
    from src.config import Config
    if Config.is_development():
        bot_thread = threading.Thread(target=run_bot_polling, daemon=True)
        bot_thread.start()
        print("✅ Bot iniciado en background (polling)")
    else:
        print("✅ Bot configurado para webhook (producción)")


# Crear aplicación
app = create_app()

if __name__ == '__main__':
    # Iniciar bot en background
    start_bot_background()
    
    # Ejecutar aplicación Flask
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )