# bacalhau_apiclient.DefaultApi

All URIs are relative to *http://bootstrap.production.bacalhau.org:1234/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_serverapprover**](DefaultApi.md#api_serverapprover) | **GET** /approve | Approves a job to be run on this compute node.

# **api_serverapprover**
> str api_serverapprover()

Approves a job to be run on this compute node.

### Example
```python
from __future__ import print_function
import time
import bacalhau_apiclient
from bacalhau_apiclient.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = bacalhau_apiclient.DefaultApi()

try:
    # Approves a job to be run on this compute node.
    api_response = api_instance.api_serverapprover()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->api_serverapprover: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

