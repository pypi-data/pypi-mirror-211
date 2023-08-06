from __future__ import annotations
from dataclasses import dataclass
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.response_handler import ResponseHandler
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ....models import error, red_hat_error_representation, service_account_create_request_data, service_account_data, validation_exception_data

class V1RequestBuilder():
    """
    Builds and executes requests for operations under /apis/service_accounts/v1
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new V1RequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception("path_parameters cannot be undefined")
        if request_adapter is None:
            raise Exception("request_adapter cannot be undefined")
        # Url template to use to build the URL for the current request builder
        self.url_template: str = "{+baseurl}/apis/service_accounts/v1{?first*,max*,clientId*}"

        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter
    
    async def get(self,request_configuration: Optional[V1RequestBuilderGetRequestConfiguration] = None) -> Optional[List[service_account_data.ServiceAccountData]]:
        """
        Returns a list of service accounts created by a user. User information is obtained from the bearer token. The list is paginated with starting index as 'first' and page size as 'max'.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[service_account_data.ServiceAccountData]]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ....models import error, red_hat_error_representation, validation_exception_data

        error_mapping: Dict[str, ParsableFactory] = {
            "400": validation_exception_data.ValidationExceptionData,
            "401": error.Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models import service_account_data

        return await self.request_adapter.send_collection_async(request_info, service_account_data.ServiceAccountData, error_mapping)
    
    async def post(self,body: Optional[service_account_create_request_data.ServiceAccountCreateRequestData] = None, request_configuration: Optional[V1RequestBuilderPostRequestConfiguration] = None) -> Optional[service_account_data.ServiceAccountData]:
        """
        Create a service account. Created service account is associated with the user defined in the bearer token.
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[service_account_data.ServiceAccountData]
        """
        if body is None:
            raise Exception("body cannot be undefined")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ....models import error, red_hat_error_representation, validation_exception_data

        error_mapping: Dict[str, ParsableFactory] = {
            "400": validation_exception_data.ValidationExceptionData,
            "401": error.Error,
            "403": red_hat_error_representation.RedHatErrorRepresentation,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models import service_account_data

        return await self.request_adapter.send_async(request_info, service_account_data.ServiceAccountData, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[V1RequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns a list of service accounts created by a user. User information is obtained from the bearer token. The list is paginated with starting index as 'first' and page size as 'max'.
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers["Accept"] = ["application/json"]
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    def to_post_request_information(self,body: Optional[service_account_create_request_data.ServiceAccountCreateRequestData] = None, request_configuration: Optional[V1RequestBuilderPostRequestConfiguration] = None) -> RequestInformation:
        """
        Create a service account. Created service account is associated with the user defined in the bearer token.
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise Exception("body cannot be undefined")
        request_info = RequestInformation()
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.POST
        request_info.headers["Accept"] = ["application/json"]
        if request_configuration:
            request_info.add_request_headers(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    @dataclass
    class V1RequestBuilderGetQueryParameters():
        """
        Returns a list of service accounts created by a user. User information is obtained from the bearer token. The list is paginated with starting index as 'first' and page size as 'max'.
        """
        client_id: Optional[List[str]] = None

        first: Optional[int] = None

        max: Optional[int] = None

    
    @dataclass
    class V1RequestBuilderGetRequestConfiguration():
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request headers
        headers: Optional[Dict[str, Union[str, List[str]]]] = None

        # Request options
        options: Optional[List[RequestOption]] = None

        # Request query parameters
        query_parameters: Optional[V1RequestBuilder.V1RequestBuilderGetQueryParameters] = None

    
    @dataclass
    class V1RequestBuilderPostRequestConfiguration():
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request headers
        headers: Optional[Dict[str, Union[str, List[str]]]] = None

        # Request options
        options: Optional[List[RequestOption]] = None

    

