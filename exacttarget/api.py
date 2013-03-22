from django.conf import settings
from exacttarget import constants
from suds.client import Client
from suds.sax.element import Element
from suds.wsse import Security, UsernameToken

class PartnerAPI(object):
    """
    Interface of the SOAP Api reusing the client that has the wsdl file
    already loaded.

    Attributes:
        internal_oauth_token
    """
    def __init__(self, internal_oauth_token):
        self.client = Client(settings.EXACTTARGET_SOAP_WSDL_URL)
        # Add the default Security in the header
        security = Security()
        token = UsernameToken('*', '*')
        security.tokens.append(token)
        self.client.set_options(wsse=security)
        # Add oAuth token to SOAP header.
        ns = (None, constants.OAUTH_HEADER_URL)
        oauth_header = Element("oAuth", ns=ns)
        oauth_element = Element("oAuthToken")
        oauth_element.setText(internal_oauth_token)
        oauth_header.append(oauth_element)
        self.client.set_options(soapheaders=oauth_header)

        # Make easy the access to the types
        self.valid_types = []
        for valid_type in self.client.sd[0].types:
            self.valid_types.append(valid_type[0].name)

    def __getattribute__(self, name):
        if name != 'valid_types' and name in self.valid_types:
            # if the attribute is one of the Types
            return self.client.factory.create(name)
        else:
            return super(PartnerAPI, self).__getattribute__(name)

    def create(self, options, api_objects, request_id=None, overall_status=None):
        """
        """
        return self.client.service.Create(options, api_objects, request_id, overall_status)

    def get_system_status(self, options=None, overall_status=None, overall_status_message=None, request_id=None):
        """
        """
        return self.client.service.GetSystemStatus(options, overall_status, overall_status_message, request_id)

    def configure(self, options, action, configuration):
        """
        """
        return self.client.service.Configure(options, action, configuration)

    def delete(self, options, api_objects):
        """
        """
        return self.client.service.Delete(options, api_objects)

    def describe(self, describe_requests):
        """
        """
        return self.client.service.Describe(describe_requests)

    def execute(self, requests):
        """
        """
        return self.client.service.Execute(requests)

    def extract(self, requests):
        """
        """
        return self.client.service.Extract(requests)

    def perform(self, options, action, definitions):
        """
        """
        return self.client.service.Perform(options, action, definitions)

    def query(self, query_request):
        """
        """
        return self.client.service.Query(query_request)

    def retrieve(self, retrieve_request):
        """
        """
        return self.client.service.Retrieve(retrieve_request)

    def schedule(self, options, action, schedule, interactions):
        """
        """
        return self.client.service.Schedule(options, action, schedule, interactions)

    def update(self, options, api_objects):
        """
        """
        return self.client.service.Update(options, api_objects)

    def version_info(self, include_version_history):
        """
        """
        return self.client.service.VersionInfo(include_version_history)
