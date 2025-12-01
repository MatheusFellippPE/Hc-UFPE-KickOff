import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "1") == "1"

# Base from env, then extend with dev helpers when DEBUG
_env_hosts = [h for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h]
ALLOWED_HOSTS = _env_hosts.copy()
if DEBUG:
    ALLOWED_HOSTS += [
        '127.0.0.1',
        'localhost',
        '.ngrok.app',
        '.ngrok.io',
        '.ngrok-free.dev',
    ]

# CSRF trusted origins: use env or dev defaults
_env_csrf = [o for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o]
if _env_csrf:
    CSRF_TRUSTED_ORIGINS = _env_csrf
elif DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.ngrok.app',
        'https://*.ngrok.io',
        'https://*.ngrok-free.dev',
    ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "demands",  # novo app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve estáticos em produção
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # usar a pasta templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",  # acesso a STATIC_URL
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # cria/usa o arquivo db.sqlite3 na raiz do projeto
    },
    "demands": {  # segundo banco para demandas
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "demands.sqlite3",
    },
}

DATABASE_ROUTERS = ["demands.router.DemandsRouter"]  # roteia app demands para o banco 'demands'

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # usado por collectstatic em produção
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ALLOWED_HOSTS já vem de variável de ambiente; em produção defina ALLOWED_HOSTS="seu_dominio,localhost,127.0.0.1"

# CSRF/hosts for ngrok access
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    # allow any ngrok subdomain
    '.ngrok.app',
    '.ngrok.io',
    # optionally, add your exact ngrok host for stricter control
    # 'SEU-DOMINIO.ngrok.app',
    '.ngrok-free.dev',
]

CSRF_TRUSTED_ORIGINS = [
    # Django expects scheme here
    'https://*.ngrok.app',
    'https://*.ngrok.io',
    'https://*.ngrok-free.dev',
]

# behind ngrok (HTTPS), ensure Django recognizes forwarded protocol
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# secure cookies when served over https
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# if you need cross-site requests (e.g. different domain hitting your site), set to 'None'
# CSRF_COOKIE_SAMESITE = 'None'
# SESSION_COOKIE_SAMESITE = 'None'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"