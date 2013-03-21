OVERVIEW
========

Interface with the [ExactTarget SOAP Api](http://help.exacttarget.com/en/technical_library/web_service_guide/working_with_soap_web_service_api/) for Django.  
Uses the [oauth authentication](https://code.exacttarget.com/devcenter/getting-started/hubexchange-apps/oauth-and-soap-api).

REQUIREMENTS
============

Python 2.7+  
Django 1.3+

INSTALLATION
============

1. Install the package

    ```shell
    pip install django-exacttarget
    ```

2. Add the module to your INSTALLED_APPS in you settings.py

    ```python
    INSTALLED_APPS = (
        ...
        'exacttarget',
        ...
    )
    ```

3. Set the wsdl url in your settings.py

    ```python
    EXACTTARGET_SOAP_WSDL_URL = "https://webservice.s6.exacttarget.com/etframework.wsdl"
    ```
    Note: _The url might be different depending on the type of your application._

USAGE
=====

#The client

```python
from exacttarget.client import PartnerAPI
api = PartnerAPI(internal_oauth_token)
print api.get_system_status()
```

Note: _You need to provide the internal\_oauth\_token you got from the [JWT information](https://code.exacttarget.com/devcenter/getting-started/hubexchange-apps).  
You can call any of the methods using the python syntax (i.e. ```VersionInfo()``` will be called using ```version_info()```)._

#The types

You can create an object of any type defined in the wsdl as follow:
```python
from exacttarget import types
# Standard object
list = types.List
# Enum object
list.Type = types.ListTypeEnum.Private
```

EXAMPLES
========

#Create a list

```python
from exacttarget import types, client

api = client.PartnerAPI(internal_oauth_token)
new_list = types.List
new_list.Description = "My description"
new_list.ListName = "My list name"
new_list.Type = types.ListTypeEnum.Private
new_list.ListClassification = types.ListClassificationEnum.ExactTargetList
co = types.CreateOptions
co.RequestType = types.RequestType.Synchronous
co.QueuePriority = types.Priority.Low

resp = api.create(co, [new_list])

print resp
```



