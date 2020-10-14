from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('PGSQL_DB_NAME'),
        'USER': get_env_variable('PGSQL_DB_USER'),
        'PASSWORD': get_env_variable('PGSQL_DB_PASW'),
        'HOST': get_env_variable('PGSQL_DB_HOST'),
        'PORT': get_env_variable('PGSQL_DB_PORT'),
    }
}
# Dev email settings, enables email output to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'contact@superlist.com'
DEFAULT_FROM_EMAIL = 'no     reply@superlist.com'
EMAIL_SUBJECT_PREFIX = '[Superlist Login]'
MANAGERS = (
    ('Us', 'ourselves@superlist.com'),
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
    'root': {'level': 'INFO'},
}
