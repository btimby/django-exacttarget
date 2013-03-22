import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


__author__ = 'Arthur Rio'
__version__ = (0, 0, 8, 'beta')


# Setup default logging.
log = logging.getLogger('exacttarget')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)

if not hasattr(settings, 'EXACTTARGET_SOAP_WSDL_URL'):
    raise ImproperlyConfigured('The EXACTTARGET_SOAP_WSDL_URL setting is required.')

