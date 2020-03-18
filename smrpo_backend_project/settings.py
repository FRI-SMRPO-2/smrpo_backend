from .common_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e+v!+_xrf@i#wld_u-!5u-3k-b=3j#t#^ju#vd=vv13#l^f3r!'

ALLOWED_HOSTS += ['127.0.0.1', '0.0.0.0', 'dev-smrpo']

BASE_URL = 'dev-smrpo:8000'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
