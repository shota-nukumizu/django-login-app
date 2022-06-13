# Django Sample Login Application

Djangoを使って認証アプリを実装した。

# 仕組み

`user1`(名前：`author`)：`leader`の役割を与えられて、app1~3までのアクセス権限を持つ

`user2`(名前：`nameless`)：`normal`の役割を与えられて、app1のみのアクセス権限を持つ

`user3`(名前：`shota`)：`super-advisor`の役割を与えられて、app2~3までのアクセス権限を持つ

# プログラムの中身

## `myapp/views.py`

```py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import SampleUser

def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            return render(request, 'login.html', {})

    return render(request, 'login.html',{})

@login_required
def index_func(request):
    return render(request, 'index.html', {})

# ここでuserモデルのプロパティroleの値に従って分類する
@login_required
def app1_func(request, pk):
    user = SampleUser.objects.get(pk=pk)
    if user.role != 'super-advisor':
        return render(request, 'app1.html', {})
    
    return render(request, 'index.html', {})

@login_required
def app2_func(request, pk):
    user = SampleUser.objects.get(pk=pk)
    if user.role != 'normal':
        return render(request, 'app2.html', {})
    
    return render(request, 'index.html', {})

@login_required()
def app3_func(request, pk):
    user = SampleUser.objects.get(pk=pk)
    if user.role != 'normal':
        return render(request, 'app3.html', {})

    return render(request, 'index.html', {})
```

## `myapp/models.py`

```py
from django.db import models
from django.contrib.auth.models import AbstractUser

LEADER = 1
SUPER_ADVISOR = 2
NORMAL = 3
ROLE_CHOICES = (
    (LEADER, 'leader'),
    (SUPER_ADVISOR, 'super-advisor'),
    (NORMAL, 'normal')
)

class SampleUser(AbstractUser):
    role = models.IntegerField(choices=ROLE_CHOICES, default=3)
```


## `myapp/urls.py`

```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_func, name='index'),
    path('login/', views.login_func, name='login'),
    path('app1/', views.app1_func, name='app1'),
    path('app2/', views.app2_func, name='app2'),
    path('app3/', views.app3_func, name='app3')
]
```

## `myapp/admin.py`

```py
from django.contrib import admin
from .models import SampleUser

admin.site.register(SampleUser)
```

## `backend/settings.py`

```py
"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-eafseljx%e(3en@841c!*zxacr)@z7&@@ak82n8x100p0#&rhi'

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
    'myapp',
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

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sampledb',
        'USER': 'author',
        'PASSWORD': '@Python2000',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


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

AUTH_USER_MODEL = 'myapp.SampleUser'


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
```

## `backend/urls.py`

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

## `manage.py`

```py
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pymysql

pymysql.install_as_MySQLdb()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

## `dump.json`

MySQLとの連携が終了した後、以下のコマンドで`dump.json`のデータをMySQLデータベースに移行する予定

```powershell
python manage.py loaddata dump.json
```

```json
[{"model": "admin.logentry", "pk": 1, "fields": {"action_time": "2022-06-13T03:42:56.984Z", "user": 1, "content_type": 6, "object_id": "2", "object_repr": "nameless", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 2, "fields": {"action_time": "2022-06-13T03:43:21.331Z", "user": 1, "content_type": 6, "object_id": "3", "object_repr": "shota", "action_flag": 1, "change_message": "[{\"added\": {}}]"}}, {"model": "admin.logentry", "pk": 3, "fields": {"action_time": "2022-06-13T03:43:29.378Z", "user": 1, "content_type": 6, "object_id": "1", "object_repr": "author", "action_flag": 2, "change_message": "[{\"changed\": {\"fields\": [\"Role\"]}}]"}}, {"model": "admin.logentry", "pk": 4, "fields": {"action_time": "2022-06-13T03:43:38.353Z", "user": 1, "content_type": 6, "object_id": "2", "object_repr": "nameless", "action_flag": 2, "change_message": "[{\"changed\": {\"fields\": [\"Role\"]}}]"}}, {"model": "admin.logentry", "pk": 5, "fields": {"action_time": "2022-06-13T03:43:44.231Z", "user": 1, "content_type": 6, "object_id": "1", "object_repr": "author", "action_flag": 2, "change_message": "[{\"changed\": {\"fields\": [\"Role\"]}}]"}}, {"model": "auth.permission", "pk": 1, "fields": {"name": "Can add log entry", "content_type": 1, "codename": "add_logentry"}}, {"model": "auth.permission", "pk": 2, "fields": {"name": "Can change log entry", "content_type": 1, "codename": "change_logentry"}}, {"model": "auth.permission", "pk": 3, "fields": {"name": "Can delete log entry", "content_type": 1, "codename": "delete_logentry"}}, {"model": "auth.permission", "pk": 4, "fields": {"name": "Can view log entry", "content_type": 1, "codename": "view_logentry"}}, {"model": "auth.permission", "pk": 5, "fields": {"name": "Can add permission", "content_type": 2, "codename": "add_permission"}}, {"model": "auth.permission", "pk": 6, "fields": {"name": "Can change permission", "content_type": 2, "codename": "change_permission"}}, {"model": "auth.permission", "pk": 7, "fields": {"name": "Can delete permission", "content_type": 2, "codename": "delete_permission"}}, {"model": "auth.permission", "pk": 8, "fields": {"name": "Can view permission", "content_type": 2, "codename": "view_permission"}}, {"model": "auth.permission", "pk": 9, "fields": {"name": "Can add group", "content_type": 3, "codename": "add_group"}}, {"model": "auth.permission", "pk": 10, "fields": {"name": "Can change group", "content_type": 3, "codename": "change_group"}}, {"model": "auth.permission", "pk": 11, "fields": {"name": "Can delete group", "content_type": 3, "codename": "delete_group"}}, {"model": "auth.permission", "pk": 12, "fields": {"name": "Can view group", "content_type": 3, "codename": "view_group"}}, {"model": "auth.permission", "pk": 13, "fields": {"name": "Can add content type", "content_type": 4, "codename": "add_contenttype"}}, {"model": "auth.permission", "pk": 14, "fields": {"name": "Can change content type", "content_type": 4, "codename": "change_contenttype"}}, {"model": "auth.permission", "pk": 15, "fields": {"name": "Can delete content type", "content_type": 4, "codename": "delete_contenttype"}}, {"model": "auth.permission", "pk": 16, "fields": {"name": "Can view content type", "content_type": 4, "codename": "view_contenttype"}}, {"model": "auth.permission", "pk": 17, "fields": {"name": "Can add session", "content_type": 5, "codename": "add_session"}}, {"model": "auth.permission", "pk": 18, "fields": {"name": "Can change session", "content_type": 5, "codename": "change_session"}}, {"model": "auth.permission", "pk": 19, "fields": {"name": "Can delete session", "content_type": 5, "codename": "delete_session"}}, {"model": "auth.permission", "pk": 20, "fields": {"name": "Can view session", "content_type": 5, "codename": "view_session"}}, {"model": "auth.permission", "pk": 21, "fields": {"name": "Can add user", "content_type": 6, "codename": "add_sampleuser"}}, {"model": "auth.permission", "pk": 22, "fields": {"name": "Can change user", "content_type": 6, "codename": "change_sampleuser"}}, {"model": "auth.permission", "pk": 23, "fields": {"name": "Can delete user", "content_type": 6, "codename": "delete_sampleuser"}}, {"model": "auth.permission", "pk": 24, "fields": {"name": "Can view user", "content_type": 6, "codename": "view_sampleuser"}}, {"model": "contenttypes.contenttype", "pk": 1, "fields": {"app_label": "admin", "model": "logentry"}}, {"model": "contenttypes.contenttype", "pk": 2, "fields": {"app_label": "auth", "model": "permission"}}, {"model": "contenttypes.contenttype", "pk": 3, "fields": {"app_label": "auth", "model": "group"}}, {"model": "contenttypes.contenttype", "pk": 4, "fields": {"app_label": "contenttypes", "model": "contenttype"}}, {"model": "contenttypes.contenttype", "pk": 5, "fields": {"app_label": "sessions", "model": "session"}}, {"model": "contenttypes.contenttype", "pk": 6, "fields": {"app_label": "myapp", "model": "sampleuser"}}, {"model": "sessions.session", "pk": "9xc093gjepo9we7w2q204zfaeahix9oi", "fields": {"session_data": ".eJxVjDsOwjAQRO_iGlle_BUlPWew1us1DiBHipMKcXccKQV0o3lv5i0ibmuNW-clTllcBIjTb5eQntx2kB_Y7rOkua3LlOSuyIN2eZszv66H-3dQsdexNqxDUeg8ZgjaJVcUsPUcrBttHggIRzbBmEIqeTqjI6UBrA9UtPh8Adw4N5A:1o0ayB:uX7mKRhw2PezZ7uqg0sacJ2S_cUmWGoJwZ_ryZ_WNiA", "expire_date": "2022-06-27T03:42:27.963Z"}}, {"model": "myapp.sampleuser", "pk": 1, "fields": {"password": "pbkdf2_sha256$320000$MyIDir1xmGO29nISywOFME$ID9hBQNL8xIOibKs2anW2KLbJaQbBxHiFY1RU4IUtdI=", "last_login": "2022-06-13T03:42:27Z", "is_superuser": true, "username": "author", "first_name": "", "last_name": "", "email": "", "is_staff": true, "is_active": true, "date_joined": "2022-06-13T03:41:48Z", "role": 2, "groups": [], "user_permissions": []}}, {"model": "myapp.sampleuser", "pk": 2, "fields": {"password": "%Sam2000", "last_login": null, "is_superuser": false, "username": "nameless", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2022-06-13T03:42:32Z", "role": 3, "groups": [], "user_permissions": []}}, {"model": "myapp.sampleuser", "pk": 3, "fields": {"password": "&Watt100", "last_login": null, "is_superuser": false, "username": "shota", "first_name": "", "last_name": "", "email": "", "is_staff": false, "is_active": true, "date_joined": "2022-06-13T03:42:57Z", "role": 3, "groups": [], "user_permissions": []}}]

```

# 開発環境

* Django 4.0.4
* MySQL 8.0.4
* Windows 11
* Visual Studio Code 1.68