import qtoml
import lib.util.serializer_core as core
from lib.parsers.parser import Serializer


class TomlSerializer(Serializer):
    def dumps(self, item):
        return qtoml.dumps(core.serialize(item), encode_none='null')

    def loads(self, string):
        return core.deserialize(qtoml.loads(string))


