import os
import dj_database_url
from .base import *

SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)

DEBUG = os.getenv('DEBUG', 'False') == 'True'

allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '.vercel.app,127.0.0.1,localhost,*')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]

# Database configuration: uses DATABASE_URL environment variable if set (e.g. Postgres on Neon/Supabase),
# otherwise falls back to local db.sqlite3
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True') == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'

# Static files storage with WhiteNoise
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

