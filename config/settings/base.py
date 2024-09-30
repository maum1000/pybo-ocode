"""

Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/

"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

import os

# 미디어 파일 관련 설정
MEDIA_URL= 'media/'
MEDIA_ROOT =  os.path.join(BASE_DIR,'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'common.apps.CommonConfig', # common 앱을 추가 # CommonConfig 클래스를 추가
    'pybo.apps.PyboConfig', # pybo 앱을 추가 # PyboConfig 클래스를 추가
    'django.contrib.admin',
    'django.contrib.auth', # 장고의 인증 앱 로그인, 로그아웃, 회원가입 등의 기능을 제공
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # templates 디렉터리를 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'AI_Database',
        'USER': 'postgres',
        'PASSWORD': 'root1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


MAX_UPLOAD_SIZE = 5242880

ALLOWED_FILE_TYPES=[

    'image/jpeg',
    'image/png',
    'image/gif',
    'image2/jpeg',
    'image2/png',
    'image2/gif',

]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static', # static 디렉터리를 추가
]

# 로깅설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, # 만약 True로 설정하면 기존에 설정된 로거들을 사용하지 않게 된다.
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse', # DEBUG=False 인지를 확인하는 필터
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue', # DEBUG=True 인지를 확인하는 필터
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}', # 서버 로그 포맷, 서버 시간과 메시지를 출력
            'style': '{',
        },
        'standard': {
            # asctime - 현재 시간
            # levelname - 로그의 레벨(debug, info, warning, error, critical)
            # name - 로거명
            # message - 출력 내용
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        # 콘솔 출력 핸들러
        'console': {
            'level': 'INFO', # INFO 레벨 이상의 로그를 출력
            'filters': ['require_debug_true'], # DEBUG=True 일 때만 로그를 출력
            'class': 'logging.StreamHandler', # 콘솔 출력 핸들러
        },
        # 서버 로그 출력 핸들러
        'django.server': {
            'level': 'INFO', # INFO 레벨 이상의 로그를 출력
            'class': 'logging.StreamHandler', # 콘솔 출력 핸들러
            'formatter': 'django.server', # 서버 로그 포맷은 django.server로 설정
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO', # INFO 레벨 이상의 로그를 기록
            'filters': ['require_debug_false'], # DEBUG=False 일 때만 로그를 기록
            #class - 파일 핸들러로 RotatingFileHandler 사용, 
            # RotatingFileHandler는 파일 크기가 설정한 크기보다 커지면 파일 뒤에 인덱스를 붙여서 백업한다. 
            # 이 핸들러의 장점은 로그가 무한히 증가되더라도 일정 개수의 파일로 롤링(Rolling)되기 때문에 
            # 로그 파일이 너무 커져서 디스크가 꽉 차는 위험을 방지할 수 있다.
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/mysite.log', # 로그 파일명은 logs 디렉터리에 mysite.log로 설정
            'maxBytes': 1024*1024*5,  # 로그 파일의 최대 크기는 5MB로 설정
            'backupCount': 5, # 로그 파일의 개수는 5개로 설정
            'formatter': 'standard', # 로그 포맷은 standard로 설정
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'], # 콘솔, 이메일, 파일 핸들러를 사용
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'pybo': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}