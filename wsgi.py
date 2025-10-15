"""
Script de inicialización para producción
"""
import os
from src.web.app import create_app
from src.database.models import init_db

# Crear aplicación para producción
app = create_app()

# Inicializar base de datos
with app.app_context():
    from src.database.models import db
    db.create_all()
    print("✅ Base de datos inicializada para producción")

if __name__ != '__main__':
    # Para gunicorn
    import sys
    sys.path.insert(0, os.path.dirname(__file__))