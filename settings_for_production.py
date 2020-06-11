from p7.settings_dev import *

DEBUG=False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = '/var/p7_static'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'p7',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
            'isolation_level': "repeatable read",
        },
        'CHARSET':'utf8',
        'COLLATION':'utf8_general_ci',
        'COLLATION_CONNECTION':'utf8_general_ci'
    }
}
