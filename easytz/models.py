import pytz

from django.db import models
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
except AppRegistryNotReady:
    from django.contrib.auth.models import User


def get_default_timezone():
    """
    Gets the default timezone in settings or GMT
    """
    return getattr(settings, 'TIME_ZONE', 'GMT')


class TimezoneStore(models.Model):
    """
    Database storage for a users timezone
    """
    user = models.OneToOneField(User, related_name = 'timezone')

    # current max length of a tz is 30, going with 48 to be safe
    timezone = models.CharField(max_length = 48, default = get_default_timezone)

    def __unicode__(self):
        return self.timezone


def get_timezone_for_user(self):    
    """
    Magic method that provides attribute like access to getting a users
    timezone. Make sure to select_related on 'timezone'

    Example:
        my_user_object.tz
    """
    if getattr(self, '_timezone', None):
        return self._timezone

    try:
        tz = self.timezone
    except TimezoneStore.DoesNotExist:
        tz, created = TimezoneStore.objects.get_or_create(user = self)

    # cache the timezone object for this user
    self._timezone = tz.timezone

    return tz.timezone


def get_timezone_info_for_user(self):
    """
    Gets a users timezone as a tzinfo object
    """
    if getattr(self, '_timezone_info', None):
        return self._timezone_info

    self._timezone_info = pytz.timezone(self.tz)

    return self._timezone_info


User.add_to_class('tz', property(get_timezone_for_user))
User.add_to_class('tzinfo', property(get_timezone_info_for_user))
