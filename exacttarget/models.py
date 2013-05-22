from django.db import models
from django.conf import settings

from exacttarget.api import PartnerAPI


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

    objects = ExactTargetManager()

    def get_client(self):
        c = PartnerAPI(self.internalOauthToken)
        # TODO: set auth info... reference:
        # https://github.com/btimby/django-exacttarget/blob/master/exacttarget/api.py#L17
        return c
