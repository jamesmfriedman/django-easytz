Django EasyTZ
====================

Timezone localization without any thinking or doing whatsoever.

The purpose of this django app is to piggy back off of Django's already great timezone handling and add some automagic to the equation. This package is perfect for you if:

 - you don't care about accurate timezone names for your users (many timezones have the same UTC offset but have different names, I.E. America/Eastern and America/New_York)
 - you trust the time and timezone setting of the client's machine
 - you are using Django 1.4 or above

Setup
---------------------

 1. Use your favorite python package installer. `$ pip install django-easytz`
 2. Make sure `USE_TZ` is set to True in your settings file. This is Django's default since they introdcued timezone support in 1.4
 3. add `easytz.middleware.TimezonesMiddleware'` to your `MIDDLEWARE_CLASSES`
 4. add `easytz` to your `INSTALLED_APPS`
 5. include {{ STATIC_URL }}easytz/js/easytz.js with your scripts 
 6. Run `./manage.py syncdb` to add the model for storing users timezones

How It Works
----------------------

On the client side, jstz (http://pellepim.bitbucket.org/jstz/) is used to set a cookie with the users timezone. A middleware picks up the cookie and activates the timezone using Django's timezone handling. If a user is authenticated, it will also set the timezone in the session under a key called **timezone** as well as save it to the database.

Anytime you want to access a users timezone, you can do so by calling `my_user.tz`. This will get_or_create a timezone entry for the user. If there is no entry present, it defaults to what is set in `settings.TIME_ZONE` or **'GMT'**. From there, its up to you to use Django's built in handling. Django automatically converts aware datetimes that are used in templates. If you're in Django, just do the following

```Python
from django.utils import timezone

def foo(request):
	timezone.localtime(timezone.now(), request.user.tz)
	...
```

Model
----------------------
There is a simple storage model in `easytz.models.TimezoneStore` with the following fields:

 - **user**: OneToOne to the user
 - **timezone**: the current timezone string for that user

If you want to cut down on redundant queries, just make sure to select_related timezone if you are accessing the `.tz` property on users.

```Python
user = User.objects.select_related('timezone').get(user_id = 1)
users = User.objects.select_related('timezone').all()
```