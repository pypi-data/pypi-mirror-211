from serializers.json_serializer.JsonSerializer import JsonSerializer
from serializers.xml_serializer.XmlSerializer import XmlSerializer


class SerializersFactory:
    @staticmethod
    def create_serializer(name: str):
        match name.lower():
            case "json":
                return JsonSerializer
            case "xml":
                return XmlSerializer
            case _:
                raise ValueError(f"{name} is not supported!")
