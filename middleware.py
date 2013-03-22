import simplejson
import urllib

from hashlib import md5

from django.core.cache import cache
from django.utils.cache import patch_vary_headers

from models import Profile

def combine(first, second):
    """
    Combines two profile objects, results in the most of both.
    """
    for (key, value) in first.items():
        if key in second:
            tmp = second[key]
            store = False
            try:
                tmp = int(tmp)
                if tmp:
                    store = True
            except ValueError:
                store = tmp
            if store:
                first[key] = store
    for (key, value) in second.items():
        tr
            value = int(value)
            if value:
                first[key] = True
        except ValueError:
            first[key] = value
        if key not in first:
            first[key] = False
    return first


class ProfileMiddleware():
    """
    Reads profile data from the cookie and the DB.
    """

    def process_request(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '')
        # Load from cache/DB based on user agent string
        key = 'profile::%s' % (md5(ua).hexdigest()) # Sanitise to avoid memcache warnings.
        server = cache.get(key)
        if server is None:
            try:
                server = Profile.objects.get(user_agent=ua)
            except Profile.DoesNotExist:
                server = Profile(user_agent=ua)
            cache.set(key, server)
        # Load data from the cookie
        cookie = request.COOKIES.get('profile', '{"profile": false}')
        cookie = urllib.unquote(cookie).decode('utf8')
        # Merge the cookie and server profile.
        client = simplejson.loads(cookie)
        merged = combine(server.profile, client)
        # If it's changed, sore to DB and cache.
        if merged != server.profile or not server.pk:
            server.profile = merged
            server.save()
            cache.set(key, server)
        # Make available on the request object.
        request.profile = server.profile

    def process_response(self, request, response):
        # Set the vary header for upstream caches.
        patch_vary_headers(response, ['User-Agent'])
        return response
