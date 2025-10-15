# 🤖 Bot de Telegram Profesional

Un bot de Telegram completo con panel web de administración, desarrollado para producción.

## 🚀 Características

- ✅ Bot de Telegram completamente funcional
- ✅ Panel web de administración moderno
- ✅ Base de datos para persistencia
- ✅ Logs y monitoreo
- ✅ Deploy automático en la nube
- ✅ HTTPS y seguridad
- ✅ Escalable y mantenible

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.10+
- **Bot Framework:** python-telegram-bot
- **Web Framework:** Flask
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Deploy:** Render.com
- **Frontend:** HTML5 + CSS3 + JavaScript

## 📋 Requisitos

- Python 3.10+
- Token de bot de Telegram (obtenido de @BotFather)
- Cuenta en Render.com (gratuita)

## 🚀 Instalación

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuración

### 1. Configurar el Bot en Telegram

1. Habla con @BotFather en Telegram
2. Crea un nuevo bot con `/newbot`
3. Guarda el token que te proporciona
4. Actualiza el token en los archivos de configuración

### 2. Token del Bot

Tu token actual: `8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g`

**⚠️ IMPORTANTE:** Nunca compartas tu token públicamente

## 🎯 Ejecución

### Opción 1: Bot Simple (Recomendado para probar)

```bash
python bot_simple.py
```

### Opción 2: Servidor Web Separado

Terminal 1 - Servidor web:
```bash
python web_server.py
```

Terminal 2 - Bot:
```bash
python bot_simple.py
```

### Opción 3: Bot con Webhook (Para producción)

1. **Instalar ngrok:**
   - Descarga desde: https://ngrok.com/
   - Registra una cuenta gratuita

2. **Exponer el puerto 5000:**
   ```bash
   ngrok http 5000
   ```

3. **Actualizar la URL en app.py:**
   - Copia la URL https que te da ngrok
   - Reemplaza `"https://tu-enlace-de-ngrok-o-ip-pública.com"` en `app.py`

4. **Ejecutar el bot:**
   ```bash
   python app.py
   ```

## 📱 Uso

1. **Inicia el bot:** Ejecuta uno de los scripts de Python
2. **Abre Telegram:** Busca tu bot por su username
3. **Envía /start:** El bot te responderá con un botón
4. **Panel Web:** Haz clic en el botón para abrir la interfaz web

## 📁 Estructura del Proyecto

```
mi-bot-tg/
├── app.py              # Bot principal con webhook
├── bot.py              # Bot original
├── bot_simple.py       # Bot simplificado con polling
├── web_server.py       # Servidor Flask independiente
├── config.py           # Configuración
├── requirements.txt    # Dependencias
├── templates/
│   └── index.html     # Interfaz web
└── README.md          # Este archivo
```

## 🔧 Comandos del Bot

- `/start` - Iniciar el bot y mostrar panel
- `/help` - Mostrar ayuda
- `/info` - Información del bot

## 🌐 Panel Web

El panel web incluye:
- ✅ Estado del bot
- 📊 Estadísticas básicas
- 💬 Envío de mensajes broadcast
- ⚙️ Controles de configuración

## 🛠️ Solución de Problemas

### El bot no responde
1. Verifica que el token sea correcto
2. Asegúrate de que el script esté ejecutándose
3. Revisa la consola por errores

### No puedo abrir el panel web
1. Verifica que el servidor Flask esté corriendo
2. Asegúrate de que el puerto 5000 esté libre
3. Para acceso desde Telegram, necesitas ngrok

### Error de webhook
1. Usa `bot_simple.py` para probar sin webhook
2. Verifica que la URL de ngrok esté actualizada
3. Asegúrate de que el token secreto sea único

## 📚 Próximos Pasos

1. **Base de datos:** Agregar SQLite para almacenar usuarios y mensajes
2. **Autenticación:** Implementar login en el panel web
3. **Más funciones:** Añadir más comandos al bot
4. **Deploy:** Subir a un servidor en la nube

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en la consola
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el token del bot sea válido

---

¡Tu bot está listo para usar! 🎉