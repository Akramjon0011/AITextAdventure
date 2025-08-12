import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///uzbek_news.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your-gemini-key')
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'your-telegram-token')
    TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID', '@your_channel')
    
    # Site Settings
    SITE_NAME = os.environ.get('SITE_NAME', 'UzbekNews AI')
    SITE_DESCRIPTION = os.environ.get('SITE_DESCRIPTION', 'O\'zbekiston va Markaziy Osiyodagi eng so\'nggi yangiliklarni AI yordamida taqdim etamiz')
    
    # Uzbek Categories
    UZBEK_CATEGORIES = [
        'O\'zbekiston yangiliklar',
        'Texnologiya', 
        'Iqtisodiyot',
        'Sport',
        'Madaniyat',
        'Ta\'lim',
        'Sog\'liqni saqlash',
        'Markaziy Osiyodagi yangiliklar',
        'Jahon yangiliklar'
    ]
    
    # Uzbek Regions
    UZBEK_REGIONS = [
        'Toshkent',
        'Samarqand',
        'Buxoro',
        'Andijon',
        'Farg\'ona',
        'Namangan',
        'Qashqadaryo',
        'Surxondaryo',
        'Xorazm',
        'Navoiy',
        'Jizzax',
        'Sirdaryo',
        'Qoraqalpog\'iston'
    ]
