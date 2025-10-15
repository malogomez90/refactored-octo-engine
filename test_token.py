"""
Verificar si el token del bot es válido
"""
import asyncio
from telegram import Bot

BOT_TOKEN = "8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g"

async def test_bot():
    try:
        bot = Bot(BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Token válido!")
        print(f"🤖 Nombre del bot: {me.first_name}")
        print(f"📱 Username: @{me.username}")
        print(f"🆔 ID: {me.id}")
        return True
    except Exception as e:
        print(f"❌ Error con el token: {e}")
        return False

if __name__ == '__main__':
    asyncio.run(test_bot())