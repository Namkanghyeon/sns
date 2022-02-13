from pathlib import Path
import os
import my_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x&j#c6t*(j)b)i!aaf^r362cu4oqv3-ljdn$4_^f!mhu=&jy(0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    '.ap-northeast-2.compute.amazonaws.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # aws S3용
    # 생성한 app들은 여기에 추가해줘야 나중에 모델을 db로 migration할 때 자동으로 해줌
    'sns',
    'content',
    'user',
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

ROOT_URLCONF = 'sns.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'sns.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Database 설정 => my_setttings.py 파일에
DATABASES = my_settings.DATABASES

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------- 커스텀 ----------

# 커스텀 유저 모델 사용
AUTH_USER_MODEL = 'user.User'

# 브라우저 닫으면 세션 정보 삭제
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 세션 타임아웃
# SESSION_COOKIE_AGE = 1200
# SESSION_SAVE_EVERY_REQUEST = True

# # aws S3 설정 => my_settings.py 파일에
AWS_ACCESS_KEY_ID = my_settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = my_settings.AWS_SECRET_ACCESS_KEY
AWS_S3_REGION_NAME = my_settings.AWS_S3_REGION_NAME
AWS_STORAGE_BUCKET_NAME = my_settings.AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = my_settings.AWS_S3_CUSTOM_DOMAIN
AWS_DEFAULT_ACL = my_settings.AWS_DEFAULT_ACL

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# # STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 각 media 파일에 대한 URL Prefix
# MEDIA_URL = '/media/'  # 항상 /로 끝나도록 설정

# 업로드된 파일을 저장할 디렉토리 경로
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
