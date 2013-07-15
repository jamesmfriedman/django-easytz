from django.conf import settings
from django.utils import timezone
from pytz import UnknownTimeZoneError
from .models import TimezoneStore

class TimezonesMiddleware(object):
    def process_request(self, request):
        """
        Attempts to activate a timezone from a cookie or session
        """
        if getattr(settings, 'USE_TZ'):
            # check the cookie and the session
            tz = request.COOKIES.get('timezone')
            session_tz = request.session.get('timezone')
            tz = tz or session_tz

            if tz:
                try:
                    # attempt to activate the timezone. This might be an invalid
                    # timezone or none, so the rest of the logic following is coniditional
                    # on getting a valid timezone
                    timezone.activate(tz)
                    
                    # check to see if the session needs to be updated
                    if request.user.is_authenticated() and session_tz != tz:
                        request.session['timezone'] = tz
                        request.session.save()

                        # the session had to change, lets update the users database entry
                        # to be safe
                        tz_store, created = TimezoneStore.objects.get_or_create(user = request.user)
                        tz_store.timezone = tz
                        tz_store.save()

                except UnknownTimeZoneError:
                    pass
            else:
                timezone.deactivate()
