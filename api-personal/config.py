import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Render provee DATABASE_URL completa
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Fallback para desarrollo local
    if not DATABASE_URL:
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_NAME = os.getenv('DB_NAME', 'personal_postgres')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    PORT = int(os.getenv('PORT', 5000))