"""
Django settings for andhra_sweets project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# BASE DIR & ENV
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file (must be next to manage.py)
load_dotenv()

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = 'django-insecure-_vzmgiyr_+sw(8onijr_oc7)63^+tw79n=t((rs2n(y(tus#+e'
DEBUG = False
ALLOWED_HOSTS = ['andhrasruchulu.com','www.andhrasruchulu.com','72.61.244.174']

# Domains trusted for CSRF protection (forms, POST requests)
CSRF_TRUSTED_ORIGINS = ['https://andhrasruchulu.com', 'https://www.andhrasruchulu   .com']

# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'products',
    'cart',
    'orders',
    'users',
    'blog',
    'payments',
    'reviews',
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'andhra_sweets.urls'

# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'andhra_sweets.wsgi.application'

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# STATIC & MEDIA
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/andhrasruchulu/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/andhrasruchulu/media/'

# --------------------------------------------------
# AUTH
# --------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/users/register_view/'
LOGIN_REDIRECT_URL = '/cart/cart_page/'
AUTH_USER_MODEL = 'users.UserProfile'

# --------------------------------------------------
# EMAIL
# --------------------------------------------------
ADMIN_EMAIL = "sambasivaprasad345@gmail.com"
DEFAULT_FROM_EMAIL = "sambasivaprasad345@gmail.com"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sambasivaprasad345@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")

# --------------------------------------------------
# PAYMENT
# --------------------------------------------------
RAZORPAY_KEY_ID = "rzp_test_RtNLRHXgb1dBZQ"
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

# --------------------------------------------------
# FAST2SMS (FROM .env)
# --------------------------------------------------
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY")

# print("FAST2SMS_API_KEY =>", FAST2SMS_API_KEY)

