from core.formats.parsers import dumps_from_dict, loads_to_dict
from core.serializer import Serializer


class XmlSerializer:
    @staticmethod
    def dumps(obj):
        obj = Serializer().serialize(obj)

        return dumps_from_dict(obj)

    @staticmethod
    def loads(item):
        item = loads_to_dict(item)

        return Serializer().deserialize(item)

    @staticmethod
    def dump(item, file):
        file.write(XmlSerializer.dumps(item))

    @staticmethod
    def load(file):
        return XmlSerializer.loads(file.read())
