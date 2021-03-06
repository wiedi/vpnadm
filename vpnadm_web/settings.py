"""
Django settings for vpnadm_web project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fz3hk%5z@g206=gjve&jvys6e*amj%oa^=%5-+26fc7q$x3y-a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'bootstrap3',
	'staffpanel',
	'vpnadm',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vpnadm_web.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'templates'),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'vpnadm_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# allow db dir to be overwritten
DB_DIR = BASE_DIR

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(DB_DIR, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR + '/static/',]
STATIC_ROOT = BASE_DIR + '/static-public/'


# VPNADM Settings

## CA Defaults

CA_LIFETIME_IN_DAYS = 360 * 100
CA_CN = 'VPN CA'
CA_O  = 'O'
CA_OU = 'OU'
CA_L  = 'L'
CA_ST = 'ST'
CA_C  = 'UN'
DH_KEYSIZE = '4096'

CERT_LIFETIME_IN_DAYS = 360 * 50

OPENVPN_PATH = '/opt/local/etc/openvpn'
OPENVPN_PROTO           = 'udp'
OPENVPN_SERVER_PORT     = 1194
OPENVPN_HOSTNAME        = 'vpn.example.com'
OPENVPN_MANAGEMENT_SOCKET = OPENVPN_PATH + '/manage.sock'

MANAGE_COMMAND = '/opt/local/bin/python /opt/vpnadm/manage.py'

