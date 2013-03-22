import simplejson

from django.db import models

# Create your models here.

class Profile(models.Model):
    user_agent = models.CharField(max_length=255, db_index=True, unique=True)
    _profile = models.TextField(default='{}')

    def get_profile(self):
        if not self._profile:
            self._profile = '{}'
        return simplejson.loads(self._profile)

    def set_profile(self, data):
        if not data:
            data = {}
        self._profile = simplejson.dumps(data, sort_keys=True)

    profile = property(get_profile, set_profile)
