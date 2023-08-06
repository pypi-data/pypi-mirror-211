from __future__ import annotations
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .v1 import v1_request_builder
    from .v1.item import v1_item_request_builder

class OrganizationsRequestBuilder():
    """
    Builds and executes requests for operations under /apis/organizations
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new OrganizationsRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception("path_parameters cannot be undefined")
        if request_adapter is None:
            raise Exception("request_adapter cannot be undefined")
        # Url template to use to build the URL for the current request builder
        self.url_template: str = "{+baseurl}/apis/organizations"

        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter
    
    def v1_by_id(self,id: str) -> v1_item_request_builder.V1ItemRequestBuilder:
        """
        Gets an item from the client.apis.organizations.v1.item collection
        Args:
            id: Unique identifier of the item
        Returns: v1_item_request_builder.V1ItemRequestBuilder
        """
        if id is None:
            raise Exception("id cannot be undefined")
        from .v1.item import v1_item_request_builder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["id"] = id
        return v1_item_request_builder.V1ItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    @property
    def v1(self) -> v1_request_builder.V1RequestBuilder:
        """
        The v1 property
        """
        from .v1 import v1_request_builder

        return v1_request_builder.V1RequestBuilder(self.request_adapter, self.path_parameters)
    

