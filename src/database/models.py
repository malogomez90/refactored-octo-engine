"""
Modelos de base de datos
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, BigInteger

db = SQLAlchemy()


class User(db.Model):
    """Modelo de usuario de Telegram"""
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True)  # Telegram User ID
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), nullable=True)
    is_bot = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.id}: {self.first_name}>'
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }


class Message(db.Model):
    """Modelo de mensaje"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger, nullable=False)  # Telegram Message ID
    user_id = Column(BigInteger, nullable=False)  # Telegram User ID
    chat_id = Column(BigInteger, nullable=False)  # Telegram Chat ID
    text = Column(Text, nullable=True)
    message_type = Column(String(50), default='text')  # text, photo, document, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}: {self.user_id}>'
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'message_id': self.message_id,
            'user_id': self.user_id,
            'chat_id': self.chat_id,
            'text': self.text,
            'message_type': self.message_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BotStats(db.Model):
    """Estadísticas del bot"""
    __tablename__ = 'bot_stats'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    commands_used = Column(Integer, default=0)
    
    def __repr__(self):
        return f'<BotStats {self.date.date()}: {self.total_users} users>'
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_users': self.total_users,
            'active_users': self.active_users,
            'total_messages': self.total_messages,
            'commands_used': self.commands_used
        }


def init_db(app):
    """Inicializar base de datos"""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada")


def get_or_create_user(user_data):
    """Obtener o crear usuario"""
    user = User.query.filter_by(id=user_data.id).first()
    
    if not user:
        user = User(
            id=user_data.id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            language_code=user_data.language_code,
            is_bot=user_data.is_bot
        )
        db.session.add(user)
    else:
        # Actualizar datos del usuario
        user.username = user_data.username
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.last_seen = datetime.utcnow()
    
    db.session.commit()
    return user


def log_message(update):
    """Registrar mensaje en base de datos"""
    if not update.message:
        return
    
    message = Message(
        message_id=update.message.message_id,
        user_id=update.effective_user.id,
        chat_id=update.effective_chat.id,
        text=update.message.text,
        message_type='text' if update.message.text else 'other'
    )
    
    db.session.add(message)
    db.session.commit()
    return message