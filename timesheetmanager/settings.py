"""
Django settings for timesheetmanager project.

Generated by 'django-admin startproject' using Django 1.9.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from django.contrib import messages
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_CONFIGS = {
  'SECRET_KEY': os.getenv('SECRET_KEY','tdbcz%oo&hha2)z_=5&dk77=5025hayj1c86)y1(c)i!dexnr0'),
  'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', '*').split(','),
  'DEBUG': bool(os.getenv('DEBUG_MODE', 'True')),
  'STATIC_ROOT': os.getenv('STATIC_ROOT', os.path.join(BASE_DIR, 'static')),
  'DATABASE': {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE','django.db.backends.sqlite3'),
        'NAME': os.getenv('DATABASE_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
      	'HOST': os.getenv('DATABASE_HOST', None),
        'USER': os.getenv('DATABASE_USER', None),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', None),
        'CHARSET': os.getenv('DATABASE_CHARSET', 'UTF-8'),
        'ATOMIC_REQUESTS': os.getenv('DATABASE_ATOMICREQUESTS','False'),
    },
  },
}

try:
    from .__secretsettings import CONFIGS as NEW_ENV_CONFIGS
    ENV_CONFIGS = NEW_ENV_CONFIGS
except:
    print("Module __secretsettings not found, loading defaults")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_CONFIGS["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_CONFIGS["DEBUG"]

ALLOWED_HOSTS = ENV_CONFIGS["ALLOWED_HOSTS"]

LOGIN_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/user/"


# Application definition

INSTALLED_APPS = [
	'base.apps.BaseConfig',
	'materialdesign.apps.MaterialdesignConfig',
	'user.apps.UserConfig',
	'history.apps.HistoryConfig',
	'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

ROOT_URLCONF = 'timesheetmanager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
				'base.apps.request_current_site',
				'base.apps.request_available_sites',
				'base.apps.mapped_languages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

WSGI_APPLICATION = 'timesheetmanager.wsgi.application'

LOGGER_FILES_ROOT = os.path.join(BASE_DIR, 'log')

os.makedirs(LOGGER_FILES_ROOT, exist_ok = True)

LOGGER_FILES = {

	'console.debug':  os.path.join(LOGGER_FILES_ROOT, '_debug.log'),
	'console.info':  os.path.join(LOGGER_FILES_ROOT, '_info.log'),
	'console.warning':  os.path.join(LOGGER_FILES_ROOT, '_warning.log'),
	'console.error':  os.path.join(LOGGER_FILES_ROOT, '_error.log'),
	'console.critical':  os.path.join(LOGGER_FILES_ROOT, '_critical.log'),


	'django.debug': os.path.join(LOGGER_FILES_ROOT, 'django.debug.log'),
	'django.info': os.path.join(LOGGER_FILES_ROOT, 'django.info.log'),
	'django.warning': os.path.join(LOGGER_FILES_ROOT, 'django.warning.log'),
	'django.error': os.path.join(LOGGER_FILES_ROOT, 'django.error.log'),
	'django.critical': os.path.join(LOGGER_FILES_ROOT, 'django.critical.log'),

}

for key in LOGGER_FILES:
	if not os.path.exists(LOGGER_FILES[key]):
		with open(LOGGER_FILES[key], "w") as lf:
			lf.write("")

LOGGING = {
	'version': 1,
	"disable_existing_loggers": False,
	'formatters': {
        'log': {
            'format': '%(asctime)s: [%(levelname)s] (M: %(module)s) (P: %(process)d) (T: %(thread)d) - %(message)s'
        },
    },
	'handlers': {

		'console': {
			'formatter': 'log',
		    'class': 'logging.StreamHandler',
		},

		'console.info': {
			'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['console.info'],
		    'level': 'INFO',
		},

		'console.debug': {
			'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['console.debug'],
		    'level': 'DEBUG',
		},

		'console.warning': {
			'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['console.warning'],
		    'level': 'WARNING',
		},
		'console.error': {
			'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['console.error'],
		    'level': 'ERROR',
		},
		'console.critical': {
			'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['console.critical'],
		    'level': 'CRITICAL',
		},

		'django.debug': {
		    'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['django.debug'],
		    'level': 'DEBUG',
		},
		'django.info': {
		    'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['django.info'],
		    'level': 'INFO',
		},
		'django.warning': {
		    'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['django.warning'],
		    'level': 'WARNING',
		},
		'django.error': {
		    'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['django.error'],
		    'level': 'ERROR',
		},
		'django.critical': {
		    'formatter': 'log',
		    'class': 'logging.FileHandler',
		    'filename': LOGGER_FILES['django.critical'],
		    'level': 'CRITICAL',
		},

    },
    'loggers': {
		'main': {
            'handlers': ['console', 'console.debug', 'console.info', 'console.warning', 'console.error', 'console.critical'],
        },
        'django': {
            'handlers': ['django.debug', 'django.info', 'django.warning', 'django.error', 'django.critical'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
__postgresql = {
	'ENGINE': 'django.db.backends.postgresql',
   'HOST': os.getenv('DJANGO_DATABASE_HOST', 'localhost'),
	'NAME': os.getenv('DJANGO_DATABASE_NAME', 'productivenv_db'),
	'USER': os.getenv('DJANGO_DATABASE_USER', 'productivenv'),
	'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD', 'rEdK-kcNUcNsAAIH18eV6ZqOoE'),
	'CHARSET': 'UTF-8',
	'ATOMIC_REQUESTS': True
}

DATABASES = ENV_CONFIGS["DATABASE"]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'translations'),
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ENV_CONFIGS["STATIC_ROOT"]

if DEBUG:
	DJANGO_LOG_LEVEL = DEBUG
