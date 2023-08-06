from __future__ import annotations
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .beta import beta_request_builder
    from .organizations import organizations_request_builder
    from .service_accounts import service_accounts_request_builder

class ApisRequestBuilder():
    """
    Builds and executes requests for operations under /apis
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new ApisRequestBuilder and sets the default values.
        Args:
            pathParameters: The raw url or the Url template parameters for the request.
            requestAdapter: The request adapter to use to execute the requests.
        """
        if path_parameters is None:
            raise Exception("path_parameters cannot be undefined")
        if request_adapter is None:
            raise Exception("request_adapter cannot be undefined")
        # Url template to use to build the URL for the current request builder
        self.url_template: str = "{+baseurl}/apis"

        url_tpl_params = get_path_parameters(path_parameters)
        self.path_parameters = url_tpl_params
        self.request_adapter = request_adapter
    
    @property
    def beta(self) -> beta_request_builder.BetaRequestBuilder:
        """
        The beta property
        """
        from .beta import beta_request_builder

        return beta_request_builder.BetaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def organizations(self) -> organizations_request_builder.OrganizationsRequestBuilder:
        """
        The organizations property
        """
        from .organizations import organizations_request_builder

        return organizations_request_builder.OrganizationsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def service_accounts(self) -> service_accounts_request_builder.Service_accountsRequestBuilder:
        """
        The service_accounts property
        """
        from .service_accounts import service_accounts_request_builder

        return service_accounts_request_builder.Service_accountsRequestBuilder(self.request_adapter, self.path_parameters)
    

