"""
Test Local - Verificar que todo funciona antes del deploy
"""
import os
import sys
import asyncio
import requests
from src.config import Config

def test_environment():
    """Test de variables de entorno"""
    print("🔧 Testing Environment Variables...")
    
    required_vars = ['BOT_TOKEN', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not getattr(Config, var, None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing variables: {missing_vars}")
        return False
    else:
        print("✅ All environment variables OK")
        return True

def test_bot_token():
    """Test de token del bot"""
    print("🤖 Testing Bot Token...")
    
    try:
        import asyncio
        from telegram import Bot
        
        async def check_bot():
            bot = Bot(Config.BOT_TOKEN)
            me = await bot.get_me()
            print(f"✅ Bot connected: @{me.username}")
            return True
        
        return asyncio.run(check_bot())
        
    except Exception as e:
        print(f"❌ Bot token error: {e}")
        return False

def test_database():
    """Test de base de datos"""
    print("💾 Testing Database...")
    
    try:
        from src.database.models import db, User
        from src.web.app import create_app
        
        app = create_app()
        with app.app_context():
            # Test create tables
            db.create_all()
            
            # Test query
            user_count = User.query.count()
            print(f"✅ Database connected, {user_count} users")
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_web_app():
    """Test de aplicación web"""
    print("🌐 Testing Web Application...")
    
    try:
        from src.web.app import create_app
        
        app = create_app()
        client = app.test_client()
        
        # Test health endpoint
        response = client.get('/health')
        if response.status_code == 200:
            print("✅ Web app healthy")
            return True
        else:
            print(f"❌ Web app error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Web app error: {e}")
        return False

def test_dependencies():
    """Test de dependencias"""
    print("📦 Testing Dependencies...")
    
    try:
        # Test imports críticos
        import flask
        import telegram
        import sqlalchemy
        import gunicorn
        
        print("✅ All dependencies installed")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 TESTING BOT BEFORE DEPLOY")
    print("=" * 40)
    
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies), 
        ("Bot Token", test_bot_token),
        ("Database", test_database),
        ("Web App", test_web_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
    
    print("=" * 40)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - READY FOR DEPLOY!")
        print("\n📋 Next steps:")
        print("1. Open: https://render.com/")
        print("2. Follow DEPLOY_NOW.md guide")
        print("3. Deploy your professional bot!")
        return True
    else:
        print("⚠️  Some tests failed - fix issues before deploy")
        return False

if __name__ == '__main__':
    main()