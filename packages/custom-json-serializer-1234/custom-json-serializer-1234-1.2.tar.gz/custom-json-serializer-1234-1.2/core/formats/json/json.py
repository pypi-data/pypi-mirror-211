from core.formats.parsers import parse_json
from core.serializer import Serializer


class JsonSerializer:
    @staticmethod
    def dumps(item):
        return str(Serializer().serialize(item)).replace("\n", "\\n")

    @staticmethod
    def dump(item, file):
        file.write(JsonSerializer.dumps(item))

    @staticmethod
    def loads(item):
        return Serializer().deserialize(parse_json(item.replace("\\n", "\n")))

    @staticmethod
    def load(file):
        return JsonSerializer.loads(file.read())
