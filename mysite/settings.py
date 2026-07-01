from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# SECURITY  — all secrets come from environment variables, never hardcoded
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-change-in-production")

# DEBUG: default False so a misconfigured server never leaks stack traces.
# Set DEBUG=True in .env only during local development.
DEBUG = os.getenv("DEBUG", "False").strip().lower() == "true"

# ALLOWED_HOSTS: comma-separated in .env, e.g. "SERVER_IP,yourdomain.com"
_raw_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

# ---------------------------------------------------------------------------
# JWT  — used by middleware.py (reads settings.JWT_SECRET_KEY)
# ---------------------------------------------------------------------------
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-to-a-long-random-secret-in-production",
)

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coreapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise — serves staticfiles directly from gunicorn (no nginx needed)
    # Must come directly after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # JWT role-based access middleware (no DB / ORM needed)
    'coreapp.middleware.RoleBasedAccessMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# ---------------------------------------------------------------------------
# Database
# Django's own internal DB (used for admin, auth, migrations tracking).
# The application's SQL Server data is accessed directly via pyodbc in
# dataaccess.py — it does NOT go through Django ORM.
# SQLite is fine for Django internals during the deferred-DB phase.
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files  (CSS, JS, images)
# WhiteNoise compresses and serves them directly — no separate nginx needed.
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'

# Where collectstatic puts everything (run once via entrypoint.sh at container start)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional directories beyond each app's /static/ folder
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# WhiteNoise: cache static files forever (they get a hash in the URL)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------------------------------------------------------
# Media files  (user uploads — expense receipts, documents)
# The host directory C:\deployments\media is bind-mounted to /app/media.
# Files written here survive container restarts.
# ---------------------------------------------------------------------------
MEDIA_URL = '/media/'

# Inside the container the bind-mount lands at /app/media.
# Override via MEDIA_ROOT env var if your layout differs.
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", str(BASE_DIR / "media")))

# Max upload size: 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ---------------------------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
