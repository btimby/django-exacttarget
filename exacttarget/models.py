import json
import time
import requests

from django.db import models
from django.conf import settings

from exacttarget.api import PartnerAPI
from exacttarget.api import TOKEN_REFRESH_URL


class ExactTargetManager(models.Manager):
    def create(self, user, **kwargs):
        try:
            exacttarget = user.exacttarget
        except self.model.DoesNotExist:
            exacttarget = user.exacttarget = ExactTarget(user=user)
        for name, value in kwargs.items():
            setattr(exacttarget, name, value)
        exacttarget.save()
        return exacttarget


class ExactTarget(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    oauthToken = models.CharField(max_length=128, null=True)
    internalOauthToken = models.CharField(max_length=128, null=True)
    refreshToken = models.CharField(max_length=128, null=True)
    expiration = models.IntegerField()
    stackKey = models.CharField(max_length=2)

    objects = ExactTargetManager()

    def get_url(self):
        hostname = 'webservice.'
        if self.stackKey.lower() != 's1':
            hostname += self.stackKey + '.'
        return 'https://%sexacttarget.com/Service.asmx' % hostname

    def get_token(self, refresh=False):
        if refresh or time.time() + 300 > self.expiration:
            p = {
                'clientId' : settings.EXACTTARGET_CLIENT_ID,
                'clientSecret' : settings.EXACTTARGET_CLIENT_SECRET,
                'refreshToken' : self.refreshToken,
                'accessType': 'offline',
                'scope':'cas:'+ self.internalOauthToken,
            }
            r = requests.post(TOKEN_REFRESH_URL,
                              data=json.dumps(p),
                              headers={'content-type': 'application/json'}).json()
            self.oauthToken = r['accessToken']
            self.expiration = time.time() + r['expiresIn']
            self.internalOauthToken = r['legacyToken']
            self.refreshToken = r.get('refreshToken', self.refreshToken)
            self.save()
        return self.internalOauthToken

    def get_client(self):
        c = PartnerAPI(self.get_token(), url=self.get_url())
        # TODO: set auth info... reference:
        # https://github.com/btimby/django-exacttarget/blob/master/exacttarget/api.py#L17
        return c
