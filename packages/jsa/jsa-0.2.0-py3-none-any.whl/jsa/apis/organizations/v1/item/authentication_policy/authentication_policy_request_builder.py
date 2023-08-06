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
    from ......models import authentication_policy, error

class AuthenticationPolicyRequestBuilder():
    """
    Builds and executes requests for operations under /apis/organizations/v1/{id}/authentication-policy
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new AuthenticationPolicyRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception("path_parameters cannot be undefined")
        if request_adapter is None:
            raise Exception("request_adapter cannot be undefined")
        # Url template to use to build the URL for the current request builder
        self.url_template: str = "{+baseurl}/apis/organizations/v1/{id}/authentication-policy"

        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter
    
    async def get(self,request_configuration: Optional[AuthenticationPolicyRequestBuilderGetRequestConfiguration] = None) -> Optional[authentication_policy.AuthenticationPolicy]:
        """
        Get current authentication policy information
        Args:
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[authentication_policy.AuthenticationPolicy]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ......models import error

        error_mapping: Dict[str, ParsableFactory] = {
            "401": error.Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models import authentication_policy

        return await self.request_adapter.send_async(request_info, authentication_policy.AuthenticationPolicy, error_mapping)
    
    async def post(self,body: Optional[authentication_policy.AuthenticationPolicy] = None, request_configuration: Optional[AuthenticationPolicyRequestBuilderPostRequestConfiguration] = None) -> Optional[authentication_policy.AuthenticationPolicy]:
        """
        Update current authentication policy information
        Args:
            body: The request body
            requestConfiguration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[authentication_policy.AuthenticationPolicy]
        """
        if body is None:
            raise Exception("body cannot be undefined")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ......models import error

        error_mapping: Dict[str, ParsableFactory] = {
            "401": error.Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models import authentication_policy

        return await self.request_adapter.send_async(request_info, authentication_policy.AuthenticationPolicy, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[AuthenticationPolicyRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Get current authentication policy information
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
            request_info.add_request_options(request_configuration.options)
        return request_info
    
    def to_post_request_information(self,body: Optional[authentication_policy.AuthenticationPolicy] = None, request_configuration: Optional[AuthenticationPolicyRequestBuilderPostRequestConfiguration] = None) -> RequestInformation:
        """
        Update current authentication policy information
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
    class AuthenticationPolicyRequestBuilderGetRequestConfiguration():
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request headers
        headers: Optional[Dict[str, Union[str, List[str]]]] = None

        # Request options
        options: Optional[List[RequestOption]] = None

    
    @dataclass
    class AuthenticationPolicyRequestBuilderPostRequestConfiguration():
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request headers
        headers: Optional[Dict[str, Union[str, List[str]]]] = None

        # Request options
        options: Optional[List[RequestOption]] = None

    

