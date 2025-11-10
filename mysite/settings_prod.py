from .settings import *
import os

# Production overrides
DEBUG = False

# Strong secret key: read from env when provided, otherwise use a long random default
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    # 64 hex chars
    'b0a3a3f6a7c2477991f1b2a1d6f3c0b4e7a9d2c1f5a6b7c8d9e0f1a2b3c4d5e6'
)

# Allow any host by default (adjust to your domain/IP for production)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Security headers and cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = 'same-origin'

# Whitenoise static files handling
MIDDLEWARE = list(MIDDLEWARE)
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    try:
        # Insert right after SecurityMiddleware
        idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
    except ValueError:
        idx = 0
    MIDDLEWARE.insert(idx, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure English-only in prod as well
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
]
