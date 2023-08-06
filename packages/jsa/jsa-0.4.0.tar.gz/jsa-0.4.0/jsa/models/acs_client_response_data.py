from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

class AcsClientResponseData(AdditionalDataHolder, Parsable):
    def __init__(self,) -> None:
        """
        Instantiates a new AcsClientResponseData and sets the default values.
        """
        # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        self._additional_data: Dict[str, Any] = {}

        # The clientId property
        self._client_id: Optional[str] = None
        # The createdAt property
        self._created_at: Optional[int] = None
        # The name property
        self._name: Optional[str] = None
        # The secret property
        self._secret: Optional[str] = None
    
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
    def client_id(self,) -> Optional[str]:
        """
        Gets the clientId property value. The clientId property
        Returns: Optional[str]
        """
        return self._client_id
    
    @client_id.setter
    def client_id(self,value: Optional[str] = None) -> None:
        """
        Sets the clientId property value. The clientId property
        Args:
            value: Value to set for the client_id property.
        """
        self._client_id = value
    
    @property
    def created_at(self,) -> Optional[int]:
        """
        Gets the createdAt property value. The createdAt property
        Returns: Optional[int]
        """
        return self._created_at
    
    @created_at.setter
    def created_at(self,value: Optional[int] = None) -> None:
        """
        Sets the createdAt property value. The createdAt property
        Args:
            value: Value to set for the created_at property.
        """
        self._created_at = value
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> AcsClientResponseData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: AcsClientResponseData
        """
        if parse_node is None:
            raise Exception("parse_node cannot be undefined")
        return AcsClientResponseData()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "clientId": lambda n : setattr(self, 'client_id', n.get_str_value()),
            "createdAt": lambda n : setattr(self, 'created_at', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "secret": lambda n : setattr(self, 'secret', n.get_str_value()),
        }
        return fields
    
    @property
    def name(self,) -> Optional[str]:
        """
        Gets the name property value. The name property
        Returns: Optional[str]
        """
        return self._name
    
    @name.setter
    def name(self,value: Optional[str] = None) -> None:
        """
        Sets the name property value. The name property
        Args:
            value: Value to set for the name property.
        """
        self._name = value
    
    @property
    def secret(self,) -> Optional[str]:
        """
        Gets the secret property value. The secret property
        Returns: Optional[str]
        """
        return self._secret
    
    @secret.setter
    def secret(self,value: Optional[str] = None) -> None:
        """
        Sets the secret property value. The secret property
        Args:
            value: Value to set for the secret property.
        """
        self._secret = value
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception("writer cannot be undefined")
        writer.write_str_value("clientId", self.client_id)
        writer.write_int_value("createdAt", self.created_at)
        writer.write_str_value("name", self.name)
        writer.write_str_value("secret", self.secret)
        writer.write_additional_data_value(self.additional_data)
    

