from __future__ import annotations
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

class AcsClientRequestData(AdditionalDataHolder, Parsable):
    def __init__(self,) -> None:
        """
        Instantiates a new AcsClientRequestData and sets the default values.
        """
        # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        self._additional_data: Dict[str, Any] = {}

        # The name property
        self._name: Optional[str] = None
        # The orgId property
        self._org_id: Optional[str] = None
        # The redirectUris property
        self._redirect_uris: Optional[List[str]] = None
    
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
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> AcsClientRequestData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: AcsClientRequestData
        """
        if parse_node is None:
            raise Exception("parse_node cannot be undefined")
        return AcsClientRequestData()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "orgId": lambda n : setattr(self, 'org_id', n.get_str_value()),
            "redirectUris": lambda n : setattr(self, 'redirect_uris', n.get_collection_of_primitive_values(str)),
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
    def org_id(self,) -> Optional[str]:
        """
        Gets the orgId property value. The orgId property
        Returns: Optional[str]
        """
        return self._org_id
    
    @org_id.setter
    def org_id(self,value: Optional[str] = None) -> None:
        """
        Sets the orgId property value. The orgId property
        Args:
            value: Value to set for the org_id property.
        """
        self._org_id = value
    
    @property
    def redirect_uris(self,) -> Optional[List[str]]:
        """
        Gets the redirectUris property value. The redirectUris property
        Returns: Optional[List[str]]
        """
        return self._redirect_uris
    
    @redirect_uris.setter
    def redirect_uris(self,value: Optional[List[str]] = None) -> None:
        """
        Sets the redirectUris property value. The redirectUris property
        Args:
            value: Value to set for the redirect_uris property.
        """
        self._redirect_uris = value
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception("writer cannot be undefined")
        writer.write_str_value("name", self.name)
        writer.write_str_value("orgId", self.org_id)
        writer.write_collection_of_primitive_values("redirectUris", self.redirect_uris)
        writer.write_additional_data_value(self.additional_data)
    

