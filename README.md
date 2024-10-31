# Django Social Auth Package
    This is simple package for made social media 
    authentication with social media platforms.


### This package support authentication with : 
1. `Google`
2. `Facebook`
3. `Github`


## Installation

```
git clone https://github.com/RadwanHegazy/dj_social_auth
```

```
pip install -r requirements.txt
```

### Integerate package with the system

```python
# your_project/settings.py
# add package to installed apps

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # drf 
    "social_auth", # social auth package 
]


# Use JWT for authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ]
}

# the custom function you must set to save the user social media data in your user model
def custom_save_data(*args, **kwargs) : 
    from django.contrib.auth.models import User
    user = kwargs['user'] # the incomming user from the social platfrom
    u, _ = User.objects.get_or_create(
        username=user['email'].split('@')[0],
        email=user['email']
    )
    u.save()
    return u

# the same function but for github only
def github_save_data(*args, **kwargs) : 
    from django.contrib.auth.models import User
    user = kwargs['user'] # the incomming user from github
    u, _ = User.objects.get_or_create(
        username=user['login'],
    )
    u.save()
    return u

# NOTE: the return data type of the function must be User model, and must takses , *args and **kwargs as parametrs

SOCIAL_AUTH = {
    
    'google' : {
        'client_id' : "GOOGLE_CLIENT_ID",
        'client_secret' : "GOOGLE_CLIENT_SECRET",
        'redirect_url' : 'FRONTE_END_SERVER_REDIRECT_URL', # your frontend server
        'save_user_data' : custom_save_data
    },
    
    'facebook' : {
        'client_id' : "FB_CLIENT_ID",
        'client_secret' : "FB_CLIENT_SECRET",
        'redirect_url' : 'FRONTE_END_SERVER_REDIRECT_URL', # your frontend server,
        'save_user_data' : custom_save_data

    },

    'github' : {
        'client_id' : 'GITHUB_CLIENT_ID',
        'client_secret' : 'GITHUB_CLIENT_SECRET',
        'redirect_url' : 'FRONTE_END_SERVER_REDIRECT_URL', 
        'save_user_data' : github_save_data

    }

}

# NOTE: the redirect url must save in the social platform
```

### Include social auth urls

```
# your_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_auth.urls')),
]
```

### Run server and test
```
python manage.py runserver
```
