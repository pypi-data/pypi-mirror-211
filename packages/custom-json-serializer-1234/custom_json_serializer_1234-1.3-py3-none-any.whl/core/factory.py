from core.serializers.xmlserializer import XMLSerializer
from core.serializers.jsonserializer import JSONSerializer


class Factory:
    @staticmethod
    def create_serializer(file_type):
        if file_type == "json":
            return JSONSerializer()
        elif file_type == "xml":
            return XMLSerializer()
