from ser_Anton.json_serializer import json_ser
from ser_Anton.xml_serializer import xml_ser


class ser_factory:
    @staticmethod
    def create_ser(format):
        format = format.lower()

        if format == "json":
            return json_ser()
        elif format == "xml":
            return xml_ser()
        else:
            raise ValueError("No such format")