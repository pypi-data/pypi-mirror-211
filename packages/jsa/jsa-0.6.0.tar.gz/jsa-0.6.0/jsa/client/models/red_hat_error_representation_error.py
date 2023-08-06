from enum import Enum

class RedHatErrorRepresentation_error(Enum):
    Service_account_limit_exceeded = "service_account_limit_exceeded",
    Service_account_not_found = "service_account_not_found",
    Service_account_user_not_found = "service_account_user_not_found",
    Service_account_access_invalid = "service_account_access_invalid",
    Acs_tenant_limit_exceeded = "acs_tenant_limit_exceeded",
    Acs_tenant_not_found = "acs_tenant_not_found",
    Acs_access_invalid = "acs_access_invalid",
    Acs_invalid_redirect_uri = "acs_invalid_redirect_uri",
    Acs_invalid_client = "acs_invalid_client",
    Acs_disabled = "acs_disabled",
    Smoketest_access_invalid = "smoketest_access_invalid",
    Smoketest_not_found = "smoketest_not_found",
    General_failure = "general_failure",
    Organization_api_access_invalid = "organization_api_access_invalid",

