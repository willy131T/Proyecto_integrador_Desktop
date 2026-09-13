import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

APP_NAME = os.getenv('APP_NAME', 'OdontoCloud Desktop')
APP_VERSION = '2.0.0'

# Base de datos: Si no se define DATABASE_URL, usa SQLite local como respaldo resiliente
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'consultorio_dental.db'}"
elif DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg://', 1)
elif DATABASE_URL.startswith('postgresql://') and not ('+' in DATABASE_URL.split('://')[0]):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

ASSETS_DIR = BASE_DIR / 'assets'
REPORTS_DIR = BASE_DIR / 'reportes'
REPORTS_DIR.mkdir(exist_ok=True)

THEME = {
    'primary': '#0284C7',
    'primary_hover': '#0369A1',
    'secondary': '#0D9488',
    'secondary_hover': '#0F766E',
    'accent': '#38BDF8',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'bg_dark': '#0F172A',
    'card_dark': '#1E293B',
    'card_light': '#FFFFFF',
    'text_dark': '#0F172A',
    'text_light': '#F8FAFC',
    'text_muted': '#94A3B8'
}
