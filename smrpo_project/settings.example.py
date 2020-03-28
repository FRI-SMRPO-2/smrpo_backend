from .common_settings import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "*b$)914m^gn@t@n$+#o!p%m=%)5*zq50gt-f+jp43ta06be04x"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'crm',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

ALLOWED_HOSTS += ['127.0.0.1', '0.0.0.0', 'dev-smrpo']

BASE_URL = 'dev-smrpo:8000'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

CORS_ORIGIN_ALLOW_ALL = True
