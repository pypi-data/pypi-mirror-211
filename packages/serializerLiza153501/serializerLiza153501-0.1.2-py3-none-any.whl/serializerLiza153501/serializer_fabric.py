from serializerLiza153501.serializer_json import serialise_JSON
from serializerLiza153501.serializer_xml import serialize_XML

class Serializer_fabric:

    @staticmethod
    def create_serializer(format_name: str):
        format_name = format_name.lower()

        if (format_name == "json"):
            return serialise_JSON()
        elif (format_name == "xml"):
            return serialize_XML()
        else:
            raise ValueError