from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from . import authentication_factors

class AuthenticationPolicy(AdditionalDataHolder, Parsable):
    def __init__(self,) -> None:
        """
        Instantiates a new AuthenticationPolicy and sets the default values.
        """
        # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        self._additional_data: Dict[str, Any] = {}

        # The authenticationFactors property
        self._authentication_factors: Optional[authentication_factors.AuthenticationFactors] = None
    
    @property
    def additional_data(self,) -> Dict[str, Any]:
        """
        Gets the additionalData property value. Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        Returns: Dict[str, Any]
        """
        return self._additional_data
    
    @additional_data.setter
    def additional_data(self,value: Dict[str, Any]) -> None:
        """
        Sets the additionalData property value. Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        Args:
            value: Value to set for the AdditionalData property.
        """
        self._additional_data = value
    
    @property
    def authentication_factors(self,) -> Optional[authentication_factors.AuthenticationFactors]:
        """
        Gets the authenticationFactors property value. The authenticationFactors property
        Returns: Optional[authentication_factors.AuthenticationFactors]
        """
        return self._authentication_factors
    
    @authentication_factors.setter
    def authentication_factors(self,value: Optional[authentication_factors.AuthenticationFactors] = None) -> None:
        """
        Sets the authenticationFactors property value. The authenticationFactors property
        Args:
            value: Value to set for the authentication_factors property.
        """
        self._authentication_factors = value
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> AuthenticationPolicy:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: AuthenticationPolicy
        """
        if parse_node is None:
            raise Exception("parse_node cannot be undefined")
        return AuthenticationPolicy()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import authentication_factors

        fields: Dict[str, Callable[[Any], None]] = {
            "authenticationFactors": lambda n : setattr(self, 'authentication_factors', n.get_object_value(authentication_factors.AuthenticationFactors)),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception("writer cannot be undefined")
        writer.write_object_value("authenticationFactors", self.authentication_factors)
        writer.write_additional_data_value(self.additional_data)
    

