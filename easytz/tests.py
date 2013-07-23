from datetime import datetime
import pytz

from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from django.utils.importlib import import_module
from django.contrib.auth.models import User

from .middleware import TimezonesMiddleware

class TimezoneTestCase(TestCase):

    def get_request(self):
        """
        Get a fake request object that has some stuff we need on it
        """
        # probably a better way to do this, but the factory
        # doesnt return a request object with a session or user
        factory = RequestFactory()
        req = factory.get('/')
        engine = import_module(settings.SESSION_ENGINE)
        req.session = engine.SessionStore(None)
        req.user = AnonymousUser()

        return req

    def test_anonymous(self):
        """
        Testing Anonymous Cookie Based Users
        """

        request = self.get_request()

        # a fake manual way of testing the middleware out
        # this is just assuming setting our document.cookie worked
        # right from javascript
        mw = TimezonesMiddleware()
        
        request.COOKIES = {
            'timezone' : 'Australia/Victoria'
        }

        utcnow = datetime.utcnow().replace(tzinfo = pytz.utc)

        mw.process_request(request)
        now1 = timezone.localtime(timezone.now())
        
        request.COOKIES = {
            'timezone' : 'America/New_York'
        }      
     
        mw.process_request(request)
        now2 = timezone.localtime(timezone.now())

        # assertion time
        self.assertNotEqual(utcnow, now1)
        self.assertNotEqual(utcnow, now2)
        self.assertNotEqual(now1, now2)


    def test_authenticated(self):
        """
        Testing authenticated users with a session store
        and db storage
        """
        request = self.get_request()
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            
        # at this point, trying to access a users timezone should result
        # in it created one with them in the default
        default_tz = getattr(settings, 'TIME_ZONE', 'GMT')
        self.assertEqual(default_tz, user.tz)
        
        # replace our anonymous user with a real one
        request.user = user

        mw = TimezonesMiddleware()
    
        # still need a cookie to kick this party off        
        request.COOKIES = {
            'timezone' : 'Australia/Victoria'
        }

        # process our request
        mw.process_request(request)
        
        # our stored timezone should match what the cookie was
        stored_user = User.objects.get(username = 'john')
        self.assertEqual(stored_user.tz, request.COOKIES['timezone'])

        # our session store should also reflect the same
        self.assertEqual(request.session.get('timezone'), request.COOKIES['timezone'])
