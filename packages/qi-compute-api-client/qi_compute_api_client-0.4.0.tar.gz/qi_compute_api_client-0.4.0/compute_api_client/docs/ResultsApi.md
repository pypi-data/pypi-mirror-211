# compute_api_client.ResultsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_result_results_post**](ResultsApi.md#create_result_results_post) | **POST** /results | Create result
[**read_result_results_id_get**](ResultsApi.md#read_result_results_id_get) | **GET** /results/{id} | Retrieve result
[**read_results_by_run_id_results_run_run_id_get**](ResultsApi.md#read_results_by_run_id_results_run_run_id_get) | **GET** /results/run/{run_id} | Retrieve result


# **create_result_results_post**
> Result create_result_results_post(result_in)

Create result

Create new result.

### Example

* Api Key Authentication (runtime):
```python
from __future__ import print_function
import time
import compute_api_client
from compute_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: runtime
configuration.api_key['runtime'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['runtime'] = 'Bearer'

# Configure API key authorization: user
configuration.api_key['user'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.ResultsApi(api_client)
    result_in = compute_api_client.ResultIn() # ResultIn | 

    try:
        # Create result
        api_response = api_instance.create_result_results_post(result_in)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ResultsApi->create_result_results_post: %s\n" % e)
```

* Api Key Authentication (user):
```python
from __future__ import print_function
import time
import compute_api_client
from compute_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: runtime
configuration.api_key['runtime'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['runtime'] = 'Bearer'

# Configure API key authorization: user
configuration.api_key['user'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.ResultsApi(api_client)
    result_in = compute_api_client.ResultIn() # ResultIn | 

    try:
        # Create result
        api_response = api_instance.create_result_results_post(result_in)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ResultsApi->create_result_results_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result_in** | [**ResultIn**](ResultIn.md)|  | 

### Return type

[**Result**](Result.md)

### Authorization

[runtime](../README.md#runtime), [user](../README.md#user)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_result_results_id_get**
> Result read_result_results_id_get(id)

Retrieve result

Get result by ID.

### Example

* Api Key Authentication (user):
```python
from __future__ import print_function
import time
import compute_api_client
from compute_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: user
configuration.api_key['user'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.ResultsApi(api_client)
    id = 56 # int | 

    try:
        # Retrieve result
        api_response = api_instance.read_result_results_id_get(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ResultsApi->read_result_results_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Result**](Result.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_results_by_run_id_results_run_run_id_get**
> list[Result] read_results_by_run_id_results_run_run_id_get(run_id)

Retrieve result

Get result by ID.

### Example

* Api Key Authentication (user):
```python
from __future__ import print_function
import time
import compute_api_client
from compute_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = compute_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: user
configuration.api_key['user'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['user'] = 'Bearer'

# Enter a context with an instance of the API client
with compute_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = compute_api_client.ResultsApi(api_client)
    run_id = 56 # int | 

    try:
        # Retrieve result
        api_response = api_instance.read_results_by_run_id_results_run_run_id_get(run_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ResultsApi->read_results_by_run_id_results_run_run_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_id** | **int**|  | 

### Return type

[**list[Result]**](Result.md)

### Authorization

[user](../README.md#user)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not Found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

