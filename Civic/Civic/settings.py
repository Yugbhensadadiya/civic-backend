import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ========================
# HOST SETTINGS
# ========================
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1,.onrender.com,.vercel.app'
    ).split(',')
    if h.strip()
]

# ========================
# PROXY FIX (IMPORTANT FOR RENDER)
# ========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True

# ========================
# SECURITY SETTINGS
# ========================
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# ========================
# INSTALLED APPS
# ========================
INSTALLED_APPS = [
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',

    'cloudinary',
    'cloudinary_storage',

    'accounts',
    'complaints',
    'departments',
    'officer',
    'dashboard',
    'contact_us',
    'Categories',
]

# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Civic.urls'
WSGI_APPLICATION = 'Civic.wsgi.application'

# ========================
# DATABASE (FIXED)
# ========================
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DEBUG and not DATABASE_URL:
    raise ImproperlyConfigured("DATABASE_URL is required in production")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

# ========================
# PASSWORD VALIDATION
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# STATIC FILES
# ========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ========================
# CLOUDINARY
# ========================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

# ========================
# CORS (FIXED)
# ========================
CORS_ALLOWED_ORIGINS = [
    "https://civic-frontend-three.vercel.app",
    "http://localhost:3000",
]

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True

# ========================
# CSRF (FIXED)
# ========================
CSRF_TRUSTED_ORIGINS = [
    "https://civic-frontend-three.vercel.app",
    "http://localhost:3000",
]

# ========================
# REST FRAMEWORK
# ========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ========================
# JWT
# ========================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ========================
# USER MODEL
# ========================
AUTH_USER_MODEL = 'accounts.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================
# GOOGLE OAUTH (FIXED 🔥)
# ========================
def clean(value):
    return value.strip().replace('"', '').replace("'", "")

GOOGLE_CLIENT_ID = clean(os.getenv("368010718950-hcafld60i8i3n95tf8o59h3cvfn525sq.apps.googleusercontent.com", ""))

# ========================
# EMAIL
# ========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'civictrack.civic@gmail.com'   # Your Gmail address
EMAIL_HOST_PASSWORD = 'psgrbqukbgzjobdk'  # Gmail App Password (not your login password)
DEFAULT_FROM_EMAIL = '<civictrack.civic@gmail.com>'  
