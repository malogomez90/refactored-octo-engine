"""
Servidor Flask para la interfaz web del bot
Ejecutar este archivo para iniciar solo el servidor web
"""
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal del panel de control"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """API para obtener estadísticas del bot"""
    # Aquí puedes conectar con una base de datos real
    stats = {
        'users': 10,
        'messages': 150,
        'status': 'active'
    }
    return jsonify(stats)

@app.route('/api/status')
def bot_status():
    """Verificar si el bot está activo"""
    return jsonify({
        'status': 'running',
        'message': 'Bot funcionando correctamente'
    })

if __name__ == '__main__':
    print("🌐 Iniciando servidor web...")
    print("📱 Panel disponible en: http://127.0.0.1:5000")
    print("🔄 Servidor ejecutándose... (Ctrl+C para detener)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)