import jwt
import time

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

from exacttarget.models import ExactTarget


UserModel = get_user_model()


class ExactTargetBackend(object):
    """
    Handles ExactTarget SSO, using JWT.

    https://code.exacttarget.com/devcenter/getting-started/hubexchange-apps/sso
    """
    # TODO: build a django-exacttarget application to externalize this
    # authentication.
    supports_inactive_user = False

    def authenticate(self, **kwargs):
        payload = kwargs.get('jwt')
        if payload is None:
            return
        try:
            info = jwt.decode(payload, settings.EXACTTARGET_APP_SIGNATURE)
        except (AttributeError, KeyError):
            raise ImproperlyConfigured('Exacttarget app signature not defined '
                                       'in settings.EXACTTARGET_APP_SIGNATURE')
        except jwt.DecodeError:
            raise PermissionDenied('Invalid JWT')
        # Extract the user info, this is all we need.
        user_info = info['request']['user']
        # We have the user info, let's locate or create them!
        try:
            user = UserModel.objects.get(id=user_info['id'])
        except KeyError:
            raise PermissionDenied('Invalid JWT: missing email')
        except UserModel.DoesNotExist:
            user = UserModel.objects.create_user(user_info['id'], email=user_info['email'])
            user.set_unusable_password()
        # OAuth tokens need refreshed on each login.
        ExactTarget.objects.create(user,
                                   oauthToken=user_info['oauthToken'],
                                   internalOauthToken=user_info['internalOauthToken'],
                                   refreshToken=user_info['refreshToken'],
                                   stackKey=info['request']['organization']['stackKey'],
                                   expiration=time.time()+user_info['expiresIn'])
        return user

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            pass
