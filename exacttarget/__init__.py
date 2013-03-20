import logging
from suds.client import Client
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from exacttarget.constants import VALID_TYPE_URL


__author__ = 'Arthur Rio'
__version__ = (0, 0, 1, 'beta')


# Setup default logging.
log = logging.getLogger('exacttarget')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)


if not hasattr(settings, 'EXACTTARGET_SOAP_WSDL_URL'):
    raise ImproperlyConfigured('The EXACTTARGET_SOAP_WSDL_URL setting is required.')

# load the wsdl file
client = Client(settings.EXACTTARGET_SOAP_WSDL_URL)

class ExacttargetTypes(object):
    '''
    Utility class to create objects from the server only once and then use a copy instead.
    '''
    def __init__(self):
        # Instanciates the types from the wsdl
        self.valid_types = []
        for s in client.wsdl.types[0].schema().elements:
            if VALID_TYPE_URL == s[1]:
                self.valid_types.append(s[0])
    def __getattribute__(self, name):
        try:
            ret = super(ExacttargetTypes, self).__getattribute__(name)
        except AttributeError as e:
            if name in self.valid_types:
                # Creates the first instance of the Type onlt once
                ret = client.factory.create(name)
                self.__setattr__(name, ret)
            else:
                raise e
        if name != 'valid_types' and name in self.valid_types:
            from copy import deepcopy
            # if the attribute is one of the Types
            return deepcopy(ret)
        else:
            return ret

types = ExacttargetTypes()
