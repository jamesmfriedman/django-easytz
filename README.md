Django Timezones
====================

Timezone localization without any thinking or doing whatsoever.

The purpose of this django app is to piggy back off of Django's already great timezone handling and add some automagic to the equation. This package is perfect for you if:

 - you don't care about accurate timezone names for your users (many timezones have the same UTC offset but have different names, I.E. America/Eastern and America/New_York)
 - you trust the time and timezone setting of the client's machine
 - you are using Django 1.4 or above

Setup
---------------------

 1. Make sure `USE_TZ` is set to True in your settings file. This is Django's default since they introdcued timezone support in 1.4
 2. add `timezones.middleware.TimezonesMiddleware'` to your `MIDDLEWARE_CLASSES`
 3. add `timezones` to your `INSTALLED_APPS`
 4. include {{ STATIC_URL }}timezones/js/timezones.js with your scripts 

How It Works
----------------------